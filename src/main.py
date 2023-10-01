from spotify_integration.spotify_client import SpotifyClient
from spotify_integration.spotify_public_client import SpotifyPublicClient
from spotify_integration.collector import Collector

client = SpotifyClient()
# publicClient = SpotifyPublicClient()

def run():
    print("Rodou")
    print(client.find_artist(artist_name="a", offset=0, limit=2))
    print(client.find_artist(artist_name="a", offset=1, limit=2))
    print(client.find_artist(artist_name="a", offset=2, limit=2))



if __name__ == "__main__":
    run()