from youtubesearchpython import VideosSearch
import webbrowser
import pyautogui
import time

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


def play_music(speak, song_name=""):

    def play_task():
        try:
            pywhatkit.playonyt(song_name)
        except Exception as e:
            print(f"[MUSIC ERROR]: {e}")

    try:
        if song_name:
            # Run in background thread (NON-BLOCKING)
            threading.Thread(target=play_task, daemon=True).start()

        else:
            speak("Resuming music")
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
    import pyautogui
    import time

    pyautogui.press("playpause")
    time.sleep(0.3)
    pyautogui.press("playpause")  # second press ensures pause


def resume_music(speak):
    speak("Resuming music")
    play_pause()


def next_music(speak):
    speak("Playing next track")
    next_track()


def previous_music(speak):
    speak("Playing previous track")
    previous_track()