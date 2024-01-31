import argparse
import logging
import os
import sys

def setup_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--debug", 
        dest="debug",
        help="Enable debug logging", 
        action="store_true"
        )
    parser.add_argument(
        "--truncate-reload", 
        dest="truncate_reload", 
        help="Full truncate and reload of Kevin Pulse data", 
        action="store_true"
        )
    return parser.parse_args()

ARGS = setup_arg_parser()

ENABLE_MAILER = int(os.getenv("ENABLE_MAILER", default=0))
DEBUG = ARGS.debug or int(os.getenv("DEBUG", default=0))
API_TOKEN = os.getenv("API_TOKEN")


def set_logging() -> None:
    """Configure logging level and outputs"""
    logging.basicConfig(
        handlers=[
            logging.FileHandler(filename="app.log", mode="w+"),
            logging.StreamHandler(sys.stdout),
        ],
        level=logging.DEBUG if DEBUG else logging.INFO,
        format="%(asctime)s | %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %I:%M:%S%p %Z",
    )
