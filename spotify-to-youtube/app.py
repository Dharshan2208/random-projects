import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import CLIENT_ID,CLIENT_SECRET
from youtube import authenticate_youtube, create_youtube_playlist,search_and_add_to_playlist


# Setup authorization
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri="http://127.0.0.1:8888/callback",
    scope="playlist-read-private user-library-read"
))

# Fetch playlists
playlists = sp.current_user_playlists()


# sp.current_user_saved_tracks(limit=50, offset=0)
# limit=50 → max songs per request

# offset=0 → used for pagination

# For Liked Songs
# def get_liked_songs(sp):
#     liked_songs = []
#     limit = 50
#     offset = 0

#     while True:
#         results = sp.current_user_saved_tracks(limit=limit, offset=offset)
#         items = results['items']
#         if not items:
#             break

#         for item in items:
#             track = item['track']
#             name = track['name']
#             artists = ', '.join([artist['name'] for artist in track['artists']])
#             track_id = track['id']
#             liked_songs.append({
#                 'id': track_id,
#                 'name': name,
#                 'artists': artists
#             })

#         offset += limit

#     return liked_songs

# liked_songs = get_liked_songs(sp)

# # print(liked_songs)

# for i, song in enumerate(liked_songs):
#     print(f"{i+1}. {song['name']} — {song['artists']}")

# Collect songs in a list
songs = []


# Show playlist names
for i, playlist in enumerate(playlists['items']):
    print(f"{i + 1}. {playlist['name']}")

choice = int(input("Enter playlist number: ")) - 1
selected_playlist = playlists['items'][choice]
playlist_id = selected_playlist['id']

results = sp.playlist_tracks(playlist_id)

# Get songs from that playlist
for i,item in enumerate(results['items']):
    track = item['track']
    name = track['name']
    artists = ', '.join([artist['name'] for artist in track['artists']])
    songs.append(f"{name} {artists}")
    print(f"{i+1} {name} -- {artists}")


youtube = authenticate_youtube()
yt_playlist_id = create_youtube_playlist(youtube, selected_playlist['name'])
search_and_add_to_playlist(youtube, yt_playlist_id, songs)