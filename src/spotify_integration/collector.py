import time

from spotify_integration.spotify_client import SpotifyClient
from spotify_integration.spotify_public_client import SpotifyPublicClient
from spotify_integration.storage_manager import StorageManager


class Collector:
    def __init__(self) -> None:
        self.client = SpotifyClient()
        self.public_client = SpotifyPublicClient()

        self.storage_manager = StorageManager()

    def collect_data(self):
        start_time = time.time()
        print("Coletando artistas")
        artists = self.get_artists(artist_name="Beyonce", offset=0, limit=1) # Pegar Beyonce

        for artist in artists:
            print("Coletando albums")
            albums = self.get_albums(artist_id=artist.get("id"), offset=0, limit=50) # Pegar albums da Beyonce

            tracks = []
            tracks_credits = []

            for album in albums:
                print("Coletando tracks do album " + album.get("id"))

                tracks += self.get_tracks(album_id=album.get("id"), offset=0, limit=50) # Pegar dados do album RENAISSANCE da Beyonce

                for track in tracks:
                    print("Coletando credits da track " + track.get("id"))
                    tracks_credits = self.get_credits(track_id=track.get("id")) # Créditos da musica HEATED

            self.storage_manager.save_songs(tracks)
            self.storage_manager.save_credits(tracks_credits)
            self.storage_manager.save_albums(albums)

        self.storage_manager.save_artists(artists)

        print("Tempo de coleta --- %s seconds ---" % (time.time() - start_time))

        start_time = time.time()
        self.storage_manager.persist()
        print("Tempo para salvar no arquivo --- %s seconds ---" % (time.time() - start_time))


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

        return credits_response

    def get_lyrics(self):
        pass