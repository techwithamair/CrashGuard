# ─────────────────────────────────────
# CrashGuard System - gps_reader.py
# Reads location and speed from
# NEO-6M GPS module via UART
# Updates continuously in background
# ─────────────────────────────────────

import serial
import pynmea2
import threading
from config import GPS_PORT, GPS_BAUDRATE

class GPSReader:
    def __init__(self):
        self.lat   = None
        self.lon   = None
        self.speed = 0.0

        try:
            self.ser = serial.Serial(
                GPS_PORT,
                GPS_BAUDRATE,
                timeout=1
            )
            # Start background thread
            # always has fresh data ready
            t = threading.Thread(
                target=self._update,
                daemon=True
            )
            t.start()
            print("GPS initialized")
        except Exception as e:
            print(f"GPS init failed: {e}")
            self.ser = None

    def _update(self):
        while True:
            try:
                line = self.ser.readline()
                line = line.decode(
                    "utf-8",
                    errors="ignore"
                )
                if line.startswith("$GPRMC"):
                    msg = pynmea2.parse(line)
                    if msg.latitude:
                        self.lat = msg.latitude
                        self.lon = msg.longitude
                        if msg.spd_over_grnd:
                            # Convert knots to mph
                            self.speed = (
                                float(msg.spd_over_grnd)
                                * 1.15078
                            )
            except:
                pass

    def get_location(self):
        return self.lat, self.lon, self.speed

    def get_maps_link(self):
        if self.lat and self.lon:
            return (
                f"https://maps.google.com"
                f"/?q={self.lat},{self.lon}"
            )
        return "Location not available"

    def is_ready(self):
        return self.lat is not None
