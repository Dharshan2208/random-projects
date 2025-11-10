package main

import (
	"os"
	"os/exec"
)

func playWithMPV(url string) {
	cmd := exec.Command("mpv", "--no-video", url)
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	cmd.Run()
}
