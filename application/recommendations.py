from application.api import api
import random


def get_artist_catalog(genre, access_token):
    artist_catalog = []

    short_term_artists = api.get_user_top_artists(access_token, time_range='short_term', limit=20)['items']
    medium_term_artists = api.get_user_top_artists(access_token, time_range='medium_term', limit=30)['items']
    long_term_artists = api.get_user_top_artists(access_token, time_range='short_term', limit=30)['items']

    top_artists = [medium_term_artists, long_term_artists, short_term_artists]

    for top_artist in top_artists:
        for artist in top_artist:
            if genre in artist['genres'] and artist['id'] not in artist_catalog:
                artist_catalog.append(artist['id'])
    return artist_catalog


def parse_api_response(track_catalog):
    song_metadata = {}
    track_uri = []

    artist = None
    album_cover = None

    if track_catalog:
        for track in track_catalog['tracks']:
            song = track['name']
            track_href = track['external_urls']['spotify']

            if track['uri'] not in track_uri:
                track_uri.append(track['uri'])

            for album in track['album']['artists']:
                artist = album['name']

            for album in track['album']['images']:
                if album['height'] == 300:
                    album_cover = album['url']

            song_metadata[song] = [artist, album_cover, track_href]

    return song_metadata, track_uri


def recommend_genre(genre, access_token):
    artist_catalog = get_artist_catalog(genre, access_token)
    if artist_catalog:
        random.shuffle(artist_catalog)
        if len(artist_catalog) > 5:
            track_catalog = api.seed_recommendations(access_token, seed_artists=artist_catalog[:5],
                                                     limit=30)
        else:
            track_catalog = api.seed_recommendations(access_token, seed_artists=artist_catalog,
                                                     limit=30)
    else:
        track_catalog = api.seed_recommendations(access_token, seed_genres=[genre], limit=30)

    return parse_api_response(track_catalog)


def recommend_mood(mood, access_token):
    # Conditional if statements
    if mood == 'chill':
        tgt_valence = 0.6
        tgt_energy = 0.2
        target_genres = ['chill', 'pop']
    elif mood == 'mood booster':
        tgt_valence = 0.8
        tgt_energy = 0.5
        target_genres = ['pop', 'happy']
    elif mood == 'deep focus':
        tgt_valence = 0.6
        tgt_energy = 0.2
        target_genres = ['study', 'classical']
    else:
        tgt_valence = 0.7
        tgt_energy = 0.8
        target_genres = ['work-out', 'pop', 'hip-hop']

    track_catalog = api.seed_recommendations(access_token, seed_genres=target_genres,
                                             target_valence=tgt_valence,
                                             target_energy=tgt_energy, limit=30)
    return parse_api_response(track_catalog)


# methods for creating by top track

def get_artist_top_tracks(artist_id, access_token):
    top_tracks = api.get_artist_top_tracks(artist_id, access_token)
    return top_tracks


def get_related_artist_catalog(artist_id, access_token):
    artist_ids = [artist_id]

    related_artists = api.get_related_artists(access_token, artist_id)['artists']

    related_artists = sorted(related_artists, key=lambda x: x['popularity'], reverse=True)
    min_popularity = related_artists[len(related_artists) - 1]['popularity']

    related_artists = related_artists[:3]

    for artist in related_artists:
        if artist['id'] not in artist_ids:
            artist_ids.append(artist['id'])

    return artist_ids, min_popularity


def recommend_track(top_track, artist_id, access_token):
    top_tracks = get_artist_top_tracks(artist_id, access_token)

    related_artist_ids, min_popularity = get_related_artist_catalog(artist_id, access_token)

    track_catalog = api.seed_recommendations(access_token, seed_tracks=[top_track], seed_artists=related_artist_ids,
                                             min_popularity=min_popularity, limit=20)
    track_ids = []

    for track in track_catalog['tracks']:
        if track['id'] not in track_ids:
            track_ids.append(track['id'])

    for track in top_tracks['tracks']:
        if track['id'] not in track_ids:
            track_catalog['tracks'].append(track)

    return parse_api_response(track_catalog)
