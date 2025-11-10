package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
	"strconv"
	"strings"

	"github.com/joho/godotenv"
)

func main() {
	godotenv.Load()

	clientID := os.Getenv("Client_ID")
	clientSecret := os.Getenv("Client_Secret")
	client := startSpotifyAuth(clientID, clientSecret)

	// Step 1: Get Playlists
	playlists := getUserPlaylists(client)
	playlistNames := make([]string, 0, len(playlists))
	for name := range playlists {
		playlistNames = append(playlistNames, name)
	}
	sort.Strings(playlistNames)

	fmt.Println("🎵 Your Playlists:")
	for i, name := range playlistNames {
		fmt.Printf("%d) %s\n", i+1, name)
	}

	// Step 2: Choose Playlist
	choice := prompt("Enter playlist number: ")
	index, err := strconv.Atoi(choice)
	if err != nil || index < 1 || index > len(playlistNames) {
		fmt.Println("Invalid choice")
		return
	}
	playlistID := playlists[playlistNames[index-1]]

	// Step 3: Fetch Songs
	songs := getTracksFromPlaylist(client, playlistID)
	fmt.Println("🎧 Songs:")
	for i, song := range songs {
		fmt.Printf("%d) %s\n", i+1, song)
	}

	// Step 4: Choose Song
	sel := prompt("Enter song number to play: ")
	songIndex, err := strconv.Atoi(sel)
	if err != nil || songIndex < 1 || songIndex > len(songs) {
		fmt.Println("Invalid song number")
		return
	}
	song := songs[songIndex-1]

	// Step 5: Play
	fmt.Println("🎶 Playing:", song)
	url := getYoutubeURL(song)
	playWithMPV(url)
}

func prompt(msg string) string {
	fmt.Print(msg)
	reader := bufio.NewReader(os.Stdin)
	input, _ := reader.ReadString('\n')
	return strings.TrimSpace(input)
}
