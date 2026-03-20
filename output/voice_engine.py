from gtts import gTTS
import os

def generate_voice(text):
    filename = "response.mp3"

    if os.path.exists(filename):
        try:
            os.remove(filename)
        except:
            pass

    tts = gTTS(text=text, lang='en', tld='co.uk')
    tts.save(filename)

    return filename