from spotify_integration.spotify_client import SpotifyClient
from spotify_integration.spotify_public_client import SpotifyPublicClient
from spotify_integration.collector import Collector
collector = Collector()

def run():
    print("Rodou")
    print(collector.get_artists(artist_name="Beyonce", offset=0, limit=1)) # Pegar Beyonce
    print(collector.get_albums(artist_id="6vWDO969PvNqNYHIOW5v0m", offset=0, limit=1)) # Pegar albums da Beyonce
    print(collector.get_tracks(album_id="6FJxoadUE4JNVwWHghBwnb", offset=0, limit=50)) # Pegar dados do album RENAISSANCE da Beyonce
    print(collector.get_credits(track_id="1w7cgGZR86yWz1pA2puVJD")) # Créditos da mpusica HEATED

if __name__ == "__main__":
    run()