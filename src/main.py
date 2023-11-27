import sys

from spotify_integration.collector import Collector


def run():
    collector = Collector()
    collector.collect_data()


if __name__ == "__main__":
    run()
