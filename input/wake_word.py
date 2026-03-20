from input.voice_listener import listen
from config.assistant_config import WAKE_WORDS

def wait_for_wake_word():
    while True:
        command = listen()

        if not command:
            continue

        for trigger in WAKE_WORDS:
            if trigger in command:
                return True