document.addEventListener('DOMContentLoaded', function () {
    const audioPlayer = document.getElementById("audioPlayer");
    const playPauseButton = document.getElementById("playPause");
    const volumeControl = document.getElementById("volumeControl");

    // Set initial volume
    audioPlayer.volume = volumeControl.value;
    volumeControl.value = audioPlayer.volume;

    playPauseButton.addEventListener("click", function () {
        if (audioPlayer.paused) {
            audioPlayer.play();
            playPauseButton.textContent = "♫";
        } else {
            audioPlayer.pause();
            playPauseButton.textContent = "♫";
        }
    });

    volumeControl.addEventListener("input", function (event) {
        const volume = event.target.value;
        audioPlayer.volume = volume;
    });

    // Update slider value if the volume changes programmatically
    audioPlayer.addEventListener("volumechange", function () {
        volumeControl.value = audioPlayer.volume;
    });
});
