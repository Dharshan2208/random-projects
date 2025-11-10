import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
from google.auth.transport.requests import Request

import pickle

scopes = ["https://www.googleapis.com/auth/youtube"]
TOKEN_PATH = "token.pickle"
scopes = ["https://www.googleapis.com/auth/youtube"]


def authenticate_youtube():
    creds = None

    # Try loading saved credentials
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, "rb") as token_file:
            creds = pickle.load(token_file)

    # If credentials are not valid, do login or refresh
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                "credentials.json", scopes)
            creds = flow.run_local_server(port=0)

        # Save the credentials for next time
        with open(TOKEN_PATH, "wb") as token_file:
            pickle.dump(creds, token_file)

    # Build YouTube client
    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=creds)
    return youtube

# def authenticate_youtube():

#     creds = None


#     flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
#         "credentials.json", scopes)
#     credentials = flow.run_local_server(port=0)
#     youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)
#     return youtube

# Call this once
# youtube = authenticate_youtube()

def create_youtube_playlist(youtube, title, description=""):
    request = youtube.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description
            },
            "status": {
                "privacyStatus": "private"  # 'public' or 'unlisted'
            }
        }
    )
    response = request.execute()
    print(f"Created YouTube playlist: {title}")
    return response["id"]  # return playlist ID

def search_and_add_to_playlist(youtube, playlist_id, songs):
    for song in songs:
        print(f"🔍 Searching: {song}")
        search_response = youtube.search().list(
            q=song,
            part="snippet",
            maxResults=1,
            type="video"
        ).execute()

        if search_response['items']:
            video_id = search_response['items'][0]['id']['videoId']
            print(f"🎵 Found: https://youtube.com/watch?v={video_id}")

            # Add to playlist
            youtube.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": playlist_id,
                        "resourceId": {
                            "kind": "youtube#video",
                            "videoId": video_id
                        }
                    }
                }
            ).execute()
            print("Added to playlist\n")
        else:
            print("No result found\n")

