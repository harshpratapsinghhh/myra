import os
import pyautogui
import time
import webbrowser
import pywhatkit

# Extendable
# Later we can plug:
# Spotify API
# Offline ML recommendations
# Playlist system

music_folder = "D:\\music" # Offline music folder


# SYSTEM MEDIA CONTROL

def play_pause():
    pyautogui.press("playpause")

def next_track():
    pyautogui.press("nexttrack")

def previous_track():
    pyautogui.press("prevtrack")


# MAIN MUSIC CONTROLLER

def play_music(speak, song_name=""):
    try:
        if song_name:
            speak(f"Playing {song_name} on YouTube")

            # Directly plays first YouTube result
            pywhatkit.playonyt(song_name)

        else:
            speak("Resuming music")
            play_pause()

    except Exception as e:
        speak("Error playing music")


def pause_music(speak):
    speak("Pausing music")
    play_pause()


def resume_music(speak):
    speak("Resuming music")
    play_pause()


def next_music(speak):
    speak("Playing next track")
    next_track()


def previous_music(speak):
    speak("Playing previous track")
    previous_track()

# Later upgrade (we WILL do):
# Direct YouTube video open -- done 
# Or API-based playback