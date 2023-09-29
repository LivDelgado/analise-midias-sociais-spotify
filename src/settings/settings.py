import os

class Settings:
    SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
    SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')
    SPOTIFY_GENERIC_CLIENT_ID = os.environ.get('SPOTIFY_GENERIC_CLIENT_ID')
