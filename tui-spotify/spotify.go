package main

import (
	"fmt"
	"log"
	"net/http"

	"github.com/zmb3/spotify"
	// "golang.org/x/oauth2"
)

var (
	auth  = spotify.NewAuthenticator("http://127.0.0.1:8888/callback", spotify.ScopeUserReadRecentlyPlayed)
	ch    = make(chan *spotify.Client)
	state = "abc123"
)

func startSpotifyAuth(clientID, clientSecret string) *spotify.Client {
	auth.SetAuthInfo(clientID, clientSecret)

	url := auth.AuthURL(state)
	fmt.Println("Please log in to Spotify:\n", url)

	http.HandleFunc("/callback", completeAuth)
	go http.ListenAndServe(":8888", nil)

	client := <-ch
	return client
}

func completeAuth(w http.ResponseWriter, r *http.Request) {
	tok, err := auth.Token(state, r)
	if err != nil {
		http.Error(w, "Auth failed", http.StatusForbidden)
		log.Fatal(err)
	}
	client := auth.NewClient(tok)
	fmt.Fprintf(w, "Login complete. You may close this tab.")
	ch <- &client
}

// hello
func getRecentTracks(client *spotify.Client) []string {
	history, err := client.PlayerRecentlyPlayed()
	if err != nil {
		log.Fatal(err)
	}
	var results []string
	for _, item := range history {
		results = append(results, item.Track.Name+" - "+item.Track.Artists[0].Name)
	}
	return results
}

// Get user playlists
func getUserPlaylists(client *spotify.Client) map[string]spotify.ID {
	playlists := make(map[string]spotify.ID)
	offset := 0
	limit := 50

	for {
		page, err := client.CurrentUsersPlaylistsOpt(&spotify.Options{Limit: &limit, Offset: &offset})
		if err != nil {
			log.Fatal("Error fetching playlists:", err)
		}
		for _, p := range page.Playlists {
			playlists[p.Name] = p.ID
		}
		if len(page.Playlists) < limit {
			break
		}
		offset += limit
	}
	return playlists
}

// Get songs from a playlist
func getTracksFromPlaylist(client *spotify.Client, playlistID spotify.ID) []string {
	var tracks []string
	offset := 0
	limit := 100

	for {
		page, err := client.GetPlaylistTracksOpt(playlistID, &spotify.Options{Limit: &limit, Offset: &offset}, "")
		if err != nil {
			log.Fatal("Error getting playlist tracks:", err)
		}
		for _, item := range page.Tracks {
			tracks = append(tracks, item.Track.Name+" - "+item.Track.Artists[0].Name)
		}
		if len(page.Tracks) < limit {
			break
		}
		offset += limit
	}
	return tracks
}
