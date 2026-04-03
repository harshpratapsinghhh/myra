from core.brain import process
from output.speaker import speak
from actions.music_actions import pause_music_action
from core.prediction_engine import check_prediction
from actions.music_actions import is_music_playing


def text_mode():
    speak("Text mode activated.")

    while True:
        command = input("You: ").lower().strip()

        # IDLE PREDICTION
        if not command:
            check_prediction()
            continue

        # HOTWORD INTERRUPT
        if "myra" in command:
            if is_music_playing():
                pause_music_action()
            speak("Yes?")
            continue

        # EXIT TEXT MODE
        if command in ["exit", "quit", "bye"]:
            speak("Shutting down text mode.")
            break

        # PROCESS COMMAND
        process(command)


if __name__ == "__main__":
    text_mode()

# play music udte teer jamaiya ke
# What MYRA is thinking right now --> memory.json
# What MYRA has learned over time --> history.json