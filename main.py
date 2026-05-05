# ─────────────────────────────────────
# CrashGuard System - main.py
# MASTER COORDINATOR
#
# GUI replaced by Flask web dashboard.
# Open http://<PI-IP>:5000 on any browser
# (Windows PC, phone, tablet) to view.
# ─────────────────────────────────────

import time
import threading

from sensor_mpu6050 import MPU6050
from gps_reader     import GPSReader
from voice_system   import ask_and_listen, speak
from alert_sender   import send_all_alerts
from detector       import AccidentDetector
from server         import CrashGuardGUI        # ← was: from gui import CrashGuardGUI
from logger         import log_event

sensor   = MPU6050()
gps      = GPSReader()
detector = AccidentDetector()

def emergency_sequence(gui, event):
    lat, lon = gps.get_location()

    gui.update_listening()                       # ← no more root.after needed

    speak(f"Alert! {event['reason']}.")
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
        gui.update_cancelled()
        speak("Incident logged. System returning to normal.")
        time.sleep(2)
    else:
        speak("Dispatching emergency alerts now.")
        gui.update_accident(event["severity"], event["accel"], event["tilt"])
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
                gui.update_accident(event["severity"], event["accel"], event["tilt"])
                emergency_sequence(gui, event)
                detector.accel_history.clear()
                detector.tilt_history.clear()
            else:
                gui.update_safe(accel, tilt, lat, lon)

            time.sleep(0.05)

        except Exception as e:
            print(f"System Error: {e}")
            gui.update_hardware_error()
            time.sleep(2)
            try:
                sensor.__init__()
            except:
                pass

if __name__ == "__main__":
    gui = CrashGuardGUI()                        # starts Flask on port 5000

    monitor_thread = threading.Thread(
        target=monitor,
        args=(gui,),
        daemon=True
    )
    monitor_thread.start()

    speak("CrashGuard system is ready.")

    # Keep main thread alive (replaces root.mainloop())
    while True:
        time.sleep(1)
