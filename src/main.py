from spotify_integration.spotify_client import SpotifyClient
from spotify_integration.spotify_public_client import SpotifyPublicClient

client = SpotifyClient()
# publicClient = SpotifyPublicClient()

def run():
    print("Rodou")
    print(client.find_artist("a"))



if __name__ == "__main__":
    run()