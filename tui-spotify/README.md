# Tui-song-player

`tui-song-player` is a command-line application written in Go that allows you to browse your Spotify playlists, select a song, and play its audio via YouTube using `yt-dlp` and `mpv`.

## Features

- **Spotify Integration**: Authenticate with your Spotify account to access your playlists.
- **Playlist Selection**: View a list of your Spotify playlists and choose one to browse.
- **Song Selection**: Select a song from the chosen playlist.
- **YouTube Playback**: Automatically fetches the audio stream from YouTube using `yt-dlp` and plays it with `mpv`.

## Prerequisites

Before running `tui-song-player`, you need to have the following installed:

- **Go**: The Go programming language (version 1.24.5 or higher).
- **yt-dlp**: A command-line program to download videos from YouTube and other video sites.
- **mpv**: A free, open-source, and cross-platform media player.

You can install `yt-dlp` and `mpv` using your system's package manager. For example:

**Debian/Ubuntu:**
```bash
sudo apt update
sudo apt install yt-dlp mpv
```

**macOS (using Homebrew):**
```bash
brew install yt-dlp mpv
```

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Dharshan2208/tui-song-player.git
   cd tui-song-player
   ```

2. **Create a Spotify Developer Application:**
   - Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications).
   - Log in and click "Create an app".
   - Fill in the details (App name, App description).
   - After creating the app, you will get a `Client ID` and `Client Secret`.
   - Click "Edit Settings" for your app and add `http://127.0.0.1:8888/callback` as a Redirect URI.

3. **Create a `.env` file:**
   In the root directory of the project, create a file named `.env` and add your Spotify `Client ID` and `Client Secret`:

   ```
   Client_ID=YOUR_SPOTIFY_CLIENT_ID
   Client_Secret=YOUR_SPOTIFY_CLIENT_SECRET
   ```

4. **Install Go dependencies:**
   ```bash
   go mod tidy
   ```

## Usage

1. **Run the application:**
   ```bash
   go run main.go spotify.go player.go yt.go
   ```

2. **Authenticate with Spotify:**
   The application will print a URL in your terminal. Open this URL in your web browser to log in to Spotify and grant permissions to the application. After successful authentication, you can close the browser tab.

3. **Select a playlist and song:**
   Follow the prompts in the terminal to choose a playlist and then a song to play.

## Project Structure

- `main.go`: The entry point of the application, handles user interaction and orchestrates the workflow.
- `spotify.go`: Contains functions for Spotify authentication, fetching user playlists, and retrieving tracks from a playlist.
- `player.go`: Contains the `playWithMPV` function responsible for playing audio using the `mpv` media player.
- `yt.go`: Contains the `getYoutubeURL` function which uses `yt-dlp` to fetch the audio stream URL for a given song query.

## Dependencies

- `github.com/joho/godotenv`: For loading environment variables from a `.env` file.
- `github.com/zmb3/spotify`: A Go client library for the Spotify Web API.
- `golang.org/x/oauth2`: Go's OAuth2 library (indirectly used by `github.com/zmb3/spotify`).

## Development Status

This project is currently under active development, and I will be working on improvements and new features. Feedback and contributions are welcome!

## Contributing

Feel free to fork the repository, open issues, or submit pull requests.
