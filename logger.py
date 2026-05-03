# ─────────────────────────────────────
# CrashGuard - logger.py
# Speed removed from log
# ─────────────────────────────────────

import csv
from datetime import datetime

LOG_FILE = "accident_log.csv"

def log_event(severity, accel, tilt,
              lat, lon, response, reason):
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            severity,
            round(accel, 2),
            round(tilt, 2),
            lat,
            lon,
            response,
            reason
        ])
    print(
        f"Logged: {severity} | {response}"
    )
