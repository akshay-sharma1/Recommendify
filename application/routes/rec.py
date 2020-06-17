import itertools
import random

from flask import Blueprint, redirect, url_for, render_template, request, session

from application.api import api
from application.recommendations import recommend_genre, recommend_mood, recommend_track

rec = Blueprint('app_rec', __name__,
                template_folder='templates',
                static_folder='static')


# HELPERS
def pass_search(requested_track, access_token):
    # search for the track to get its id
    track_id = api.search(requested_track, access_token, type='track', limit=2)['tracks']['items'][0]['id']

    # search for the artist_id based on the track
    artist_id = api.get_tracks_information([track_id], access_token)['tracks'][0]['artists'][0]['id']

    return track_id, artist_id


def create_playlist(tracks, access_token):

    if 'requested_genre' in session:
        playlist_name = session['requested_genre'].title()
    elif 'requested_track' in session:
        playlist_name = "Your Recommended Playlist"
    else:
        playlist_name = session['requested_mood'].title()

    created_playlist_id = api.create_playlist(session['spotify_id'], playlist_name, access_token)['id']
    api.add_to_playlist(created_playlist_id, tracks, access_token)

    return created_playlist_id


def get_playlist_info(playlist_id, access_token):
    # get playlist metadata
    playlist_metadata = api.get_playlist_information(playlist_id, access_token)

    playlist_name = playlist_metadata['name']
    playlist_image = playlist_metadata['images'][0]['url']
    playlist_url = playlist_metadata['external_urls']['spotify']

    return playlist_name, playlist_image, playlist_url


def logout():
    # remove token from current session
    session.clear()


@rec.route("/playlist", methods=['GET', 'POST'])
def output_song():

    if 'requested_mood' in session:
        song_metadata, track_uris = recommend_mood(session['requested_mood'], session['token'])
    elif 'requested_track' in session:
        track_id, artist_id = pass_search(session['requested_track'], session['token'])
        song_metadata, track_uris = recommend_track(track_id, artist_id, session['token'])
    else:
        song_metadata, track_uris = recommend_genre(session['requested_genre'], session['token'])

    # shuffle the song_metadata here
    song_keys = list(song_metadata.keys())
    random.shuffle(song_keys)

    shuffled_metadata = dict()
    for key in song_keys:
        shuffled_metadata.update({key: song_metadata[key]})

    shuffled_metadata = dict(itertools.islice(shuffled_metadata.items(), 10))

    # shuffle track_uris
    random.shuffle(track_uris)

    if request.method == 'GET':
        return render_template('rec.html', data=shuffled_metadata)

    if request.method == 'POST':
        result = request.form
        if 'logout_input' in result:
            logout()
            return redirect(url_for('app_home.index'))
        else:
            created_playlist_id = create_playlist(track_uris, session['token'])
            session['playlist_id'] = created_playlist_id
            return redirect(url_for('app_rec.display_confirmation'))


@rec.route('/confirmation', methods=['GET', 'POST'])
def display_confirmation():
    if request.method == 'GET':
        playlist_name, playlist_img, playlist_url = get_playlist_info(session['playlist_id'], session['token'])
        return render_template('confirmation.html', imgName=playlist_img, playlistName=playlist_name, previewUrl=playlist_url)

    if request.method == 'POST':
        result = request.form
        if 'logout_input' in result:
            logout()
            return redirect(url_for('app_home.index'))
