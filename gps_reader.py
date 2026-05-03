# ─────────────────────────────────────
# CrashGuard System - gps_reader.py
#
# Real GPS modules (like the NEO-6M) lose
# signal inside metal Expo halls. This 
# module simulates live satellite movement
# to keep the GUI dynamic and responsive.
# ─────────────────────────────────────


import threading
import time

class GPSReader:
    def __init__(self):
        self.lat = 32.5232
        self.lon = -92.6379

        self.demo_thread = threading.Thread(
            target=self._update,
            daemon=True
        )
        self.demo_thread.start()
        print("GPS Module: Running")

    def _update(self):
        while True:
            self.lat += 0.00001
            self.lon += 0.00001
            time.sleep(1)

    def get_location(self):
        return self.lat, self.lon

    def get_maps_link(self):
        return (
            f"https://maps.google.com"
            f"/?q={self.lat},{self.lon}"
        )
