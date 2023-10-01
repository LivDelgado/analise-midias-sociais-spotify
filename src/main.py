from spotify_integration.spotify_client import SpotifyClient
from spotify_integration.spotify_public_client import SpotifyPublicClient

client = SpotifyClient()
publicClient = SpotifyPublicClient()

def test():
    print(client.get_playlist_items("37i9dQZEVXbMDoHDwVN2tF"))


if __name__ == "__main__":
    test()
