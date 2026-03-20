import webbrowser
from output.speaker import speak

def search_google(query):
    speak(f"Searching for {query}")
    webbrowser.open(f"https://www.google.com/search?q={query}")