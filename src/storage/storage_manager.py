from typing import Optional

import pandas as pd

from storage.constants import Constants


class StorageManager:

    def __init__(self, num_planilha: int) -> None:
        self.num_planilha = num_planilha
        self.__FILE_NAME = f"arquivos/coleta_dividida/coleta_dados_spotify_{num_planilha}.xlsx"
        self.artists_df = pd.DataFrame()
        self.albums_df = pd.DataFrame()
        self.songs_df = pd.DataFrame()
        self.credits_df = pd.DataFrame()
        self.lyrics_df = pd.DataFrame()

        self.albums_artists_df = pd.DataFrame()
        self.songs_artists_df = pd.DataFrame()

        self.fetch_all_data_from_storage()

    def get_artists_from_storage(self):
        try:
            if self.artists_df.empty:
                self.fetch_all_data_from_storage()

            return self.artists_df.reset_index().to_dict("records")
        except Exception as error:
            print(error)
            return None

    def get_last_fetched_artist_id(self, artists):
        try:
            if self.artists_df.empty or self.albums_artists_df.empty:
                self.fetch_all_data_from_storage()

            indice = -1
            ultimo_artista_coletado = (
                self.albums_artists_df.reset_index()
                .to_dict("records")[indice]
                .get("artist_id")
            )

            while not next(
                (item for item in artists if item.get("id") == ultimo_artista_coletado),
                None,
            ):
                indice = indice - 1
                ultimo_artista_coletado = (
                    self.albums_artists_df.reset_index()
                    .to_dict("records")[indice]
                    .get("artist_id")
                )

            return ultimo_artista_coletado
        except Exception as error:
            print(error)
            return None

    def save_artists(self, artists):
        for artist in artists:
            del artist["images"]

        new_artists = pd.DataFrame.from_dict(artists)
        self.artists_df = pd.concat([self.artists_df, new_artists], ignore_index=True)

    def save_albums(self, albums):
        albums_artists_list = []

        for album in albums:
            artists = album.get("artists")
            for artist in artists:
                album_artist = {
                    "album_id": album.get("id"),
                    "artist_id": artist.get("id"),
                    "artist_name": artist.get("name"),
                    "artist_type": artist.get("type"),
                }

                albums_artists_list.append(album_artist)

            del album["images"]
            del album["artists"]

        new_albums = pd.DataFrame.from_dict(albums)
        self.albums_df = pd.concat([self.albums_df, new_albums], ignore_index=True)

        new_albums_artists = pd.DataFrame.from_dict(albums_artists_list)
        self.albums_artists_df = pd.concat(
            [self.albums_artists_df, new_albums_artists], ignore_index=True
        )

    def save_songs(self, songs):
        songs_artists_list = []

        for song in songs:
            artists = song.get("artists")
            for artist in artists:
                song_artist = {
                    "track_id": song.get("id"),
                    "artist_id": artist.get("id"),
                    "artist_name": artist.get("name"),
                    "artist_type": artist.get("type"),
                }

                songs_artists_list.append(song_artist)

            del song["artists"]

        new_songs = pd.DataFrame.from_dict(songs)
        self.songs_df = pd.concat([self.songs_df, new_songs], ignore_index=True)

        new_songs_artists = pd.DataFrame.from_dict(songs_artists_list)
        self.songs_artists_df = pd.concat(
            [self.songs_artists_df, new_songs_artists], ignore_index=True
        )

    def save_credits(self, credits):
        track_credits_flatten_list = []

        for credit in credits:
            if not credit:
                continue

            for role_credits in credit["roleCredits"]:
                for artist in role_credits.get("artists"):
                    credits_flatten = {
                        "trackUri": credit["trackUri"],
                        "trackTitle": credit["trackTitle"],
                        "roleTitle": role_credits["roleTitle"],
                        "artist_uri": artist.get("uri", ""),
                        "artist_name": artist.get("name", ""),
                        "artist_image_uri": artist.get("imageUri", ""),
                        "artist_subroles": artist.get("subroles", []),
                        "artist_weight": artist.get("weight", 0.0),
                        "artist_external_url": artist.get("externalUrl", ""),
                        "artist_creator_uri": artist.get("creatorUri", ""),
                    }
                    track_credits_flatten_list.append(credits_flatten)

        new_credits = pd.DataFrame.from_dict(track_credits_flatten_list)
        self.credits_df = pd.concat([self.credits_df, new_credits], ignore_index=True)

    def save_lyrics(self, lyrics):
        new_lyrics = pd.DataFrame.from_dict(lyrics)
        self.lyrics_df = pd.concat([self.lyrics_df, new_lyrics], ignore_index=True)

    def fetch_all_data_from_storage(self):
        try:
            with open(self.__FILE_NAME, "rb") as outfile:
                self.artists_df = pd.read_excel(
                    outfile, index_col=0, sheet_name=Constants.NOME_ABA_ARTISTAS
                )
                self.albums_df = pd.read_excel(
                    outfile, index_col=0, sheet_name=Constants.NOME_ABA_ALBUMS
                )
                self.songs_df = pd.read_excel(
                    outfile, index_col=0, sheet_name=Constants.NOME_ABA_MUSICAS
                )
                self.credits_df = pd.read_excel(
                    outfile, index_col=0, sheet_name=Constants.NOME_ABA_CREDITOS
                )
                self.lyrics_df = pd.read_excel(
                    outfile, index_col=0, sheet_name=Constants.NOME_ABA_LYRICS
                )

                self.albums_artists_df = pd.read_excel(
                    outfile,
                    index_col=0,
                    sheet_name=Constants.NOME_ABA_RELACIONAMENTO_ARTISTA_ALBUM,
                )
                self.songs_artists_df = pd.read_excel(
                    outfile,
                    index_col=0,
                    sheet_name=Constants.NOME_ABA_RELACIONAMENTO_ARTISTA_MUSICA,
                )
        except Exception as error:
            print(error)

    def persist(self, file_name: Optional[str] = None):
        if not file_name:
            file_name = self.__FILE_NAME

        self.__drop_duplicates()

        try:
            with pd.ExcelWriter(file_name) as writer:
                self.artists_df.to_excel(writer, sheet_name=Constants.NOME_ABA_ARTISTAS)
                self.albums_df.to_excel(writer, sheet_name=Constants.NOME_ABA_ALBUMS)
                self.songs_df.to_excel(writer, sheet_name=Constants.NOME_ABA_MUSICAS)
                self.credits_df.to_excel(writer, sheet_name=Constants.NOME_ABA_CREDITOS)
                self.lyrics_df.to_excel(writer, sheet_name=Constants.NOME_ABA_LYRICS)
                self.albums_artists_df.to_excel(
                    writer, sheet_name=Constants.NOME_ABA_RELACIONAMENTO_ARTISTA_ALBUM
                )
                self.songs_artists_df.to_excel(
                    writer, sheet_name=Constants.NOME_ABA_RELACIONAMENTO_ARTISTA_MUSICA
                )
        except Exception as error:
            print(error)

    def __drop_duplicates(self):
        self.artists_df.drop_duplicates(subset=["id"], inplace=True)
        self.albums_df.drop_duplicates(subset=["id"], inplace=True)
        self.songs_df.drop_duplicates(subset=["id"], inplace=True)
        self.credits_df.drop_duplicates(
            subset=["trackUri", "artist_uri", "artist_creator_uri"], inplace=True
        )
        self.lyrics_df.drop_duplicates(subset=["trackUri"], inplace=True)

        self.albums_artists_df.drop_duplicates(
            subset=["album_id", "artist_id"], inplace=True
        )
        self.songs_artists_df.drop_duplicates(
            subset=["track_id", "artist_id"], inplace=True
        )

