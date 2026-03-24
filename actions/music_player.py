from youtubesearchpython import VideosSearch
import webbrowser
import pyautogui
import time
from core.memory_engine import set_music_state

# SYSTEM MEDIA CONTROL

def play_pause():
    pyautogui.press("playpause")

def next_track():
    pyautogui.press("nexttrack")

def previous_track():
    pyautogui.press("prevtrack")


# MAIN MUSIC CONTROLLER

import threading
import time
import pywhatkit


from core.memory_engine import set_music_state
import threading
import pywhatkit

def play_music(speak, song_name=""):

    def play_task():
        try:
            pywhatkit.playonyt(song_name)
            set_music_state(True)   # 🔥 mark playing
        except Exception as e:
            print(f"[MUSIC ERROR]: {e}")
    try:
        if song_name:
            threading.Thread(target=play_task, daemon=True).start()
        else:
            play_pause()

    except Exception as e:
        print(f"[MUSIC ERROR]: {e}")

        speak("Trying alternative method")

        try:
            # FALLBACK METHOD
            from youtubesearchpython import VideosSearch
            import webbrowser

            videosSearch = VideosSearch(song_name, limit=1)
            result = videosSearch.result()

            video_url = result["result"][0]["link"]
            webbrowser.open(video_url)

        except Exception as e:
            print(f"[FALLBACK ERROR]: {e}")
            speak("I couldn't play that song.")


def pause_music(speak=None):
    pyautogui.press("playpause")
    time.sleep(0.3)
    pyautogui.press("playpause")

    set_music_state(False)   # 🔥 mark paused

def resume_music(speak=None):
    pyautogui.press("playpause")
    set_music_state(True)


def next_music(speak):
    speak("Playing next track")
    next_track()


def previous_music(speak):
    speak("Playing previous track")
    previous_track()