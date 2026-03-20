from input.voice_listener import listen
from input.wake_word import wait_for_wake_word
from output.speaker import speak
from core.brain import process
from config.assistant_config import SLEEP_WORDS, EXIT_WORDS


def main():
    speak("System initialized. Say my name to activate.")

    while True:
        # WAIT FOR WAKE WORD
        wait_for_wake_word()
        speak("Yes, I'm listening.")

        fail_count = 0  # Track mic failures

        # ACTIVE MODE
        while True:
            command = listen()

            if not command:
                fail_count += 1
                print(f"[INFO] No input detected ({fail_count})")

                # Auto fallback to text mode
                if fail_count >= 3:
                    speak("Switching to text mode temporarily.")

                    from run import text_mode
                    text_mode()

                    fail_count = 0
                    speak("Returning to voice mode.")

                continue

            # Reset fail count if valid input
            fail_count = 0

            # EXIT SYSTEM
            if any(word in command for word in EXIT_WORDS):
                speak("Shutting down.")
                exit()

            # SLEEP MODE
            if any(word in command for word in SLEEP_WORDS):
                speak("Going to standby mode.")
                break

            # PROCESS COMMAND
            process(command)


if __name__ == "__main__":
    main()