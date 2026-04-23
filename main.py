# ─────────────────────────────────────
# CrashGuard System - main.py
# MASTER COORDINATOR
#
# Links the hardware sensors, GPS, Voice
# Engine, GUI, Logger, and Email Alerts
# into a single, bulletproof thread loop.
# ─────────────────────────────────────

import time
import threading
import tkinter as tk

# Import all custom CrashGuard modules
from sensor_mpu6050 import MPU6050
from gps_reader import GPSReader
from voice_system import ask_and_listen, speak
from alert_sender import send_all_alerts
from detector import AccidentDetector
from gui import CrashGuardGUI
from logger import log_event

# Initialize Core Hardware & Logic Components
sensor = MPU6050()
gps = GPSReader()
detector = AccidentDetector()

def emergency_sequence(gui, event):
    """
    Executes the full crash response protocol:
    Voice prompt -> Log -> Check response -> Alert.
    """
    lat, lon, speed = gps.get_location()
    
    # 1. Update GUI to show the microphone is active
    gui.root.after(0, gui.update_listening)
    
    # 2. Trigger Vosk Voice Engine
    speak(f"Alert! {event['reason']}. Are you okay?")
    driver_response = ask_and_listen()
    
    # 3. Permanently log the event and the driver's response to CSV
    log_event(
        severity=event["severity"],
        accel=event["accel"],
        tilt=event["tilt"],
        lat=lat,
        lon=lon,
        speed=speed,
        response=driver_response,
        reason=event["type"]
    )
    
    # 4. Handle the response
    if driver_response == "OKAY":
        # Driver is safe. Cancel alert.
        gui.root.after(0, gui.update_cancelled)
        speak("Incident logged. System returning to normal.")
        time.sleep(2) # Give the judge 2 seconds to read the cancellation on screen
    else:
        # Driver needs help (or timeout occurred). Dispatch alerts!
        speak("Dispatching emergency alerts now.")
        
        # Ensure the GUI stays locked in the red "Emergency" state
        gui.root.after(0, gui.update_accident, event["severity"])
        
        # Fire the background email threads
        send_all_alerts(
            severity=event["severity"],
            lat=lat,
            lon=lon,
            speed=speed,
            accel=event["accel"],
            tilt=event["tilt"],
            reason=event["reason"]
        )

def monitor(gui):
    """
    The main telemetry loop. Runs on a background thread so 
    it never freezes the Tkinter touch screen.
    """
    while True:
        try:
            # Poll Sensors
            accel = sensor.get_magnitude()
            tilt = sensor.get_tilt()
            lat, lon, speed = gps.get_location()
            
            # Run False-Positive Filtering Analysis
            event = detector.analyze(accel, tilt, speed)
            
            if event:
                # 🚨 CRASH DETECTED
                # Lock the GUI with the exact crash parameters
                gui.root.after(0, gui.update_accident, event["severity"])
                
                # Execute the Voice and Alert sequence
                emergency_sequence(gui, event)
                
                # INFINITE LOOP PREVENTION: Wipe the detector's memory
                detector.accel_history.clear() 
                detector.tilt_history.clear()
            else:
                # ✅ SYSTEM SAFE
                # Update live telemetry numbers on the dashboard
                gui.root.after(0, gui.update_safe, accel, tilt, speed, lat, lon)
                
            # Loop frequency (20 times per second)
            time.sleep(0.05)
            
        except Exception as e:
            # HARDWARE DISCONNECT PROTECTION
            print(f"System Error: {e}")
            gui.root.after(0, lambda: gui.status_lbl.config(text="⚠ HARDWARE ERROR", fg="orange"))
            time.sleep(2)
            
            # Safe sensor reconnect sequence
            try:
                sensor.__init__()
            except:
                pass

if __name__ == "__main__":
    # 1. Initialize the display window
    root = tk.Tk()
    
    # 2. Build the Dashboard UI
    app_gui = CrashGuardGUI(root)
    
    # 3. Launch the hardware monitor in a separate Daemon thread
    monitor_thread = threading.Thread(target=monitor, args=(app_gui,), daemon=True)
    monitor_thread.start()
    
    # 4. Startup Announcement (Waits 1.5s for UI to render)
    root.after(1500, lambda: speak("CrashGuard system is ready."))
    
    # 5. Start the UI event loop (must be on the main thread)
    root.mainloop()
