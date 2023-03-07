from config import CLIENT_ID, CLIENT_SECRET

import json
import logging
import os
import requests
import secrets
import string
from urllib.parse import urlencode

# Spotify API endpoints
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
ME_URL = 'https://api.spotify.com/v1/me/top/tracks?limit=15'
AUDIO_URL = 'https://api.spotify.com/v1/audio-features'

scope = 'user-top-read'

auth_response = requests.post(AUTH_URL, {
    'grant_type':'client_credentials',
    'client_id' :CLIENT_ID,
    'client_secret':CLIENT_SECRET
})

auth_response_data = auth_response.json()

access_token = auth_response_data['access_token']

response = requests.get(ME_URL)

