''' Example of Spotify authorization code flow (refreshable user auth).

Displays profile information of authenticated user and access token
information that can be refreshed by clicking a button.

Basic flow:
    -> '/'
    -> Spotify login page
    -> '/callback'
    -> get tokens
    -> use tokens to access API

Required environment variables:
    FLASK_APP, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, SECRET_KEY

More info:
    https://developer.spotify.com/documentation/general/guides/authorization-guide/#authorization-code-flow

'''

from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, SECRET_KEY

from flask import (
    abort,
    Flask,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
import json
import logging
import os
import requests
import secrets
import string
from urllib.parse import urlencode
import pandas as pd



logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG
)


# Client info
CLIENT_ID = CLIENT_ID
CLIENT_SECRET = CLIENT_SECRET
REDIRECT_URI = REDIRECT_URI
SECRET_KEY = SECRET_KEY


# Spotify API endpoints
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
ME_URL = 'https://api.spotify.com/v1/me/top/tracks?limit=50&time_range=long_term'
AUDIO_URL = 'https://api.spotify.com/v1/audio-features?ids='


# Start 'er up
app = Flask(__name__)
app.secret_key = SECRET_KEY




@app.route('/')
def index():

    return render_template('index2.html')


@app.route('/<loginout>')
def login(loginout):
    '''Login or logout user.

    Note:
        Login and logout process are essentially the same. Logout forces
        re-login to appear, even if their token hasn't expired.
    '''

    # redirect_uri can be guessed, so let's generate
    # a random `state` string to prevent csrf forgery.
    state = ''.join(
        secrets.choice(string.ascii_uppercase + string.digits) for _ in range(16)
    )

    # Request authorization from user
    scope = 'user-top-read'

    if loginout == 'logout':
        payload = {
            'client_id': CLIENT_ID,
            'response_type': 'code',
            'redirect_uri': REDIRECT_URI,
            'state': state,
            'scope': scope,
            'show_dialog': True,
        }
    elif loginout == 'login':
        payload = {
            'client_id': CLIENT_ID,
            'response_type': 'code',
            'redirect_uri': REDIRECT_URI,
            'state': state,
            'scope': scope,
        }
    else:
        abort(404)

    res = make_response(redirect(f'{AUTH_URL}/?{urlencode(payload)}'))
    res.set_cookie('spotify_auth_state', state)

   

    return res


@app.route('/callback')
def callback():
    error = request.args.get('error')
    code = request.args.get('code')
    state = request.args.get('state')
    stored_state = request.cookies.get('spotify_auth_state')

    # Check state
    if state is None or state != stored_state:
        app.logger.error('Error message: %s', repr(error))
        app.logger.error('State mismatch: %s != %s', stored_state, state)
        abort(400)

    # Request tokens with code we obtained
    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
    }

    # `auth=(CLIENT_ID, SECRET)` basically wraps an 'Authorization'
    # header with value:
    # b'Basic ' + b64encode((CLIENT_ID + ':' + SECRET).encode())
    res = requests.post(TOKEN_URL, auth=(CLIENT_ID, CLIENT_SECRET), data=payload)

    
    # convert the response to JSON
    res_data = res.json()

    # save the access token
    #access_token = res_data.get('access_token')
    #res_data = res.json()

    if res_data.get('error') or res.status_code != 200:
        app.logger.error(
            'Failed to receive token: %s',
            res_data.get('error', 'No error information received.'),
        )
        abort(res.status_code)

    # Load tokens into session
    session['tokens'] = {
        'access_token': res_data.get('access_token'),
        'refresh_token': res_data.get('refresh_token'),
    }

    return redirect(url_for('me'))


