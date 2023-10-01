from spotify_integration.spotify_client import SpotifyClient
from spotify_integration.spotify_public_client import SpotifyPublicClient

class Collector:
    def __init__(self) -> None:
        self.client = SpotifyClient()

    def collect_data(self):
        pass

    def get_artists(self, artist_name, offset, limit):
        return self.client.find_artist(artist_name=artist_name, offset=offset, limit=limit)

    def get_albums(self, artist_id, offset, limit):
        return self.client.get_artist_albums(artist_id=artist_id, offset=offset, limit=limit)

    def get_tracks(self, album_id, offset, limit):
        return self.client.get_albums_tracks(album_id=album_id, offset=offset, limit=limit)

    def get_credits(self, track_id):
        publicClient = SpotifyPublicClient()
        return publicClient.get_credits(track_id=track_id)

    def get_lyrics(self):
        pass