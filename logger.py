# ─────────────────────────────────────
# CrashGuard System - logger.py
# Saves every event to CSV file
# ─────────────────────────────────────

import csv
import os
from datetime import datetime
from config import LOG_FILE

def log_event(severity, accel, tilt, lat, lon, speed, response, reason):
    # Create file with headers if it does not exist yet
    file_exists = os.path.exists(LOG_FILE)

    try:
        with open(LOG_FILE, "a", newline="") as f:
            writer = csv.writer(f)

            # Write headers if this is a brand new file
            if not file_exists:
                writer.writerow([
                    "timestamp", 
                    "severity",
                    "type", 
                    "accel_g",
                    "tilt_deg", 
                    "speed_mph",
                    "latitude", 
                    "longitude",
                    "driver_response"
                ])

            # Write the actual accident data
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                severity,
                reason,
                round(accel, 2),
                round(tilt,  2),
                round(speed, 1),
                lat  if lat  else "N/A",
                lon  if lon  else "N/A",
                response
            ])

        print(f"Logger: Event permanently saved ({severity} | Response: {response})")
    except Exception as e:
        print(f"Logger Error: Could not save to CSV - {e}")
