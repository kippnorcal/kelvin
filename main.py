import logging
import traceback

import pandas as pd
from sqlsorcery import MSSQL

import config
from mailer import Mailer


class Connector:
    """
    Data connector for Extracting data, Transforming into dataframes, 
    and Loading into a database.
    """

    def __init__(self):
        self.sql = MSSQL()


def main():
    config.set_logging()
    connector = Connector()


if __name__ == "__main__":
    try:
        main()
        error_message = None
    except Exception as e:
        logging.exception(e)
        error_message = traceback.format_exc()
    if config.ENABLE_MAILER:
        Mailer("PROJECT NAME GOES HERE").notify(error_message=error_message)
