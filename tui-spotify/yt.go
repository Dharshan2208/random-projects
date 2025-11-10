package main

import (
	"log"
	"os/exec"
	"strings"
)

func getYoutubeURL(query string) string {
	cmd := exec.Command("yt-dlp", "-f", "bestaudio", "-g", "ytsearch1:"+query)
	out, err := cmd.Output()
	if err != nil {
		log.Fatal("yt-dlp error:", err)
	}
	return strings.TrimSpace(string(out))
}
