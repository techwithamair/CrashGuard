# ─────────────────────────────────────
# CrashGuard System - main.py
# COMPLETE FINAL CODE
#
# Hardware:
#   GY-521 MPU6050  → I2C (SDA/SCL)
#   NEO-6M GPS      → UART (TX/RX)
#   WM8960 HAT      → I2S + I2C
#   Pi keyboard     → WiFi for alerts
#
# Features:
#   1. Folium map display
#   2. Smart email with Google Maps
#   3. False positive filtering
# ─────────────────────────────────────

import time
import threading
import tkinter as tk

from sensor_mpu6050 import MPU6050
from gps_reader     import GPSReader
from voice_system   import speak, ask_driver
from alert_sender   import send_all_alerts
from map_display    import generate_map
from logger         import log_event
from detector       import AccidentDetector
from gui            import CrashGuardGUI

# ─────────────────────────────────────
# INITIALIZE ALL HARDWARE
# ─────────────────────────────────────
print("CrashGuard starting up...")

sensor   = MPU6050()
gps      = GPSReader()
detector = AccidentDetector()

# ─────────────────────────────────────
# EMERGENCY SEQUENCE
# Called when accident is detected
# ─────────────────────────────────────
def emergency_sequence(gui, event):

    severity = event["severity"]
    accel    = event["accel"]
    tilt     = event["tilt"]
    reason   = event["reason"]
    atype    = event["type"]

    # Get GPS location immediately
    lat, lon, speed = gps.get_location()

    print(f"\n{'='*40}")
    print(f"ACCIDENT DETECTED!")
    print(f"Type:     {atype}")
    print(f"Severity: {severity}")
    print(f"Reason:   {reason}")
    print(f"Accel:    {accel:.2f}g")
    print(f"Tilt:     {tilt:.1f} degrees")
    print(f"Speed:    {speed:.1f} mph")
    print(f"GPS:      {lat}, {lon}")
    print(f"{'='*40}\n")

    # Update GUI
    gui.update_accident(
        severity, atype,
        accel, tilt, speed,
        lat, lon, 0
    )

    # Generate map immediately
    # runs in background while asking driver
    if lat and lon:
        map_thread = threading.Thread(
            target=generate_map,
            args=(lat, lon, severity,
                  speed, accel, tilt),
            daemon=True
        )
        map_thread.start()

    # Ask driver if they are okay
    # WM8960 speaks and listens
    gui.update_listening()
    response = ask_driver()

    print(f"Driver response: {response}")

    # ─────────────────────────────
    # HANDLE RESPONSE
    # ─────────────────────────────

    if response == "OKAY":
        # Driver is fine
        speak("Okay! Alert cancelled. Stay safe!")
        gui.update_cancelled()
        log_event(
            severity, accel, tilt,
            lat, lon, speed,
            "CANCELLED", reason
        )
        print("Alert cancelled by driver")
        time.sleep(2)
        return

    elif response == "HELP":
        # Driver needs help
        speak(
            "Sending emergency alert now! "
            "Help is on the way!"
        )

    else:
        # No response = assume unconscious
        speak(
            "No response detected. "
            "Assuming emergency. "
            "Sending alert automatically!"
        )

    # ─────────────────────────────
    # SEND ALL ALERTS
    # ─────────────────────────────
    gui.update_accident(
        severity, atype,
        accel, tilt, speed,
        lat, lon, 0
    )

    # Send email + telegram simultaneously
    send_all_alerts(
        severity, lat, lon,
        speed, accel, tilt, reason
    )

    # Log event
    log_event(
        severity, accel, tilt,
        lat, lon, speed,
        response, reason
    )

    speak("Emergency alert sent successfully!")
    print("All alerts sent!")


# ─────────────────────────────────────
# MAIN MONITORING LOOP
# Runs in background thread
# Reads sensor 20 times per second
# ─────────────────────────────────────
def monitor(gui):
    accident_active = False

    print("Monitoring started...")

    while True:
        try:
            # Read sensor
            accel, tilt = sensor.get_all()
            lat, lon, speed = gps.get_location()

            # Run through detector
            # with false positive filtering
            event = detector.analyze(
                accel, abs(tilt), speed
            )

            if event and not accident_active:
                # ACCIDENT CONFIRMED
                accident_active = True
                emergency_sequence(gui, event)
                accident_active = False

            else:
                # All normal
                gui.root.after(
                    0,
                    gui.update_safe,
                    accel, tilt,
                    speed, lat, lon
                )

            # 0.05 seconds = 20 reads per second
            time.sleep(0.05)

        except Exception as e:
            print(f"Monitor error: {e}")
            time.sleep(1)


# ─────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────
def main():
    speak("CrashGuard system starting up.")
    print("Initializing GUI...")

    root = tk.Tk()
    gui  = CrashGuardGUI(root)

    # Start monitor in background thread
    monitor_thread = threading.Thread(
        target=monitor,
        args=(gui,),
        daemon=True
    )
    monitor_thread.start()

    speak("CrashGuard system is ready.")
    print("System ready!")

    # GUI runs on main thread
    root.mainloop()


if __name__ == "__main__":
    main()
