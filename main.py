import datetime as dt
import logging
import traceback
from typing import List

from job_notifications import create_notifications, timer
import pandas as pd
import requests
from sqlsorcery import MSSQL

import config


notifications = create_notifications("Kelvin", "mailgun", "app.log")


class Connector:
    """
    Data connector for Extracting data, Transforming into dataframes,
    ?? and loads into db (or keep the load separate from this class since we have sql_sorcery?)
    """

    def __init__(self):
        self.sql = MSSQL()
        self.headers = {"Authorization": f"token {config.API_TOKEN}"}
        self.url = "https://pulse.kelvin.education/api/v1/pulse_responses"

    def get_last_dw_update(self) -> str:
        df = pd.read_sql_table("kelvin_pulse_responses", con=self.sql.engine, schema=self.sql.schema)
        return df["responded_at"].max()

    def get_responses(self) -> List[dict]:
        """ Extract data to load into the dw """
        page = 0
        all_records = []
        while True:
            r = requests.get(f"{self.url}?page={page}", headers=self.headers).json()
            logging.debug(f"Requesting data from {self.url} page {page}")
            if r:
                all_records.extend(r)
                logging.debug(f"Extracted {len(r)} records from page {page}")
                page += 1
                if page % 50 == 0:
                    # Logging every 50 pages so we know the job isn't stalling
                    logging.info(f"Page {page} of {self.url}")
            else:
                logging.debug(f"No data from page {page}")
                break

        return all_records

    @staticmethod
    def normalize_json(records: List[dict]) -> pd.DataFrame:
        """
        Takes in dataframe of all data to be processed, and list of record paths.
        Loops over nested json and returns normalized data frame.
        """
        df = pd.json_normalize(
            records,
            record_path=["responses", "choices"],
            meta=[
                "id",
                "pulse_id",
                "pulse_name",
                "pulse_window_id",
                "pulse_window_number",
                "pulse_window_start_date",
                "pulse_window_end_date",
                "pulse_respondent_type",
                "email",
                "state_id",
                "district_id",
                "display_id",
                "participant_id",
                "responded_at",
                "needs_assistance",
                "needs_assistance_asked",
                ["responses", "question_id"],
                ["responses", "dimension_id"],
                ["responses", "skipped"],
                ["responses", "stem"],
                ["responses", "dimension"],
                ["responses", "is_favorable"],
                ["responses", "comment"],
                ["responses", "comment_share_name"],
            ],
            errors="ignore",
            sep="_",
        )

        """ Lint Columns (timestamp, sort order, data types) """
        df["LastUpdated"] = dt.datetime.now()

        col_order = [
            "id",
            "pulse_id",
            "pulse_name",
            "pulse_window_id",
            "pulse_window_number",
            "pulse_window_start_date",
            "pulse_window_end_date",
            "pulse_respondent_type",
            "email",
            "state_id",
            "district_id",
            "display_id",
            "participant_id",
            "responded_at",
            "needs_assistance",
            "needs_assistance_asked",
            "responses_question_id",
            "responses_dimension_id",
            "responses_skipped",
            "responses_stem",
            "responses_dimension",
            "responses_is_favorable",
            "responses_comment",
            "responses_comment_share_name",
            "choice",
            "sort_order",
            "number",
        ]
        df = df[col_order]

        numerics = [
            "pulse_id",
            "pulse_window_id",
            "pulse_window_number",
            "state_id",
            "display_id",
            "responses_question_id",
        ]
        for item in numerics:
            df[item] = pd.to_numeric(df[item])

        dates = ["pulse_window_start_date", "pulse_window_end_date"]
        for item in dates:
            df[item] = df[item].astype("datetime64[ns]")

        return df

    def load_into_dw(self, df: pd.DataFrame) -> None:
        """Writes the data into the related table"""

        table_name = "kelvin_pulse_responses"
        logging.info(f"{table_name}: inserting {len(df)} records into {table_name}.")
        self.sql.insert_into(table_name, df, chunksize=10000, if_exists="replace")

    def load_into_survey_model(self):
        """Take raw Kelvin data and parse it in to relational survey model dims and fact."""
        # This list allows us to loop through the table names in a specific order,
        # which is required due to dependencies
        # - dimRespondent depends on SurveyKey
        # - dimQuestion depends on dimSurvey and dimResponseItem
        # - factResponse depends on dimRespondent and dimQuestion
        table_names = [
            "Survey_dimSurvey",
            "Survey_dimRespondent",
            "Survey_dimResponseItem",
            "Survey_dimQuestion",
            "Survey_factResponse",
        ]
        for table_name in table_names:
            df = self.sql.query_from_file(f"sql/{table_name}.sql")
            if not df.empty:
                self.sql.insert_into(table_name, df)
                logging.info(f"Inserted {len(df)} records into {table_name}.")
            else:
                logging.info(f"No records to insert into {table_name}.")


def calculate_query_date(last_updated_timestamp: str) -> str:
    """
    Moving query date up by a day to avoid duplicates. Since job typically runs on a Sunday, 
    it should have all of the responses from the last date.
    """
    date_str = last_updated_timestamp.split(" ")[0]
    year, month, day = date_str.split("-")
    date_obj    = dt.date(
        year=int(year), 
        month=int(month), 
        day=int(day)
        )
    query_date = date_obj + dt.timedelta(days=1)
    return query_date.strftime("%Y-%m-%d")


@timer("Kelvin")
def main():

    config.set_logging()
    connector = Connector()
    last_update_date = connector.get_last_dw_update()
    query_date = calculate_query_date(last_update_date)

    logging.info("Getting responses from Kelvin")
    all_records = connector.get_responses()
    df_trans = connector.normalize_json(all_records)
    logging.info("Loading data into kelvin_pulse_responses")
    connector.load_into_dw(df_trans)
    logging.info("Loading data into survey models")
    connector.load_into_survey_model()


if __name__ == "__main__":
    try:
        main()
        notifications.notify()
    except Exception as e:
        logging.exception(e)
        error_message = traceback.format_exc()
        notifications.notify(error_message=error_message)
