from core.intent_engine import detect_intent
from output.speaker import speak
from actions.system_actions import open_app
from actions.web_actions import search_google
from actions.music_actions import (
    play_music_action,
    pause_music_action,
    resume_music_action,
    next_music_action,
    previous_music_action
)
from input.voice_listener import listen
import webbrowser
import time
from core.suggestion_engine import ( 
    detect_mood,
    suggest_action,
    detect_habit,
    set_pending
    )
from core.memory_engine import ( 
    recall,
    update_music_history, load_memory,
    remember_context, get_context,
    update_song_queue, get_previous_song, get_next_song,
    save_memory,
    learn_user_preference,
    log_activity
 )


# FALLBACK SYSTEM
def fallback(command):
    speak("I couldn't understand that. Should I search it for you?")
    
    response = listen()

    if not response:
        speak("No response detected.")
        return

    if any(word in response for word in ["yes", "search", "go ahead"]):
        speak("Searching now")
        webbrowser.open(f"https://www.google.com/search?q={command}")
    else:
        speak("Okay, skipping")


# MAIN PROCESSOR
def process(command):

    habit = detect_habit()

    if habit == "play_music":
        speak("You usually listen to music at this time. Want me to play something?")
        set_pending("habit_music")
        return

    elif habit == "open_app":
        speak("You usually open something at this time. Want me to open it?")
        set_pending("habit_app")
        return
    
    # STEP -1: HANDLE PENDING ACTION
    memory = load_memory()
    pending = memory.get("pending_action", "")

    if pending:
        if any(word in command for word in ["yes", "yeah", "yup", "ok", "okay"]):
        
            if pending == "play_calm_music":
                song = "calm relaxing music"
                speak("Playing something relaxing")
                time.sleep(2)

                update_music_history(song)
                update_song_queue(song)
                play_music_action(song)
                remember_context("play_music", song)

            elif pending == "play_happy_music":
                song = "happy upbeat music"
                speak("Playing something uplifting")
                time.sleep(2)

                update_music_history(song)
                update_song_queue(song)
                play_music_action(song)
                remember_context("play_music", song)

            elif pending == "bored_options":
                speak("What would you like? Music or YouTube?")
            
            elif pending == "habit_music":
                speak("Playing music for you")
                time.sleep(2)
                play_music_action("top songs")
        
            memory["pending_action"] = ""
            save_memory(memory)
            return
        

        # MULTI-CHOICE HANDLING (MAIN FEATURE)

    if pending == "bored_options":

        if "music" in command:
            speak("Playing your favorite music")
            time.sleep(2)

            memory_data = load_memory()
            history = memory_data.get("music_history", {})

            if history:
                fav_song = max(history, key=history.get)

                update_song_queue(fav_song)
                play_music_action(fav_song)
                remember_context("play_music", fav_song)
            else:
                play_music_action("top songs")

        elif "youtube" in command:
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")
            remember_context("open_app", "youtube")

        else:
            speak("I didn't get that. Please say music or YouTube.")
            return

        memory["pending_action"] = ""
        save_memory(memory)
        return

    #  NO RESPONSE

    elif any(word in command for word in ["no", "nope", "nah"]):
        speak("Alright, let me know if you need anything.")
        memory["pending_action"] = ""
        save_memory(memory)
        return

    # STEP 0: MOOD DETECTION (HIGHEST PRIORITY)

    mood = detect_mood(command)

    if mood:
        suggest_action(mood)
        return
    
    # STEP 1: CONTEXT COMMANDS (HIGH PRIORITY)

    if "play that again" in command or "play again" in command:
        last_action, last_data = get_context()

        if last_action == "play_music" and last_data:
            speak(f"Playing {last_data} again")
            time.sleep(2)

            update_song_queue(last_data)  
            play_music_action(last_data)

            remember_context("play_music", last_data)
            return

    if "open it" in command:
        last_action, last_data = get_context()

        if last_action == "open_app" and last_data:
            speak(f"Opening {last_data} again")
            time.sleep(1)

            open_app(last_data)
            remember_context("open_app", last_data)
            return

    # NEW: QUEUE CONTROLS

    if "play previous song" in command:
        song = get_previous_song()

        if song:
            speak(f"Playing previous song {song}")
            time.sleep(2)

            play_music_action(song)
            remember_context("play_music", song)
        else:
            speak("No previous song found")
        return

    if "play next song" in command:
        song = get_next_song()

        if song:
            speak(f"Playing next song {song}")
            time.sleep(2)

            play_music_action(song)
            remember_context("play_music", song)
        else:
            speak("No next song found")
        return


    # STEP 2: NORMAL INTENT FLOW

    intent = detect_intent(command)

    if not intent:
        fallback(command)
        return

    action = intent["action"]
    data = intent.get("data", "")


    # STEP 3: ACTION EXECUTION

    if action == "open_app":
        log_activity("open_app")
        speak(f"Opening {data}")
        time.sleep(1)

        open_app(data)
        remember_context("open_app", data)


    elif action == "search":
        log_activity("search")
        speak(f"Searching {data}")
        time.sleep(1)

        search_google(data)
        remember_context("search", data)


    elif action == "play_music":

        log_activity("play_music")

        if data:
            speak(f"Playing {data}")
            time.sleep(2)

            # LEARNING + MEMORY PIPELINE
            update_music_history(data)
            update_song_queue(data)
            learn_user_preference(data)
            play_music_action(data)
            remember_context("play_music", data)

        else:
            last_song = recall("last_song")

            if last_song:
                speak(f"Playing your last song {last_song}")
                time.sleep(2)

                # KEEP SYSTEM CONSISTENT
                update_music_history(last_song)
                update_song_queue(last_song)
                learn_user_preference(last_song)

                play_music_action(last_song)

                remember_context("play_music", last_song)

            else:
                speak("What would you like to hear?")


    elif action == "favorite_music":
        memory = load_memory()
        history = memory.get("music_history", {})

        if history:
            fav_song = max(history, key=history.get)

            speak(f"Playing your favorite song {fav_song}")
            time.sleep(2)

            # SAME PIPELINE HERE ALSO (VERY IMPORTANT)
            update_music_history(fav_song)
            update_song_queue(fav_song)
            learn_user_preference(fav_song)

            play_music_action(fav_song)

            remember_context("play_music", fav_song)

        else:
            speak("I don't know your favorite yet.")


    elif action == "pause_music":
        pause_music_action()
        remember_context("pause_music")


    elif action == "resume_music":
        resume_music_action()
        remember_context("resume_music")


    elif action == "next_music":
        next_music_action()
        remember_context("next_music")


    elif action == "previous_music":
        previous_music_action()
        remember_context("previous_music")


    else:
        fallback(command)