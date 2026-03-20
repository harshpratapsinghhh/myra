import json
import os

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


def remember(key, value):
    memory = load_memory()
    memory[key] = value
    save_memory(memory)


def recall(key):
    memory = load_memory()
    return memory.get(key, None)

def update_music_history(song):
    memory = load_memory()

    if "music_history" not in memory:
        memory["music_history"] = {}

    history = memory["music_history"]

    if song in history:
        history[song] += 1
    else:
        history[song] = 1

    memory["last_song"] = song

    save_memory(memory)

def remember_context(action, data=""):
    memory = load_memory()
    memory["last_action"] = action
    memory["last_data"] = data
    save_memory(memory)


def get_context():
    memory = load_memory()
    return memory.get("last_action"), memory.get("last_data")

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