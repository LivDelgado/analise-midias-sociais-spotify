import string
import time

from spotify_integration.exceptions import StopFetchingDataException
from spotify_integration.spotify_client import SpotifyClient
from spotify_integration.spotify_public_client import SpotifyPublicClient
from storage.storage_manager import StorageManager


class Collector:
    _LIMITE_REQUEST = 50

    def __init__(self, num_planilha: int) -> None:
        self.client = SpotifyClient()
        self.public_client = SpotifyPublicClient()

        self.storage_manager = StorageManager(num_planilha)

    def collect_data(self):
        start_time = time.time()

        print("Listando artistas")
        artists = self.storage_manager.get_artists_from_storage()

        if artists is None or not len(artists):
            raise EOFError("This file does not exist.")

        print(
            "Tempo para listar artistas --- %s segundos ---"
            % (time.time() - start_time)
        )

        start_time = time.time()

        print("Coletando dados dos artistas")

        ultimo_artista_coletado = self.storage_manager.get_last_fetched_artist_id(
            artists
        )

        indice_ultimo_artista_coletado = next(
            (
                i
                for i, item in enumerate(artists)
                if item["id"] == ultimo_artista_coletado
            ),
            0,
        )

        deveria_encerrar_o_programa = False

        for artist in artists[indice_ultimo_artista_coletado + 1 :]:
            if artist.get("popularity") == 0:
                continue

            try:
                self.collect_data_for_single_artist(artist)
            except Exception:
                print("persistindo os dados antes de encerrar")
                deveria_encerrar_o_programa = True
            finally:
                self.storage_manager.persist()
                if deveria_encerrar_o_programa:
                    exit(0)

        print("Tempo de coleta --- %s segundos ---" % (time.time() - start_time))

    def list_all_artists_from_graph(self):
        todos_os_artistas_do_grafo = {}

        try:
            alfabeto = list(string.ascii_lowercase)
            indexes_busca = alfabeto

            """
            duas_letras = list(itertools.permutations(alfabeto, 2))
            tres_letras = list(itertools.permutations(alfabeto, 3))

            indexes_busca += duas_letras
            indexes_busca += tres_letras

            indexes_busca = [''.join(element) for element in indexes_busca]
            """

            for index_busca in indexes_busca:
                offsets = range(0, 951, self._LIMITE_REQUEST)

                for i in offsets:
                    artistas = self.get_artists(
                        artist_name=index_busca, offset=i, limit=self._LIMITE_REQUEST
                    )

                    for artista in artistas:
                        todos_os_artistas_do_grafo[artista["id"]] = artista

        except Exception:
            print("salvando dados antes de encerrar!")

        finally:
            print(f"Serão coletados {len(todos_os_artistas_do_grafo.keys())} artistas")
            self.storage_manager.save_artists(todos_os_artistas_do_grafo.values())
            self.storage_manager.persist()

        return list(todos_os_artistas_do_grafo.values())

    def collect_data_for_single_artist(self, artist):
        albums = []
        tracks = []
        tracks_credits = []

        raise_exception = False

        try:
            print("Coletando albums")

            offsets = range(0, 951, self._LIMITE_REQUEST)

            for offset in offsets:
                albums_listed = self.get_albums(artist_id=artist.get("id"), offset=offset, limit=self._LIMITE_REQUEST)
                
                if not albums_listed:
                    break
                
                albums += albums_listed

            for album in albums:
                print("Coletando tracks do album " + album.get("id"))

                for offset in offsets:
                    tracks_listed = self.get_tracks(
                        album_id=album.get("id"), offset=offset, limit=self._LIMITE_REQUEST
                    )

                    if not tracks_listed:
                        break
                    
                    tracks += tracks_listed

            for track in tracks:
                print("Coletando credits da track " + track.get("id"))
                tracks_credits.append(self.get_credits(track_id=track.get("id")))

        except (KeyboardInterrupt, StopFetchingDataException, Exception):
            print("salvando dados do artista em coleta atualmente antes de encerrar")
            raise_exception = True

        finally:
            self.storage_manager.save_songs(tracks)
            self.storage_manager.save_credits(tracks_credits)
            self.storage_manager.save_albums(albums)

            if raise_exception:
                raise Exception()

    def get_artists(self, artist_name, offset, limit):
        artists_response = self.client.find_artist(
            artist_name=artist_name, offset=offset, limit=limit
        )

        if not artists_response:
            return []

        return artists_response["artists"].get("items", [])

    def get_albums(self, artist_id, offset, limit):
        albums_response = self.client.get_artist_albums(
            artist_id=artist_id, offset=offset, limit=limit
        )

        if not albums_response:
            return []

        return albums_response.get("items", [])

    def get_tracks(self, album_id, offset, limit):
        tracks_response = self.client.get_albums_tracks(
            album_id=album_id, offset=offset, limit=limit
        )

        if not tracks_response:
            return []

        return tracks_response.get("items", [])

    def get_credits(self, track_id):
        credits_response = self.public_client.get_credits(track_id=track_id)

        if not credits_response:
            return None

        return credits_response

    def get_lyrics(self):
        pass
