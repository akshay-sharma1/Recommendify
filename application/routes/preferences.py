import itertools

from flask import Blueprint, redirect, url_for, render_template, request, session

from application.api import api

# Blueprint configuration
preferences = Blueprint('app_preferences', __name__,
                        template_folder='templates',
                        static_folder='static')


def build_image_url(*args):
    return '/'.join(args)


def get_mood_metadata():
    # assembles data for mood_images
    BASE_URL = 'https://source.unsplash.com'
    image_ids = ['dWIVg59BVXY', 'fnztlIb52gU', 's9CC2SKySJM', 'zfPOelmDc-M']

    image_url_list = []
    for image in image_ids:
        image_url_list.append(build_image_url(BASE_URL, image))

    identifier_list = ['Chill', 'Mood Booster', 'Deep Focus', 'Workout']

    return dict(zip(identifier_list, image_url_list))


def get_top_track_metadata(access_token):
    track_metadata = {}
    top_tracks = api.get_user_top_tracks(access_token, time_range='medium_term', limit=20)['items']

    for track in top_tracks:
        song_name = track['name']
        song_img = track['album']['images'][1]['url']
        artist_name = track['artists'][0]['name']

        track_metadata[song_name] = [song_img, artist_name]

    return track_metadata


def generate_autocomplete(access_token):
    genre_list = api.genre_seeds(access_token)['genres']

    medium_artists = api.get_user_top_artists(access_token, time_range='medium_term', limit=30)['items']
    short_artists = api.get_user_top_artists(access_token, time_range='short_term', limit=30)['items']

    if len(medium_artists) < 8:
        top_artists = short_artists
    else:
        top_artists = medium_artists

    for artist in top_artists:
        for genre in artist['genres']:
            if genre not in genre_list:
                genre_list.append(genre)

    genre_list.sort()
    return genre_list


def clear_session():
    if 'playlist_id' in session:
        session.pop('playlist_id', None)

    if 'requested_mood' in session:
        session.pop('requested_mood', None)
    elif 'requested_track' in session:
        session.pop('requested_track', None)
    else:
        session.pop('requested_genre', None)


def logout():
    # remove token from current session
    session.clear()


@preferences.route('/preferences', methods=["GET", "POST"])
def starter_page():
    clear_session()

    # assembles data for artist_images
    top_track_metadata = get_top_track_metadata(session['token'])
    top_tracks = dict(itertools.islice(top_track_metadata.items(), 8))

    mood_metadata = get_mood_metadata()

    # available genres
    genreList = generate_autocomplete(session['token'])

    if request.method == "GET":
        return render_template("preferences.html", top_track_metadata=top_tracks, mood_metadata=mood_metadata,
                               availableGenres=genreList)

    if request.method == "POST":
        # get from data from the post request (Form)
        result = request.form

        if 'logout_input' in result:
            logout()
            return redirect(url_for('app_home.index'))
        elif 'genreInput' in result:
            session['requested_genre'] = str.lower(result['genreInput'])
        elif 'topTrackInput' in result:
            session['requested_track'] = str.lower(result['topTrackInput'])
        else:
            session['requested_mood'] = str.lower(result['moodInput'])

        return redirect(url_for('app_rec.output_song'))
