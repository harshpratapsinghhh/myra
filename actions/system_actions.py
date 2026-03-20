import os
from output.speaker import speak

def open_app(app_name):
    speak(f"Opening {app_name}")
    os.system(f"start {app_name}")