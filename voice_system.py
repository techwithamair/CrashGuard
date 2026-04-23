# ─────────────────────────────────────
# CrashGuard System - voice_system.py
# FEATURE: OFFLINE VOICE RECOGNITION
#
# Handles speaking and listening
# Uses WM8960 Audio HAT, pyttsx3 for TTS,
# and Vosk for offline speech recognition.
# ─────────────────────────────────────

import pyttsx3
import speech_recognition as sr
import json
import os

# ─────────────────────────────────────
# 1. TEXT-TO-SPEECH (TTS) SETUP
# ─────────────────────────────────────
engine = pyttsx3.init()
engine.setProperty("rate",   145) # Slightly slower for clarity
engine.setProperty("volume", 1.0)

def speak(text):
    """Converts text to audible speech and prints to console."""
    print(f"[SPEAK] {text}")
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"[SPEAK ERROR] {e}")


# ─────────────────────────────────────
# 2. SPEECH RECOGNITION SETUP
# ─────────────────────────────────────
recognizer = sr.Recognizer()
# Expo Hall Optimization: Dynamic threshold helps ignore background chatter
recognizer.energy_threshold         = 300
recognizer.dynamic_energy_threshold = True

def _find_vosk_model():
    """Finds the actual existing path for the Vosk offline model."""
    candidates = [
        "vosk-model-small-en-us-0.15",
        "model"
    ]
    for path in candidates:
        if os.path.exists(path):
            return path  # returns ACTUAL path
    return None

def listen(timeout=10):
    """
    Listens to the microphone and processes speech entirely OFFLINE via Vosk.
    Returns the parsed text or a failure code.
    """
    # CRITICAL: Prevent fatal crash if offline model is missing
    model_path = _find_vosk_model()
    
    if not model_path:
        print("[CRITICAL] Vosk model folder not found! Voice recognition disabled.")
        return "error"

    with sr.Microphone() as source:
        print("[LISTEN] Adjusting for background noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        
        print("[LISTEN] Microphone Active. Listening now...")
        try:
            # phrase_time_limit ensures it stops listening after 5 seconds of talking
            audio = recognizer.listen(
                source,
                timeout=timeout,
                phrase_time_limit=5
            )
            
            # Vosk processes the audio locally (No Wi-Fi needed)
            text   = recognizer.recognize_vosk(audio)
            result = json.loads(text)
            heard  = result.get("text", "")
            
            print(f"[LISTEN] Heard: '{heard}'")
            return heard.lower()

        except sr.WaitTimeoutError:
            print("[LISTEN] Timeout - no response detected.")
            return "timeout"
        except Exception as e:
            print(f"[LISTEN] Hardware/Processing Error: {e}")
            return "unknown"


# ─────────────────────────────────────
# 3. CRASH RESPONSE LOGIC
# ─────────────────────────────────────
def ask_and_listen():
    """
    Coordinates the driver interaction. 
    Returns 'OKAY', 'HELP', or 'TIMEOUT' back to main.py.
    """
    # main.py already states the accident type. We just give the instructions here.
    speak("Please say YES if you are fine, or NO if you need help. You have 10 seconds.")
    
    response = listen(timeout=10)

    # Robust word-matching for high-stress environments
    yes_words = [
        "yes", "okay", "fine", "good",
        "alright", "im fine", "i am okay",
        "cancel", "safe", "i am fine"
    ]
    
    no_words = [
        "no", "help", "hurt", "injured",
        "emergency", "pain", "not okay",
        "i need help", "call"
    ]

    # Evaluate the transcript
    if any(w in response for w in yes_words):
        return "OKAY"
    elif any(w in response for w in no_words):
        return "HELP"
    else:
        # If they say something unintelligible, or silence, assume the worst.
        return "TIMEOUT"
