from spotify_integration.spotify_client import SpotifyClient

client = SpotifyClient()

def test():
    print(client.generate_private_client_token())


if __name__ == "__main__":
    test()
