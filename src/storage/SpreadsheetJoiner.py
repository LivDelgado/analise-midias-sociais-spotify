from storage.storage_manager import StorageManager

from storage.constants import Constants


import pandas as pd


class SpreadsheetJoiner:
    def __init__(self):
        self.__FILE_NAME = (
            f"arquivos/main_artists_dividida/coleta_top_artists_joined.xlsx"
        )

        self.artists_df = pd.DataFrame()
        self.albums_df = pd.DataFrame()
        self.songs_df = pd.DataFrame()
        self.credits_df = pd.DataFrame()
        self.lyrics_df = pd.DataFrame()

        self.albums_artists_df = pd.DataFrame()
        self.songs_artists_df = pd.DataFrame()

        self._storage_manager_1 = StorageManager(1)
        self._storage_manager_2 = StorageManager(2)
        self._storage_manager_3 = StorageManager(3)
        self._storage_manager_4 = StorageManager(4)
        self._storage_manager_5 = StorageManager(5)
        self._storage_manager_6 = StorageManager(6)

        self._storage_managers = [
            StorageManager(1),
            StorageManager(2),
            StorageManager(3),
            StorageManager(4),
            StorageManager(5),
            StorageManager(6),
        ]

    def persist_in_single_spreadsheet(self):
        self.__join_spreadsheets()
        try:
            with pd.ExcelWriter(self.__FILE_NAME) as writer:
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

    def __join_spreadsheets(self):
        for manager in self._storage_managers:
            self.artists_df = pd.concat([self.artists_df, manager.artists_df], ignore_index=True)
            self.albums_df = pd.concat([self.albums_df, manager.albums_df], ignore_index=True)
            self.songs_df = pd.concat([self.songs_df, manager.songs_df], ignore_index=True)
            self.credits_df = pd.concat([self.credits_df, manager.credits_df], ignore_index=True)
            self.lyrics_df = pd.concat([self.lyrics_df, manager.lyrics_df], ignore_index=True)
            self.albums_artists_df = pd.concat([self.albums_artists_df, manager.albums_artists_df], ignore_index=True)
            self.songs_artists_df = pd.concat([self.songs_artists_df, manager.songs_artists_df], ignore_index=True)
        
        self.artists_df.drop_duplicates()
        self.albums_df.drop_duplicates()
        self.songs_df.drop_duplicates()
        self.credits_df.drop_duplicates()
        self.lyrics_df.drop_duplicates()
        self.albums_artists_df.drop_duplicates()
        self.songs_artists_df.drop_duplicates()
