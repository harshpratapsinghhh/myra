from difflib import get_close_matches

# INTENT DEFINITIONS

INTENTS = {
    "play_music": ["play music", "start music", "play song", "put on music"],
    "pause_music": ["pause music", "stop music"],
    "resume_music": ["resume music", "play again", "continue music"],
    "next_music": ["next song", "skip song"],
    "previous_music": ["previous song", "go back song"],
    "favorite_music": ["play my favorite song", "play my favourite", "my favorite song","play my favorite"],
    "open_app": ["open", "launch", "start"],
    "search": ["search", "find", "look up"]
}


# INTENT DETECTOR

def detect_intent(command):
    command = command.lower()

    # Direct keyword match
    for intent, patterns in INTENTS.items():
        for pattern in patterns:
            if pattern in command:
                return extract_data(intent, command)

    # Fuzzy matching (approx match)
    all_patterns = [p for patterns in INTENTS.values() for p in patterns]
    match = get_close_matches(command, all_patterns, n=1, cutoff=0.6)

    if match:
        for intent, patterns in INTENTS.items():
            if match[0] in patterns:
                return extract_data(intent, command)

    return None


# DATA EXTRACTION
def extract_data(intent, command):

    if intent == "play_music":

        song = command.lower()

        # Remove trigger phrases
        triggers = [
            "play music",
            "play song",
            "start music",
            "put on music",
            "play"
        ]

        for word in triggers:
            song = song.replace(word, "")

        # Remove noise words
        noise_words = [
            "on youtube",
            "on chrome",
            "youtube",
            "chrome",
            "please",
            "song"
        ]

        for noise in noise_words:
            song = song.replace(noise, "")

        # Clean spacing
        song = " ".join(song.split())

        # CRITICAL FIX: avoid wrong commands as songs
        invalid_words = ["next", "previous", "again"]

        if song in invalid_words or song == "":
            return {"action": "play_music", "data": ""}

        return {"action": "play_music", "data": song}


    elif intent == "open_app":
        app = command.lower()

        for word in ["open", "launch", "start"]:
            app = app.replace(word, "")

        app = " ".join(app.split())

        return {"action": "open_app", "data": app}


    elif intent == "search":
        query = command.lower()

        for word in ["search", "find", "look up"]:
            query = query.replace(word, "")

        query = " ".join(query.split())

        return {"action": "search", "data": query}


    elif intent == "favorite_music":
        return {"action": "favorite_music"}


    else:
        return {"action": intent}