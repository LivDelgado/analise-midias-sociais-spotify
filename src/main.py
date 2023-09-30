from spotify_integration.spotify_client import SpotifyClient

client = SpotifyClient()

def test():
    print(client.get_playlist_items("37i9dQZEVXbMDoHDwVN2tF"))


if __name__ == "__main__":
    test()
