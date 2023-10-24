from spotify_integration.collector import Collector

collector = Collector()


def run():
    collector.collect_data()


if __name__ == "__main__":
    run()
