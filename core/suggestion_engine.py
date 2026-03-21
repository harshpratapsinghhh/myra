from output.speaker import speak
from core.memory_engine import (
    load_memory, save_memory
    )
import datetime

def detect_mood(command):
    command = command.lower()

    if any(word in command for word in ["bored", "boring", "nothing to do"]):
        return "bored"

    elif any(word in command for word in ["sleepy", "sleep", "tired"]):
        return "sleepy"

    elif any(word in command for word in ["sad", "low", "upset"]):
        return "sad"

    return None

def set_pending(action):
    memory = load_memory()
    memory["pending_action"] = action
    save_memory(memory)

def suggest_action(mood):

    memory = load_memory()
    prefs = memory.get("user_preferences", {})

    fav_artist = prefs.get("favorite_artist", "")
    fav_type = prefs.get("favorite_type", "")

    if mood == "bored":

        if fav_artist:
            speak(f"You seem bored. Should I play some {fav_artist} songs or open YouTube?")

        elif fav_type:
            speak(f"You seem bored. Should I play some {fav_type} music or open YouTube?")

        else:
            speak("You seem bored. Should I play your favorite music or open YouTube?")

        set_pending("bored_options")

    elif mood == "sleepy":
        speak("You look tired. Should I play some calm music?")
        set_pending("play_calm_music")

    elif mood == "sad":
        speak("I can play something uplifting for you. Want me to?")
        set_pending("play_happy_music")

    else:
        speak("I'm here if you need anything.")

# 
def detect_habit():
    memory = load_memory()
    logs = memory.get("activity_log", [])

    if not logs:
        return None

    current_hour = datetime.datetime.now().strftime("%H")

    # filter logs of same hour
    same_time_logs = [log for log in logs if log["hour"] == current_hour]

    if len(same_time_logs) < 3:
        return None

    actions = [log["action"] for log in same_time_logs]

    most_common = max(set(actions), key=actions.count)

    return most_common