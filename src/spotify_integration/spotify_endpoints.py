class SpotifyEndpoints:
    GENERATE_CLIENT_TOKEN_URL = "https://accounts.spotify.com/api/token"
    PRIVATE_CLIENT_TOKEN_URL = "https://clienttoken.spotify.com/v1/clienttoken"
    SPOTIFY_BASE_URL = "https://api.spotify.com/v1/"
    GENERATE_AUTH_URL = "https://open.spotify.com/get_access_token"
    CSRF_URL = "https://www.spotify.com/us/signup"
    PLAYER_BASE_URL = "https://spclient.wg.spotify.com/"

    CREDITS_URL = "https://spclient.wg.spotify.com/track-credits-view/v0/experimental/{track_id}/credits"

    SEARCH = "search"
    PLAYLIST_ITEMS = "playlists/{playlist_id}/tracks?fields=items(track(name,id,href,album(name,href, id),artists(name,id,href,type)))"
    ARTIST_ALBUMS = "artists/{artist_id}/albums"
    ALBUM_TRACKS = "albums/{album_id}/tracks"
    LYRICS = "color-lyrics/v2/track/{track_id}"
