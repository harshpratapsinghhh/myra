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

def play_music(speak, song_name=""):
    try:
        if song_name:
            # speak(f"Playing {song_name}") -- this was repeating two times.
            time.sleep(1)

            # PRIMARY METHOD (most reliable)
            import pywhatkit
            pywhatkit.playonyt(song_name)

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