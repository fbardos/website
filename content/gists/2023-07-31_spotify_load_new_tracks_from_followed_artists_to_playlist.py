"""

This Python script will check for newly added tracks from artists you follow on
spotify. It then creates a playlist and adds all these newly added tracks to
this playlist.

Config Options (see bottom):
- CLIENT_ID and CLIENT_SECRET:
    Are needed for API calls. Register an app at http://developer.spotify.com
    and add ID and SECRET to these lines.
- SpotifyApi.put_new_tracks_in_playlist_from_followed_artists(lookback_days=90)
    lookback_days specifies, how many days to look back for new tracks.

"""
import datetime as dt
import logging
from typing import Callable, List, Optional, Set

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from tqdm import tqdm


class SpotifyApi:

    # Redirect URI needs to be configured in Spotify API dashboard.
    REDIRECT_URI = 'http://127.0.0.1:8080'

    def __init__(self, client_id: str, client_secret: str):
        self._client_id = client_id
        self._client_secret = client_secret
        self._client = None

    def _get_dict_response(self, api_method: Callable, **kwargs) -> dict:
        """Asserts that returned API calls contains a dictionary and is not empty."""
        response = api_method(**kwargs)
        assert isinstance(response, dict)
        return response

    @property
    def client(self) -> spotipy.Spotify:
        assert isinstance(self._client, spotipy.Spotify)
        return self._client

    @property
    def followed_artists(self) -> List[dict]:
        """Returns a list of followed artists by the user."""
        response = self._get_dict_response(self.client.current_user_followed_artists)
        artists = response['artists']['items']
        while response['artists']['next']:
            response = self._get_dict_response(self.client.next, result=response['artists'])
            artists.extend(response['artists']['items'])
        logging.info(f'Imported {len(artists)} artists.')
        return artists

    def connect(self):
        """Init a spotipy.Spotify client."""
        scope = ' '.join((
            'user-follow-read',
            'user-follow-modify',
            'playlist-read-private',
            'playlist-modify-private',
        ))
        self._client = spotipy.Spotify(
            auth_manager=SpotifyOAuth(self._client_id, self._client_secret, self.REDIRECT_URI, scope=scope)
        )

    def get_tracks_from_artist(self, artist_id: str, release_after: Optional[dt.datetime] = None) -> Set[dict]:
        """Loads all tracks from an artist (no compilations). Returns a list of track URIs"""

        # First, get all albums, later extract the tracks
        response = self._get_dict_response(self.client.artist_albums, artist_id=artist_id, album_type=['album', 'single', 'appears_on'])
        albums = response['items']
        while response['next']:
            response = self._get_dict_response(self.client.next, result=response)
            albums.extend(response['items'])

        # Filter albums by release date when release_after is set
        if release_after:
            albums_filtered = []
            for album in albums:
                match album['release_date_precision']:
                    case 'year':
                        if dt.datetime.strptime(album['release_date'], '%Y') > release_after:
                            albums_filtered.append(album)
                    case 'day':
                        if dt.datetime.strptime(album['release_date'], '%Y-%m-%d') > release_after:
                            albums_filtered.append(album)
        else:
            albums_filtered = albums

        # Then load all tracks from the albums
        tracks = []
        for album in albums_filtered:
            response = self._get_dict_response(self.client.album_tracks, album_id=album['id'])
            album_tracks = response['items']
            while response['next']:
                response = self._get_dict_response(self.client.next, result=response)
                album_tracks.extend(response['items'])
            tracks.extend(album_tracks)

        # Filter tracks and keep only tracks from the current artist
        def _extract_artist_ids_from_track(track: dict) -> bool:
            track_artists = [artist['id'] for artist in track['artists']]
            return True if artist_id in track_artists else False

        tracks = [track for track in tracks if _extract_artist_ids_from_track(track)]

        # Clean duplicate tracks
        distinct_tracks = set([track['uri'] for track in tracks])
        logging.info(f'Imported {len(distinct_tracks)} tracks.')

        return distinct_tracks

    def put_new_tracks_in_playlist_from_followed_artists(
        self,
        lookback_days: int = 7,
    ):
        """Loads tracks into a newly created playlist.

        Args:
            - lookback_days: Specifies, how many days to look back for new tracks.

        """
        now = dt.datetime.now()
        release_after = now - dt.timedelta(days=lookback_days)
        artists = self.followed_artists
        tracks = []

        for artist in (pbar := tqdm(artists, desc='Loading tracks from followed artists')):
            artist_info = self._get_dict_response(self.client.artist, artist_id=artist['id'])
            pbar.set_description(f"Get tracks for {artist_info['name'][:25].ljust(25, ' ')}")
            artist_tracks = self.get_tracks_from_artist(artist['id'], release_after=release_after)
            tracks.extend(artist_tracks)

        # Assert again tracks are unique (for features)
        tracks = list(set(tracks))

        # Create a new playlist
        user = self._get_dict_response(self.client.me)
        playlist = self._get_dict_response(
            self.client.user_playlist_create,
            user=user.get('id', None),
            name=f'_FRESH_TRACKS_t-{lookback_days}d_{now.isoformat()}',
            public=False,
        )

        # Load tracks to this newly created playlist
        # But split the tracks in multiple chunks
        PAGE_SIZE = 50
        for i in tqdm(range(0, len(tracks), PAGE_SIZE), desc=f'Add tracks to playlist in pages of {PAGE_SIZE}'):
            self.client.playlist_add_items(playlist['id'], items=tracks[i:i+PAGE_SIZE])



if __name__ == '__main__':

    # Using 'Client Authorization Code Flow'
    CLIENT_ID = 'xxx'
    CLIENT_SECRET = 'xxx'

    client = SpotifyApi(CLIENT_ID, CLIENT_SECRET)
    client.connect()
    client.put_new_tracks_in_playlist_from_followed_artists(lookback_days=90)
