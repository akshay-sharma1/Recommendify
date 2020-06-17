import os
import requests
from application.api import api
from flask import Blueprint, redirect, url_for, render_template, request, session


# Blueprint configuration
home = Blueprint('app_home', __name__,
                 template_folder='templates',
                 static_folder='static')

BASE_URL = 'https://accounts.spotify.com'
SCOPE = os.environ.get('SCOPE')
SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = os.environ.get('REDIRECT_URI')
SHOW_DIALOG = True
AUTH_URL = f'{BASE_URL}/authorize?client_id={SPOTIFY_CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={SCOPE}&show_dialog={SHOW_DIALOG}'

def register_user(access_token):
    user_info = api.get_user_profile(access_token)
    session['spotify_id'] = user_info['id']
    session['display_name'] = user_info['display_name']

@home.route('/')
def index():
    return redirect(url_for('app_home.authenticate'))


@home.route('/login', methods=['GET', 'POST'])
def authenticate():
    if request.method == 'GET':
        return render_template('start.html')

    if request.method == 'POST':
        return redirect(AUTH_URL)


@home.route('/api_callback')
def callback():

    session.clear()
    code = request.args.get('code')
    auth_token_endpoint = f'{BASE_URL}/api/token'
    result = requests.post(auth_token_endpoint, data={
        'grant_type': "authorization_code",
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': SPOTIFY_CLIENT_ID,
        'client_secret': SPOTIFY_CLIENT_SECRET
    })

    result_data = result.json()
    session['token'] = result_data.get('access_token')

    if session['token']:
        register_user(session['token'])
        return redirect(url_for('app_preferences.starter_page'))
    else:
        return redirect(url_for('app_home.authenticate'))