@app.route('/refresh')
def refresh():
    '''Refresh access token.'''

    payload = {
        'grant_type': 'refresh_token',
        'refresh_token': session.get('tokens').get('refresh_token'),
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    res = requests.post(
        TOKEN_URL, auth=(CLIENT_ID, CLIENT_SECRET), data=payload, headers=headers
    )
    res_data = res.json()

    # Load new token into session
    session['tokens']['access_token'] = res_data.get('access_token')

    return json.dumps(session['tokens'])


@app.route('/me')
def me():
    '''Get profile info as a API example.'''

    # Check for tokens
    if 'tokens' not in session:
        app.logger.error('No tokens in session.')
        abort(400)

    # Get profile info
    headers = {'Authorization': f"Bearer {session['tokens'].get('access_token')}"}

    #headers = {'Authorization': 'Bearer {token}'.format(token=access_token)
               


    res = requests.get(ME_URL, headers=headers)
    app.logger.info(f"Status Code {res.status_code}")
    app.logger.info(f"Status Code {res.headers}")
    app.logger.info(f"Status Code {res.text}")
    top_tracks = res.json()
    

    if res.status_code != 200:
        app.logger.error(
            'Failed to get profile info: %s',
            top_tracks.get('error', 'No error message returned.'),
        )
        abort(res.status_code)


    '''
    #top_songs =[]
    #for idx, item in enumerate(top_tracks['items']):
         #top_songs.append(item['id'])

    #song_count = len(top_songs)

    #top_songs_names = []
    #for idx, item in enumerate(top_tracks['items']):
        #top_songs_names.append(item['name'])

    #top_songs_string = ', '.join(top_songs_names)

    #id_string = ','.join(top_songs)

    #url = AUDIO_URL+id_string

    #response = requests.get(url, headers=headers)
    #audio_features = response.json()

    #dance = []
    #energy = []
    #key = []
    #loud = []
    #mode = []
    #speech = []
    #acoustic = []
    #instrument = []
    #liveness = []
    #valence = []
    #tempo = []
    '''


    """
    for idx, item in enumerate(audio_features['audio_features']):
        dance.append(item["danceability"])
        energy.append(item["energy"])
        key.append(item["key"])
        loud.append(item["loudness"])
        mode.append(item["mode"])
        speech.append(item["speechiness"])
        acoustic.append(item["acousticness"])
        instrument.append(item["instrumentalness"])
        liveness.append(item["liveness"])
        valence.append(item["valence"])
        tempo.append(item["tempo"])

    song_dict = dict(danceability=dance, 
                    energy =energy,
                    key =key,
                    loudness=loud,  
                    mode=mode,
                    speechiness=speech,
                    acousticness=acoustic,
                    instrumentalness=instrument,
                    liveness=liveness,
                    valence=valence,
                    tempo=tempo)

    song_df = pd.DataFrame(song_dict)

    top_songs_means = song_df[["danceability","energy","key","loudness",
        "mode","speechiness","acousticness",
        "instrumentalness","liveness","valence","tempo"]].mean()
    top_mean = top_songs_means.mean()

    ts_mean = 11.800125012121212
    fr_mean = 12.051548975419582
    sp_mean = 12.964633383051945
    rd_mean = 11.325443456060606
    e9_mean = 11.426378996083917
    rp_mean = 11.37416730771717
    lv_mean = 10.85594381328283
    fk_mean = 10.274035654943182
    ev_mean = 10.558981043212121
    md_mean = 10.680990369545453

    df_data = {'Albums': ["Taylor Swift Debut",
                        "Fearless",
                        "Speak Now", 
                        "Red",
                        "1989", 
                        "Reputation",
                        "Lover",
                        "Folklore",
                        "Evermore", 
                        "Midnights"],
            'Means': [ts_mean, 
                        fr_mean,
                        sp_mean,
                        rd_mean,
                        e9_mean,
                        rp_mean,
                        lv_mean,
                        fk_mean,
                        ev_mean,
                        md_mean]}

    df = pd.DataFrame(data=df_data)

    df["My Top Mean"] = top_mean

    df["Difference"] = df["Means"] - df["My Top Mean"]

    df["Minimum"] = df["Difference"].abs()

    smallest = df.nsmallest(1, 'Minimum')
    name = smallest['Albums'].to_string(index=False)
    result = "You are " + name + " era! Your top songs are:" + top_songs_string
    """

    output_dict = [x for x in top_tracks["items"] if x['artists'][0]['name'] == 'Taylor Swift' and x['album']['album_type'] == 'ALBUM']

    result = output_dict[0]["album"]['name']

    song_name = output_dict[0]['name']


    if result == 'Midnights (The Til Dawn Edition)' or result == 'Midnights (3am Edition)' or result =='Midnights':
        era_name = "Midnights"
    elif result == "Red (Taylor's Version)" or result == 'Red' or result == "Red (Deluxe Edition)":
        era_name = "Red"
    elif result == "Fearless (Taylor's Version)" or result == 'Fearless' or result == "Fearless Platinum Edition":
        era_name = "Fearless"
    elif result == "evermore (deluxe version)" or result == 'evermore':
        era_name = "evermore"
    elif result == "folklore: the long pond studio sessions (from the Disney+ special) [deluxe edition]" or result == 'folklore (deluxe version)' or result == "folklore":
        era_name = "folklore"
    elif result == "Lover":
        era_name = "Lover"
    elif result == "reputation" or result == 'reputation Stadium Tour Surprise Song Playlist':
        era_name = "reputation"
    elif result == "1989 (Taylor's Version)" or result == '1989' or result == "1989 (Deluxe Edition)":
        era_name = "1989"
    elif result == "Speak Now (Taylor's Version)" or result == "Speak Now" or result == "Speak Now (Deluxe Edition)" or result == "Speak Now World Tour Live":
        era_name = "Speak Now"
    elif result == "Taylor Swift" or result == 'Live From Clear Channel Stripped 2008':
        era_name = "Taylor Swift Debut"
    else:
        era_name = "UH OH, you need to listen to more Taylor Swift"


    return render_template('me.html', result=era_name, tokens=session.get('tokens'))

