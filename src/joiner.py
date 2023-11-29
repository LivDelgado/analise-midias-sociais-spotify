import sys

from spotify_integration.collector import Collector
from storage.SpreadsheetJoiner import SpreadsheetJoiner


def run():
    joiner = SpreadsheetJoiner()
    joiner.persist_in_single_spreadsheet()


if __name__ == "__main__":
    run()
