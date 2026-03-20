from output.voice_engine import generate_voice
from config.assistant_config import VOICE_TONE
import os
import time


def speak(text):
    try:
        # Personality control
        if VOICE_TONE == "professional":
            text = text.replace("boss", "").strip()

        # Generate voice
        filename = generate_voice(text)

        # Play audio
        os.system(f'start /min {filename}')
        time.sleep(2)

    except Exception as e:
        print(f"[SPEAKER ERROR]: {e}")