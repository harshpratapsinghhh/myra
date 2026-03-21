import json
import os
import datetime
import json

HISTORY_FILE = "data/history.json"

def load_history():
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except:
        return {
            "activity_log": [],
            "music_history": {},
            "user_preferences": {}
        }


def save_history(data):
    with open(HISTORY_FILE, "w") as f:
        json.dump(data, f, indent=4)


MEMORY_FILE = "data/memory.json"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}

    with open(MEMORY_FILE, "r") as file:
        try:
            return json.load(file)
        except:
            return {}

def save_memory(memory):
    with open(MEMORY_FILE, "w") as file:
        json.dump(memory, file, indent=4)

# remeber key and values like a song played how many times will help to learn fav by repitation of song
def remember(key, value):
    memory = load_memory()
    memory[key] = value
    save_memory(memory)


def recall(key):
    memory = load_memory()
    return memory.get(key, None)

def update_music_history(song):
    memory = load_history()

    if "music_history" not in memory:
        memory["music_history"] = {}

    history = memory["music_history"]

    if song in history:
        history[song] += 1
    else:
        history[song] = 1

    memory["last_song"] = song

    save_history(memory)

# remeber last action done
def remember_context(action, data=""):
    memory = load_memory()
    memory["last_action"] = action
    memory["last_data"] = data
    save_memory(memory)


def get_context():
    memory = load_memory()
    return memory.get("last_action"), memory.get("last_data")

# Updates song queue according to my usage
def update_song_queue(song):
    memory = load_memory()

    queue = memory.get("song_queue", [])
    index = memory.get("current_index", -1)

    # If new song, append
    queue.append(song)
    index = len(queue) - 1

    memory["song_queue"] = queue
    memory["current_index"] = index

    save_memory(memory)

# For previous song
def get_previous_song():
    memory = load_memory()
    queue = memory.get("song_queue", [])
    index = memory.get("current_index", -1)

    if index > 0:
        index -= 1
        memory["current_index"] = index
        save_memory(memory)
        return queue[index]

    return None

# For next song
def get_next_song():
    memory = load_memory()
    queue = memory.get("song_queue", [])
    index = memory.get("current_index", -1)

    if index < len(queue) - 1:
        index += 1
        memory["current_index"] = index
        save_memory(memory)
        return queue[index]

    return None

# help myra to get suggestion for me.
def learn_user_preference(song):
    memory = load_history()

    prefs = memory.get("user_preferences", {})

    # Simple logic (can upgrade later)
    if "arijit" in song:
        prefs["favorite_artist"] = "arijit singh"

    elif "lofi" in song or "calm" in song:
        prefs["favorite_type"] = "calm"

    elif "remix" in song or "dj" in song:
        prefs["favorite_type"] = "party"

    memory["user_preferences"] = prefs
    save_history(memory)

# Here my daily activity log will be located
def log_activity(action):
    memory = load_history()

    logs = memory.get("activity_log", [])

    current_time = datetime.datetime.now().strftime("%H")

    logs.append({
        "action": action,
        "hour": current_time
    })

    # keep last 50 logs only
    logs = logs[-50:]

    memory["activity_log"] = logs
    save_history(memory)