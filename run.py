from core.brain import process
from output.speaker import speak
from actions.music_actions import pause_music_action

def text_mode():
    speak("Text mode activated.")

    while True:
        command = input("You: ").lower().strip()

        # HOTWORD INTERRUPT
        if command.strip() in ["myra", "hey myra"]:
            pause_music_action()  
            speak("Yes?")
            continue

        if not command:
            continue

        if command in ["exit", "quit", "bye"]:
            speak("Shutting down text mode.")
            break

        process(command)

if __name__ == "__main__":
    text_mode()

# play music udte teer jamaiya ke
# What MYRA is thinking right now -- memory.json
# What MYRA has learned over time -- history.json