import pandas as pd

from typing import Optional


class StorageManager:
    __FILE_NAME = "arquivos/teste.xlsx"

    def __init__(self) -> None:
        self.artists_df = pd.DataFrame()
        self.albums_df = pd.DataFrame()
        self.songs_df = pd.DataFrame()
        self.credits_df = pd.DataFrame()
        self.lyrics_df = pd.DataFrame()

    def save_artists(self, artists):
        new_artists = pd.DataFrame.from_dict(artists)
        self.artists_df = pd.concat([self.artists_df, new_artists], ignore_index=True)

    def save_albums(self, albums):
        new_albums = pd.DataFrame.from_dict(albums)
        self.albums_df = pd.concat([self.albums_df, new_albums], ignore_index=True)

    def save_songs(self, songs):
        new_songs = pd.DataFrame.from_dict(songs)
        self.songs_df = pd.concat([self.songs_df, new_songs], ignore_index=True)

    def save_credits(self, credits):
        new_credits = pd.DataFrame.from_dict(credits)
        self.credits_df = pd.concat([self.credits_df, new_credits], ignore_index=True)

    def save_lyrics(self, lyrics):
        new_lyrics = pd.DataFrame.from_dict(lyrics)
        self.lyrics_df = pd.concat([self.lyrics_df, new_lyrics], ignore_index=True)

    def persist(self, file_name: Optional[str] = None):
        if not file_name:
            file_name = self.__FILE_NAME

        self.__drop_duplicates()
        
        try:
            with pd.ExcelWriter(file_name) as writer:  
                self.artists_df.to_excel(writer, sheet_name='artists')
                self.albums_df.to_excel(writer, sheet_name='albums')
                self.songs_df.to_excel(writer, sheet_name='songs')
                self.credits_df.to_excel(writer, sheet_name='credits')
                self.lyrics_df.to_excel(writer, sheet_name='lyrics')
        except Exception as error:
            print(error)

    def __drop_duplicates(self):
        self.artists_df.drop_duplicates(subset=['id'], inplace=True)
        self.albums_df.drop_duplicates(subset=['id'], inplace=True)
        self.songs_df.drop_duplicates(subset=['id'], inplace=True)
        self.credits_df.drop_duplicates(subset=['id'], inplace=True)
        self.lyrics_df.drop_duplicates(subset=['id'], inplace=True)
        
