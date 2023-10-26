import sys

from spotify_integration.collector import Collector


def run(num: int):
    collector = Collector(num)
    collector.collect_data()


if __name__ == "__main__":
    num_planilha = sys.argv[1]
    run(int(num_planilha))
