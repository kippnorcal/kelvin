import argparse
import logging
import os
import sys


parser = argparse.ArgumentParser(description="Pick which ones")
parser.add_argument("--debug", help="Enable debug logging", action="store_true")
ARGS, _ = parser.parse_known_args()

ENABLE_MAILER = int(os.getenv("ENABLE_MAILER", default=0))
DEBUG = ARGS.debug or int(os.getenv("DEBUG", default=0))


def set_logging():
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
