import json
import logging
import traceback
import csv
import datetime as dt

import pandas as pd
from sqlsorcery import MSSQL
import requests

import config
from mailer import Mailer

class Connector:
    """
    Data connector for Extracting data, Transforming into dataframes, 
    ?? and loads into db (or keep the load separate from this class since we have sql_sorcery?)
    """

    def __init__(self):
        self.sql = MSSQL()
        token = config.API_TOKEN
        self.headers = {"Authorization": f"token {token}"}
        self.url = "https://pulse.kelvin.education/api/v1/pulse_responses"
        
    def get_last_dw_update(self): 
        df = pd.read_sql_table('kelvin_pulse_responses', con=self.sql.engine, schema=self.sql.schema)
        return df["LastUpdated"].max()

    def get_responses(self):
        """ Extract data to load into the dw """
        page = 0
        all_records = []
        while True:
            r = requests.get(f"{self.url}?page={page}", headers=self.headers).json()
            if r: 
                all_records.extend(r)
                page = page + 1
            else:
                break
    
        return all_records
    
    def normalize_json(self, records): #do these variables need to be declared within the class?
        """
           Takes in dataframe of all data to be processed, and list of record paths.
           Loops over nested json and returns normalized data frame. 
        """
        df = pd.DataFrame()
        df = pd.json_normalize(
            records,
            record_path = ["responses", "choices"],
            meta = [
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
                ["responses", "skipped"], 
                ["responses", "stem"],
                ["responses", "is_favorable"],
                ["responses", "comment"], 
                ["responses", "comment_share_name"], 
            ], 
            errors = 'ignore',
            sep = '_',
        )

        """ Lint Columns (timestamp, sort order, data types) """
        df['LastUpdated'] = dt.datetime.now()

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
            "responses_skipped",
            "responses_stem",
            "responses_is_favorable",
            "responses_comment",
            "responses_comment_share_name",
            "choice",
            "sort_order",
            "number",
        ]
        df = df[col_order]

        numerics = ['pulse_id', 'pulse_window_id', 'pulse_window_number', 'state_id', 'display_id', 'responses_question_id']
        for item in numerics: 
            df[item] = pd.to_numeric(df[item])
        
        dates = ['pulse_window_start_date', 'pulse_window_end_date']
        for item in dates: 
            df[item] = df[item].astype('datetime64[ns]')

        return df 

    def load_into_dw(self, df): 
        """Writes the data into the related table"""
        
        tablename = "kelvin_pulse_responses"
        logging.debug(f"{tablename}: inserting {len(df)} records into {tablename}.")
        self.sql.insert_into(tablename, df, chunksize=10000, if_exists='replace')
        

def main():

    config.set_logging()
    connector = Connector()

    all_records = connector.get_responses()
    df_trans = connector.normalize_json(all_records)
    connector.load_into_dw(df_trans)

if __name__ == "__main__":
    try:
        main()
        error_message = None
    except Exception as e:
        logging.exception(e)
        error_message = traceback.format_exc()
    if config.ENABLE_MAILER:
        Mailer("PROJECT NAME GOES HERE").notify(error_message=error_message)
