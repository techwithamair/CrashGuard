# ─────────────────────────────────────
# CrashGuard System - voice_system.py
# Handles speaking and listening
# Uses WM8960 Audio HAT
# pyttsx3 for speech output
# Vosk for offline speech recognition
# ─────────────────────────────────────

import pyttsx3
import speech_recognition as sr
import json

# Initialize TTS engine once
engine = pyttsx3.init()
engine.setProperty("rate",   145)
engine.setProperty("volume", 1.0)

def speak(text):
    print(f"[SPEAK] {text}")
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Speak error: {e}")

# Initialize recognizer once
recognizer = sr.Recognizer()
recognizer.energy_threshold        = 300
recognizer.dynamic_energy_threshold = True

def listen(timeout=10):
    with sr.Microphone() as source:
        print("[LISTEN] Adjusting for noise...")
        recognizer.adjust_for_ambient_noise(
            source, duration=1
        )
        print("[LISTEN] Listening now...")
        try:
            audio = recognizer.listen(
                source,
                timeout=timeout,
                phrase_time_limit=5
            )
            # Vosk runs completely offline
            text   = recognizer.recognize_vosk(audio)
            result = json.loads(text)
            heard  = result.get("text", "")
            print(f"[LISTEN] Heard: '{heard}'")
            return heard.lower()

        except sr.WaitTimeoutError:
            print("[LISTEN] Timeout - no response")
            return "timeout"
        except Exception as e:
            print(f"[LISTEN] Error: {e}")
            return "unknown"

def ask_driver():
    speak(
        "Accident detected! "
        "Are you okay? "
        "Say YES if you are fine. "
        "Say NO if you need help. "
        "You have 10 seconds to respond."
    )
    response = listen(timeout=10)

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

    if any(w in response for w in yes_words):
        return "OKAY"
    elif any(w in response for w in no_words):
        return "HELP"
    else:
        # No response or unclear
        return "TIMEOUT"
