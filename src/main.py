from spotify_integration.spotify_client import SpotifyClient
from spotify_integration.spotify_public_client import SpotifyPublicClient
from spotify_integration.collector import Collector
from spotify_integration.storage_manager import StorageManager


collector = Collector()
storage_manager = StorageManager()

def run():
    print("Rodou")
    artists = collector.get_artists(artist_name="Beyonce", offset=0, limit=1) # Pegar Beyonce
    albums = collector.get_albums(artist_id="6vWDO969PvNqNYHIOW5v0m", offset=0, limit=1) # Pegar albums da Beyonce
    tracks = collector.get_tracks(album_id="6FJxoadUE4JNVwWHghBwnb", offset=0, limit=50) # Pegar dados do album RENAISSANCE da Beyonce
    # tracks_credits = collector.get_credits(track_id="1w7cgGZR86yWz1pA2puVJD") # Créditos da mpusica HEATED

    storage_manager.save_artists(artists)
    storage_manager.save_albums(albums)
    storage_manager.save_songs(tracks)
    # storage_manager.save_credits(tracks_credits) #-> ta com erro!

    storage_manager.persist()


if __name__ == "__main__":
    run()