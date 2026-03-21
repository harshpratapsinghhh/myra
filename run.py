from core.brain import process
from output.speaker import speak

def text_mode():
    speak("Text mode activated.")

    while True:
        command = input("You: ").lower().strip()

        if not command:
            continue

        if command in ["exit", "quit", "bye"]:
            speak("Shutting down text mode.")
            break

        process(command)

if __name__ == "__main__":
    text_mode()

# play music udte teer jamaiya ke