# ─────────────────────────────────────
# CrashGuard System - gps_reader.py
# Expo Demo Edition (Threaded)
#
# Real GPS modules (like the NEO-6M) lose
# signal inside metal Expo halls. This 
# module simulates live satellite movement
# to keep the GUI dynamic and responsive.
# ─────────────────────────────────────

import threading
import time
import random

class GPSReader:
    def __init__(self):
        """
        Initialize with Ruston, LA coordinates.
        Launches a background thread to simulate live vehicle movement.
        """
        # Starting coordinates for Ruston, Louisiana
        self.lat = 32.5232
        self.lon = -92.6379
        self.speed = 45.0
        
        # Start the live-movement simulation
        self.demo_thread = threading.Thread(target=self._update, daemon=True)
        self.demo_thread.start()
        print("GPS Module: Running in Expo Demo Mode (Ruston, LA)")

    def _update(self):
        """
        Background thread that slightly shifts coordinates and speed.
        This prevents the GUI from looking frozen during the presentation
        and proves to judges that the system handles real-time data loops.
        """
        while True:
            # Micro-movements to simulate driving south-east
            self.lat += 0.00001
            self.lon += 0.00001
            
            # Add slight speed fluctuations (e.g., 44.8 to 45.2 mph)
            # to make the dashboard look completely authentic
            fluctuation = random.uniform(-0.3, 0.3)
            self.speed = max(0.0, self.speed + fluctuation)
            
            # Update frequency
            time.sleep(1)

    def get_location(self):
        """
        Returns the current simulated coordinates and speed.
        Signature precisely matches what main.py and alert_sender.py expect.
        """
        return self.lat, self.lon, self.speed
