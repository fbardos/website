from collections import Counter
from typing import List

import spotipy
from spotipy.oauth2 import SpotifyOAuth


class SpotifyApi:

    # Redirect URI needs to be configured in Spotify API dashboard.
    REDIRECT_URI = 'http://127.0.0.1:8080'

    def __init__(self, client_id: str, client_secret: str):
        self._client_id = client_id
        self._client_secret = client_secret

    def _generate_scope(self, *args) -> str:
        return ' '.join(args)

    def _get_tracks_on_playlist(self, client: spotipy.Spotify, playlist_id: str) ->List[dict]:

        # Get information about playlist
        playlist = client.playlist(playlist_id)
        print(f'Found playlist: {playlist["name"]}')

        # Collect all tracks
        response = client.playlist_items(playlist_id)
        tracks = response['items']
        while response['next']:
            response = client.next(response)
            tracks.extend(response['items'])
        print(f'Imported {len(tracks)} tracks.')
        return tracks

    def _get_list_of_following_artists(self, client: spotipy.Spotify) -> List[dict]:
        response = client.current_user_followed_artists()
        following_artists = response['artists']['items']
        while response['artists']['next']:
            response = client.next(response['artists'])
            following_artists.extend(response['artists']['items'])
        print(f'Imported {len(following_artists)} followed artists.')
        return following_artists

    def follow_artists_on_playlist(self, playlist_id: str, min_amount_of_songs: int = 1) -> None:
        """Follows artists on a specific playlist.

        Args:
            playlist_id: ID of playlist
            min_amount_of_songs: Minimum amount of songs from this artists until follow is triggered.

        """
        scope = self._generate_scope(
            'user-follow-read',
            'user-follow-modify',
            'playlist-read-private',
        )
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(self._client_id, self._client_secret, self.REDIRECT_URI, scope=scope))
        tracks = self._get_tracks_on_playlist(sp, playlist_id)

        artists = []
        for track in tracks:
            for artist in track['track']['artists']:
                artists.append((artist['id'], artist['name']))
        artists_counter = Counter(artists)

        # Keep only artists with more than x tracks on playlist
        artists_counter = Counter({k: c for k, c in artists_counter.items() if c >= min_amount_of_songs})

        # Get a list of current artist follows
        list_following_artists = self._get_list_of_following_artists(sp)
        following_artists = [(i['id'], i['name']) for i in list_following_artists]

        # Pop counter elements if already existent
        for artist_id, artist_name in artists_counter.copy():
            if (artist_id, artist_name) in following_artists:
                print(f'Already following {artist_name}. Skip.')
                artists_counter.pop((artist_id, artist_name))

        # Follow filtered artists
        print('========= START FOLLOWING =========')
        for artist_id, artist_name in artists_counter:
            print(f'Start following {artist_name}...')
            sp.user_follow_artists([artist_id])


if __name__ == '__main__':

    # Using 'Client Authorization Code Flow'
    CLIENT_ID = 'xxx'
    CLIENT_SECRET = 'xxx'

    client = SpotifyApi(CLIENT_ID, CLIENT_SECRET)
    client.follow_artists_on_playlist('xxx', 2)
