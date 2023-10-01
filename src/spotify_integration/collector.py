from spotify_integration.spotify_client import SpotifyClient
from spotify_integration.spotify_public_client import SpotifyPublicClient

class Collector:
    def __init__(self) -> None:
        self.client = SpotifyClient()
        self.public_client = SpotifyPublicClient()

    def collect_data(self):
        pass

    def get_artists(self, artist_name, offset, limit):
        artists_response = self.client.find_artist(artist_name=artist_name, offset=offset, limit=limit)

        return artists_response["artists"].get("items", [])

    def get_albums(self, artist_id, offset, limit):
        albums_response = self.client.get_artist_albums(artist_id=artist_id, offset=offset, limit=limit)

        return albums_response.get("items", [])

    def get_tracks(self, album_id, offset, limit):
        tracks_response = self.client.get_albums_tracks(album_id=album_id, offset=offset, limit=limit)

        return tracks_response.get("items", [])

    def get_credits(self, track_id):
        credits_response = self.public_client.get_credits(track_id=track_id)
        print(credits_response)

        return credits_response

    def get_lyrics(self):
        pass