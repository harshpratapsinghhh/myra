from actions.music_player import (
    play_music,
    pause_music,
    resume_music,
    next_music,
    previous_music
)
from output.speaker import speak


def play_music_action(song_name):
    play_music(speak, song_name)

def pause_music_action():
    pause_music(speak)

def resume_music_action():
    resume_music(speak)

def next_music_action():
    next_music(speak)

def previous_music_action():
    previous_music(speak)