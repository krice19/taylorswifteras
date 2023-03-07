import spotipy
import spotipy.util as util
from config import client_id, client_secret
import pandas as pd

redirect_uri = 'http://localhost:7777/callback'
scope = 'user-top-read'

token = util.prompt_for_user_token(scope=scope, 
client_id=client_id,   
client_secret=client_secret,     
redirect_uri=redirect_uri)

sp = spotipy.Spotify(auth=token)

top_tracks = sp.current_user_top_tracks(limit=15,time_range='long_term')

top_songs =[]
for idx, item in enumerate(top_tracks['items']):
    top_songs.append(item['id'])

features = []
for id in top_songs:
    features.append(sp.audio_features(id))


song_count = len(top_songs)
dance = []
energy = []
key = []
loud = []
mode = []
speech = []
acoustic = []
instrument = []
liveness = []
valence = []
tempo = []

for i in range(song_count):
    dance.append(features[i][0]["danceability"])
    energy.append(features[i][0]["energy"])
    key.append(features[i][0]["key"])
    loud.append(features[i][0]["loudness"])
    mode.append(features[i][0]["mode"])
    speech.append(features[i][0]["speechiness"])
    acoustic.append(features[i][0]["acousticness"])
    instrument.append(features[i][0]["instrumentalness"])
    liveness.append(features[i][0]["liveness"])
    valence.append(features[i][0]["valence"])
    tempo.append(features[i][0]["tempo"])

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

df_data = {'Albums': ["Taylor Swift",
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
print("You are " + name + " era!")