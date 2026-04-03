import time
from core.memory_engine import get_last_activity
from output.speaker import speak


def check_prediction():
    action, timestamp = get_last_activity()

    if not action or not timestamp:
        return

    current_time = time.time()

    # wait at least 20 seconds
    if current_time - timestamp < 20:
        return

    if action == "play_music":
        speak("Do you want me to play similar songs?")

    elif action == "pause_music":
        speak("Should I resume your music?")