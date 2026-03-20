from output.speaker import speak

def detect_mood(command):
    command = command.lower()

    if any(word in command for word in ["bored", "boring", "nothing to do"]):
        return "bored"

    elif any(word in command for word in ["sleepy", "sleep", "tired"]):
        return "sleepy"

    elif any(word in command for word in ["sad", "low", "upset"]):
        return "sad"

    return None


def suggest_action(mood):

    if mood == "bored":
        speak("You seem bored. Should I play your favorite music or open YouTube?")

    elif mood == "sleepy":
        speak("You look tired. Should I play some calm music?")

    elif mood == "sad":
        speak("I can play something uplifting for you. Want me to?")

    else:
        speak("I'm here if you need anything.")