import time
import string

from spotify_integration.spotify_client import SpotifyClient
from spotify_integration.spotify_public_client import SpotifyPublicClient
from spotify_integration.storage_manager import StorageManager


class Collector:
    _LIMITE_REQUEST = 50

    def __init__(self) -> None:
        self.client = SpotifyClient()
        self.public_client = SpotifyPublicClient()

        self.storage_manager = StorageManager()

    def collect_data(self):
        start_time = time.time()

        print("Listando artistas")
        artists = self.list_all_artists_from_graph()
        print("Tempo para listar artistas --- %s segundos ---" % (time.time() - start_time))

        """
        start_time = time.time()

        print("Coletando dados dos artistas")
        for artist in artists:
            collect_data_for_single_artist(artist)

        print("Tempo de coleta --- %s segundos ---" % (time.time() - start_time))

        start_time = time.time()
        print("Salvando os dados em arquivo")
        self.storage_manager.persist()
        print("Tempo para salvar no arquivo --- %s segundos ---" % (time.time() - start_time))
        """

    def list_all_artists_from_graph(self):
        alfabeto = list(string.ascii_lowercase)

        todos_os_artistas_do_grafo = []

        for letra in alfabeto:
            for i in range(0, 951, self._LIMITE_REQUEST):
                todos_os_artistas_do_grafo += self.get_artists(artist_name=letra, offset=i, limit=self._LIMITE_REQUEST)

        todos_os_artistas_do_grafo = list({artista['id']: artista for artista in todos_os_artistas_do_grafo}.values())

        print(f"Serão coletados {len(todos_os_artistas_do_grafo)} artistas")

        return todos_os_artistas_do_grafo

    def collect_data_for_single_artist(self, artist):
        print("Coletando albums")
        albums = self.get_albums(artist_id=artist.get("id"), offset=0, limit=self._LIMITE_REQUEST)

        tracks = []
        tracks_credits = []

        for album in albums:
            print("Coletando tracks do album " + album.get("id"))
            tracks += self.get_tracks(album_id=album.get("id"), offset=0, limit=self._LIMITE_REQUEST)

        for track in tracks:
            print("Coletando credits da track " + track.get("id"))
            tracks_credits.append(self.get_credits(track_id=track.get("id")))

        self.storage_manager.save_songs(tracks)
        self.storage_manager.save_credits(tracks_credits)
        self.storage_manager.save_albums(albums)

        self.storage_manager.save_artists([artist])


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