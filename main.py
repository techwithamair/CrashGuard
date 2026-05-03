# ─────────────────────────────────────
# CrashGuard System - main.py
# MASTER COORDINATOR
#
# Links the hardware sensors, GPS, Voice
# Engine, GUI, Logger, and Email Alerts
# into a single, bulletproof thread loop.
# ─────────────────────────────────────

# ─────────────────────────────────────
# CrashGuard - main.py
# Speed completely removed
# ─────────────────────────────────────

import time
import threading
import tkinter as tk

from sensor_mpu6050 import MPU6050
from gps_reader     import GPSReader
from voice_system   import ask_and_listen, speak
from alert_sender   import send_all_alerts
from detector       import AccidentDetector
from gui            import CrashGuardGUI
from logger         import log_event

sensor   = MPU6050()
gps      = GPSReader()
detector = AccidentDetector()

def emergency_sequence(gui, event):
    lat, lon = gps.get_location()

    gui.root.after(0, gui.update_listening)

    speak(
        f"Alert! {event['reason']}. "
        f"Are you okay?"
    )
    driver_response = ask_and_listen()

    log_event(
        severity=event["severity"],
        accel=event["accel"],
        tilt=event["tilt"],
        lat=lat,
        lon=lon,
        response=driver_response,
        reason=event["type"]
    )

    if driver_response == "OKAY":
        gui.root.after(0, gui.update_cancelled)
        speak(
            "Incident logged. "
            "System returning to normal."
        )
        time.sleep(2)
    else:
        speak("Dispatching emergency alerts now.")
        gui.root.after(
            0, gui.update_accident,
            event["severity"]
        )
        send_all_alerts(
            severity=event["severity"],
            lat=lat,
            lon=lon,
            accel=event["accel"],
            tilt=event["tilt"],
            reason=event["reason"]
        )

def monitor(gui):
    while True:
        try:
            accel    = sensor.get_magnitude()
            tilt     = sensor.get_tilt()
            lat, lon = gps.get_location()

            event = detector.analyze(accel, tilt)

            if event:
                gui.root.after(
                    0, gui.update_accident,
                    event["severity"]
                )
                emergency_sequence(gui, event)
                detector.accel_history.clear()
                detector.tilt_history.clear()
            else:
                gui.root.after(
                    0, gui.update_safe,
                    accel, tilt, lat, lon
                )

            time.sleep(0.05)

        except Exception as e:
            print(f"System Error: {e}")
            gui.root.after(
                0,
                lambda: gui.status_lbl.config(
                    text="HARDWARE ERROR",
                    fg="orange"
                )
            )
            time.sleep(2)
            try:
                sensor.__init__()
            except:
                pass

if __name__ == "__main__":
    root    = tk.Tk()
    app_gui = CrashGuardGUI(root)

    monitor_thread = threading.Thread(
        target=monitor,
        args=(app_gui,),
        daemon=True
    )
    monitor_thread.start()

    root.after(
        1500,
        lambda: speak("CrashGuard system is ready.")
    )
    root.mainloop()
