## Youtube-Spotify Playlist Converter

This Python app allows you to select any of your Spotify playlists and automatically recreate it as a private playlist on YouTube — by searching for and adding matching songs.

## 🚀 Features

- Authenticate and access your Spotify playlists.
- Search for equivalent tracks on YouTube.
- Automatically create a new YouTube playlist with matching songs.
- Saves login credentials (token) for reuse across sessions.

## 🛠 Requirements

- Python 3.7+
- Spotify Developer Credentials
- YouTube Data API Credentials

### 📦 Install Dependencies

```bash
pip install spotipy google-auth google-auth-oauthlib google-api-python-client
```

## 🔑 Setup

### 1. Spotify API Setup

- Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
- Create an app and note your `Client ID` and `Client Secret`.
- Add the redirect URI: `http://127.0.0.1:8888/callback`

Create a `.env` file in your root directory with:

```
CLIENT_ID=your_spotify_client_id
CLIENT_SECRET=your_spotify_client_secret
```

Make sure `config.py` uses `dotenv` like this:

```python
from dotenv import load_dotenv
import os

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
```

### 2. YouTube API Setup

- Go to [Google Cloud Console](https://console.developers.google.com/)
- Create a project and enable **YouTube Data API v3**
- Set up OAuth 2.0 credentials for a **Desktop App**
- Download the `credentials.json` file and place it in your project root

## 📂 Project Structure

```
.
├── app.py                  # Main script for Spotify to YouTube conversion
├── youtube.py              # YouTube auth and playlist functions
├── config.py               # Loads credentials from .env
├── .env                    # Your secret Spotify credentials (not committed to Git)
├── token.pickle            # Auto-saved YouTube auth token (generated)
├── credentials.json        # YouTube OAuth credentials
└── README.md
```

## ▶️ How to Use

1. Run the script:

```bash
python app.py
```

2. Select the Spotify playlist you want to convert.
3. A new private playlist will be created on your YouTube with matched songs.

## ⚠️ Notes

- Not all Spotify songs may perfectly match YouTube videos.
- Only the first search result on YouTube is added (usually the best match).
- Created YouTube playlists are set to private by default.
- Dont use to many times as the youtube api will get maxed out.

## 🙏 Credits

- This is a personal project built using help from various YouTube tutorials and online resources.
