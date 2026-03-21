import speech_recognition as sr

def listen():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source, timeout=5, phrase_time_limit=5)

    try:
        command = r.recognize_google(audio)
        print(f"[DEBUG] You said: {command}")
        return command.lower()

    except sr.UnknownValueError:
        print("[DEBUG] Could not understand audio")
        return ""

    except sr.RequestError:
        print("[DEBUG] API error")
        return ""