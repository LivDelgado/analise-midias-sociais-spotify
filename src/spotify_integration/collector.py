from spotify_integration.spotify_client import SpotifyClient

class Collector:
    def __init__(self) -> None:
        self.client = SpotifyClient()

    def collect_data(self):
        pass

    def get_artists(self, artist_name, offset):
        return self.client.find_artist(artist_name=artist_name, offset=offset)

    def get_albums(self, artist_id, offset):
        return self.client.get_artist_albums(artist_id=artist_id, offset=offset)

    def get_tracks(self, album_id, offset):
        return self.client.get_albums_tracks(album_id=album_id, offset=offset)

    def get_credits(self):
        pass

    def get_lyrics(self):
        pass