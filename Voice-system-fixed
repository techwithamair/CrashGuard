import ctypes
import os
import sys
import time
import subprocess
import pyttsx3
import speech_recognition as sr

# BLOCK 1: SILENCE ALSA NOISE
try:
    _F = ctypes.CFUNCTYPE(
        None,
        ctypes.c_char_p, ctypes.c_int,
        ctypes.c_char_p, ctypes.c_int,
        ctypes.c_char_p
    )
    def _silent(*a): pass
    ctypes.cdll.LoadLibrary(
        'libasound.so.2'
    ).snd_lib_error_set_handler(_F(_silent))
except:
    pass

# BLOCK 2: STDERR SUPPRESSOR
class _HideStderr:
    def __enter__(self):
        try:
            self._null = open(os.devnull, 'w')
            self._old  = os.dup(2)
            sys.stderr.flush()
            os.dup2(self._null.fileno(), 2)
        except:
            pass
        return self
    def __exit__(self, *a):
        try:
            sys.stderr.flush()
            os.dup2(self._old, 2)
            os.close(self._old)
            self._null.close()
        except:
            pass

# BLOCK 3: TTS ENGINE
_tts = None
try:
    _tts = pyttsx3.init()
    _tts.setProperty('rate', 145)
    _tts.setProperty('volume', 1.0)
    print("[TTS] pyttsx3 ready")
except Exception as e:
    print(f"[TTS] failed: {e}")

def speak(text):
    print(f"[SPEAK] {text}")
    if _tts:
        try:
            _tts.say(text)
            _tts.runAndWait()
            return
        except Exception as e:
            print(f"[SPEAK] pyttsx3 error: {e}")
    try:
        subprocess.run(
            ['espeak', '-v', 'en',
             '-s', '145', '-a', '200', text],
            timeout=20,
            capture_output=True
        )
    except Exception as e:
        print(f"[SPEAK] espeak error: {e}")

# BLOCK 4: YES / NO WORD LISTS
_YES = [
    "yes", "yeah", "yep", "yup", "yea", "ya",
    "okay", "ok", "fine", "good", "great",
    "alright", "all right", "sure", "correct",
    "safe", "cancel", "stop", "im fine",
    "i am fine", "i am okay", "i am good",
    "i'm fine", "i'm okay", "i'm good",
    "am fine", "am okay", "no problem",
    "doing fine", "doing good", "doing okay",
]

_NO = [
    "no", "nope", "nah", "negative",
    "help", "hurt", "pain", "injured",
    "injury", "emergency", "accident",
    "call", "send", "need help", "i need",
    "assist", "danger", "not okay",
    "not fine", "not good", "sos",
    "mayday", "alert", "ambulance",
    "hospital", "doctor", "bleeding",
]

def _classify(text):
    if not text:
        return None
    text = text.lower().strip()
    print(f"[CLASS] Checking: '{text}'")
    for w in _YES:
        if w in text:
            print(f"[CLASS] YES matched: '{w}'")
            return "OKAY"
    for w in _NO:
        if w in text:
            print(f"[CLASS] NO matched: '{w}'")
            return "HELP"
    print(f"[CLASS] No match for: '{text}'")
    return None

# BLOCK 5: SPEECH RECOGNIZER SETUP
_rec = sr.Recognizer()
_rec.energy_threshold         = 100
_rec.dynamic_energy_threshold = True
_rec.pause_threshold          = 1.0
_rec.phrase_threshold         = 0.3
_rec.operation_timeout        = None

# BLOCK 6: GOOGLE LISTEN
def _listen_google(timeout=15):
    try:
        with _HideStderr():
            mic = sr.Microphone()
        with mic as source:
            print("[MIC] Calibrating (1s)...")
            _rec.adjust_for_ambient_noise(
                source, duration=1
            )
            print(
                f"[MIC] Threshold: "
                f"{_rec.energy_threshold:.0f}"
            )
            print(
                f"[MIC] Listening {timeout}s "
                f"— SPEAK NOW"
            )
            audio = _rec.listen(
                source,
                timeout=timeout,
                phrase_time_limit=8
            )
        print("[GOOGLE] Sending to Google...")
        text = _rec.recognize_google(audio)
        text = text.lower().strip()
        print(f"[GOOGLE] Heard: '{text}'")
        return text

    except sr.WaitTimeoutError:
        print("[GOOGLE] No speech detected")
        return "timeout"
    except sr.UnknownValueError:
        print("[GOOGLE] Could not understand")
        return "unknown"
    except sr.RequestError as e:
        print(f"[GOOGLE] No internet: {e}")
        return "no_wifi"
    except Exception as e:
        print(f"[GOOGLE] Error: {e}")
        return "error"

# BLOCK 7: MAIN FUNCTION
# Called by main.py after crash detected
# 1 attempt of 15 seconds
# Returns: OKAY | HELP | TIMEOUT
def ask_and_listen():
    speak(
        "Accident detected! "
        "Are you okay? "
        "Say YES if you are fine. "
        "Say NO if you need help. "
        "You have 15 seconds."
    )

    print("\n[ASR] Listening — 1 attempt of 15s")
    text = _listen_google(timeout=15)

    if text not in (
        "timeout", "unknown",
        "no_wifi", "error", ""
    ):
        match = _classify(text)
        if match:
            return match

    print("\n[ASR] No valid response")
    speak(
        "No response detected. "
        "Sending emergency alert now."
    )
    return "TIMEOUT"

# Alias for compatibility
def ask_driver():
    return ask_and_listen()
