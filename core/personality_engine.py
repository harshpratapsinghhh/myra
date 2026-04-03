import random
from config.assistant_config import PERSONALITY_MODE
import datetime


def get_mode(command, mood=None):
    
    command = command.lower()
    hour = datetime.datetime.now().hour  # ✅ FIXED (dynamic time)

    # Night behavior
    if hour >= 23:
        return "professional"

    # Mood based
    if mood == "sad":
        return "friendly"
    
    if mood == "sleepy":
        return "professional"
    
    # Casual tone detection
    if any(word in command for word in ["bhai", "yaar", "bro"]):
        return "desi"
    
    # Default
    return PERSONALITY_MODE


def respond(action, data="", command="", mood=None):

    responses = {

        "friendly": {
            "play_music": [
                f"Alright, playing {data}" if data else "Playing music",
                f"Got it, here's {data}" if data else "Got it, playing music",
                f"Enjoy {data}" if data else "Enjoy the music",
                f"Playing {data} for you" if data else "Playing something for you"
            ],
            "pause_music": [
                "Pausing the music",
                "Music paused",
                "Alright, taking a pause"
            ],
            "resume_music": [
                "Resuming your music",
                "Back to where we left off",
                "Let's continue"
            ],
            "time": [
                "Let me check the time for you",
                "Here's the current time"
            ],
            "default": [
                "Done",
                "Alright",
                "Got it"
            ]
        },

        "professional": {
            "play_music": [
                f"Playing {data}" if data else "Playing music",
                f"Initiating playback: {data}" if data else "Initiating playback"
            ],
            "pause_music": [
                "Music paused",
                "Playback halted"
            ],
            "resume_music": [
                "Resuming playback",
                "Continuing music"
            ],
            "time": [
                "Fetching current time",
                "Current time is as follows"
            ],
            "default": [
                "Completed",
                "Done"
            ]
        },

        "desi": {
            "play_music": [
                f"Chalo bhai, {data} baja dete hain" if data else "Chalo bhai, music chalu karte hain",
                f"Lo ji, {data} shuru karte hain" if data else "Lo ji, music shuru"
            ],
            "pause_music": [
                "Thoda rukte hain",
                "Music band kar diya"
            ],
            "resume_music": [
                "Phir se chalu karte hain",
                "Wapas shuru kar diya"
            ],
            "time": [
                "Ek second, time check karta hoon",
                "Abhi ka time bata raha hoon"
            ],
            "default": [
                "Ho gaya kaam",
                "Done bhai"
            ]
        }
    }

    # Select mode properly
    mode = get_mode(command, mood)

    # Safety fallback
    if mode not in responses:
        mode = "friendly"

    action_responses = responses[mode].get(action, responses[mode]["default"])

    return random.choice(action_responses)