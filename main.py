import sys
from input.voice_listener import listen
from input.wake_word import wait_for_wake_word
from output.speaker import speak
from core.brain import process
from config.assistant_config import SLEEP_WORDS, EXIT_WORDS
from actions.music_actions import pause_music_action
from core.prediction_engine import check_prediction
from actions.music_actions import pause_music_action, is_music_playing

def main():
    speak("System initialized. Say my name to activate.")

    while True:
        # WAIT FOR WAKE WORD
        wait_for_wake_word()
        speak("Yes, I'm listening.")

        fail_count = 0

        # ACTIVE MODE
        while True:
            command = listen()

            if not command:
                fail_count += 1
                print(f"[INFO] No input detected ({fail_count})")

                check_prediction()

                if fail_count >= 3:
                    speak("Switching to text mode temporarily.")
                    from run import text_mode
                    text_mode()
                    fail_count = 0
                    speak("Returning to voice mode.")
                continue

            fail_count = 0

             # HOTWORD INTERRUPT
             
            if any(word in command for word in ["myra","mayara"]):
                if is_music_playing():
                    pause_music_action() 
                speak("Yes?")
                continue

            # EXIT SYSTEM
            if any(word in command for word in EXIT_WORDS):
                speak("Shutting down.")
                sys.exit()

            # SLEEP MODE
            if any(word in command for word in SLEEP_WORDS):
                speak("Going to standby mode.")
                break

            # PROCESS COMMAND SAFELY
            try:
                process(command)
            except Exception as e:
                print(f"[ERROR]: {e}")
                speak("Something went wrong, but I'm still here.")


if __name__ == "__main__":
    main()