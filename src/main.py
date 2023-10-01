from spotify_integration.spotify_client import SpotifyClient
from spotify_integration.spotify_public_client import SpotifyPublicClient
from spotify_integration.storage_manager import StorageManager

client = SpotifyClient()
# publicClient = SpotifyPublicClient()

storage_manager = StorageManager()

def run():
    print("Rodou")
    items = client.find_artist("a")
    artists=items["artists"]["items"]

    storage_manager.save_artists(artists)

    items = client.find_artist("x")
    artists=items["artists"]["items"]
    storage_manager.save_artists(artists)

    print(storage_manager.artists_df.shape)


if __name__ == "__main__":
    run()