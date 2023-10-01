class SpotifyEndpoints:
    GENERATE_CLIENT_TOKEN_URL = "https://accounts.spotify.com/api/token"
    PRIVATE_CLIENT_TOKEN_URL = "https://clienttoken.spotify.com/v1/clienttoken"
    SPOTIFY_BASE_URL = "https://api.spotify.com/v1/"
    GENERATE_AUTH_URL = "https://open.spotify.com/get_access_token"
    CSRF_URL = "https://www.spotify.com/us/signup"
    
    SEARCH = "search"
    PLAYLIST_ITEMS = "playlists/{playlist_id}/tracks"
    ARTIST_ALBUMS = "artists/{artist_id}/albums"
    ALBUM_TRACKS = "albums/{album_id}/tracks"