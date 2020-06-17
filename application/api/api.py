import requests
from application.api import util
import json

# Constant variables
SPOTIFY_BASE = 'https://api.spotify.com/v1'


def get_user_profile(access_token):
    url = util.build_url(SPOTIFY_BASE, 'me')
    return requests.get(url, headers=util.create_authorization_header(access_token)).json()


def search(name, access_token, **kwargs):
    url = util.build_url(SPOTIFY_BASE, 'search?') + 'q=' + name + '&'

    for k, v in kwargs.items():
        url += k + '=' + str(v) + '&'
    url = url[:-1]

    return requests.get(url, headers=util.create_authorization_header(access_token)).json()


def get_user_top_artists(access_token, **kwargs):
    url = util.build_url(SPOTIFY_BASE, 'me', 'top', 'artists?')
    for k, v in kwargs.items():
        url += k + "=" + str(v) + '&'
    url = url[:-1]

    return requests.get(url, headers=util.create_authorization_header(access_token)).json()

def get_user_top_tracks(access_token, **kwargs):
    url = util.build_url(SPOTIFY_BASE, 'me', 'top', 'tracks?')

    for k, v in kwargs.items():
        url += k + '=' + str(v) + '&'
    url = url[:-1]

    return requests.get(url, headers=util.create_authorization_header(access_token)).json()

def get_related_artists(access_token, artist_id):
    url = util.build_url(SPOTIFY_BASE, 'artists', artist_id, 'related-artists')
    return requests.get(url, headers=util.create_authorization_header(access_token)).json()


def get_artist_albums(artist_id, access_token, **kwargs):
    url = util.build_url(SPOTIFY_BASE, 'artists', artist_id, 'albums?')

    for k, v in kwargs.items():
        if isinstance(v, list):
            url += k + "=" + ','.join(v) + '&'
        else:
            url += k + '=' + str(v) + '&'

    url = url[:-1]
    return requests.get(url, headers=util.create_authorization_header(access_token)).json()


def get_album_tracks(album_id, access_token, **kwargs):
    url = util.build_url(SPOTIFY_BASE, 'albums', album_id, 'tracks?')

    for k, v in kwargs.items():
        url += k + "=" + str(v) + '&'

    url = url[:-1]
    return requests.get(url, headers=util.create_authorization_header(access_token)).json()


def get_tracks_information(track_ids, access_token):
    url = util.build_url(SPOTIFY_BASE, 'tracks', '?') + 'ids=' + ','.join(track_ids)

    return requests.get(url, headers=util.create_authorization_header(access_token)).json()


def get_artist_top_tracks(artist_id, access_token):
    url = util.build_url(SPOTIFY_BASE, 'artists', artist_id, 'top-tracks?country=US')
    return requests.get(url, headers=util.create_authorization_header(access_token)).json()


def genre_seeds(access_token):
    url = util.build_url(SPOTIFY_BASE, 'recommendations', 'available-genre-seeds')
    return requests.get(url, headers=util.create_authorization_header(access_token)).json()


def seed_recommendations(access_token, **kwargs):
    url = util.build_url(SPOTIFY_BASE, 'recommendations?')

    for k, v in kwargs.items():
        if isinstance(v, list):
            url += k + "=" + ','.join(v) + '&'
        else:
            url += k + "=" + str(v) + '&'

    url = url[:-1]

    return requests.get(url, headers=util.create_authorization_header(access_token)).json()


def create_playlist(user_id, playlist_name, access_token):
    url = util.build_url(SPOTIFY_BASE, 'users', user_id, 'playlists')
    data = {'name': playlist_name, 'public': 'true', 'description': 'created at recommend-ify.herokuapp.com'}
    return requests.post(url, headers=util.create_playlist_header(access_token), data=json.dumps(data)).json()


def add_to_playlist(playlist_id, tracks, access_token):
    url = util.build_url(SPOTIFY_BASE, 'playlists', playlist_id, 'tracks?')
    data = {'uris': tracks}
    return requests.put(url, headers=util.create_playlist_header(access_token), data=json.dumps(data)).json()


def get_playlist_information(playlist_id, access_token):
    url = util.build_url(SPOTIFY_BASE, 'playlists', playlist_id)
    return requests.get(url, headers=util.create_authorization_header(access_token)).json()
