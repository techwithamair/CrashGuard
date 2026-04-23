# ─────────────────────────────────────
# CrashGuard System - gui.py
# Tkinter dashboard display
# ─────────────────────────────────────

import tkinter as tk
from datetime import datetime

class CrashGuardGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CrashGuard System")
        self.root.geometry("720x500")
        self.root.configure(bg="#0d1117")
        self.root.resizable(False, False)

        # Title bar
        title = tk.Label(
            root,
            text="🛡 CrashGuard System",
            font=("Arial", 22, "bold"),
            fg="#58a6ff",
            bg="#0d1117"
        )
        title.pack(pady=(15, 5))

        # Status
        self.status_lbl = tk.Label(
            root,
            text="● SAFE",
            font=("Arial", 28, "bold"),
            fg="#3fb950",
            bg="#0d1117"
        )
        self.status_lbl.pack(pady=8)

        # Severity
        self.severity_lbl = tk.Label(
            root,
            text="Severity: None",
            font=("Arial", 16),
            fg="#8b949e",
            bg="#0d1117"
        )
        self.severity_lbl.pack(pady=3)

        # Sensor frame
        sensor_frame = tk.Frame(
            root, bg="#161b22",
            pady=10, padx=20
        )
        sensor_frame.pack(
            fill="x", padx=40, pady=8
        )

        self.accel_lbl = tk.Label(
            sensor_frame,
            text="Acceleration: 0.00g",
            font=("Arial", 13),
            fg="#c9d1d9",
            bg="#161b22"
        )
        self.accel_lbl.pack(anchor="w")

        self.tilt_lbl = tk.Label(
            sensor_frame,
            text="Tilt: 0.0 degrees",
            font=("Arial", 13),
            fg="#c9d1d9",
            bg="#161b22"
        )
        self.tilt_lbl.pack(anchor="w")

        self.speed_lbl = tk.Label(
            sensor_frame,
            text="Speed: 0.0 mph",
            font=("Arial", 13),
            fg="#c9d1d9",
            bg="#161b22"
        )
        self.speed_lbl.pack(anchor="w")

        self.gps_lbl = tk.Label(
            sensor_frame,
            text="GPS: Acquiring satellite...",
            font=("Arial", 13),
            fg="#c9d1d9",
            bg="#161b22"
        )
        self.gps_lbl.pack(anchor="w")

        self.type_lbl = tk.Label(
            sensor_frame,
            text="Type: --",
            font=("Arial", 13),
            fg="#c9d1d9",
            bg="#161b22"
        )
        self.type_lbl.pack(anchor="w")

        # Countdown
        self.countdown_lbl = tk.Label(
            root,
            text="",
            font=("Arial", 18, "bold"),
            fg="#f85149",
            bg="#0d1117"
        )
        self.countdown_lbl.pack(pady=5)

        # Time
        self.time_lbl = tk.Label(
            root,
            text="",
            font=("Arial", 11),
            fg="#484f58",
            bg="#0d1117"
        )
        self.time_lbl.pack(pady=3)
        self._update_time()

    def _update_time(self):
        now = datetime.now().strftime(
            "%Y-%m-%d  %H:%M:%S"
        )
        self.time_lbl.config(text=now)
        self.root.after(1000, self._update_time)

    def update_safe(self, accel, tilt,
                    speed, lat, lon):
        self.status_lbl.config(
            text="● SAFE",
            fg="#3fb950"
        )
        self.severity_lbl.config(
            text="Severity: None",
            fg="#8b949e"
        )
        self.accel_lbl.config(
            text=f"Acceleration: {accel:.2f}g"
        )
        self.tilt_lbl.config(
            text=f"Tilt: {tilt:.1f} degrees"
        )
        self.speed_lbl.config(
            text=f"Speed: {speed:.1f} mph"
        )
        if lat:
            self.gps_lbl.config(
                text=f"GPS: {lat:.5f}, {lon:.5f}"
            )
        self.type_lbl.config(text="Type: --")
        self.countdown_lbl.config(text="")

    def update_accident(self, severity, atype,
                        accel, tilt, speed,
                        lat, lon, countdown):
        self.status_lbl.config(
            text="⚠ ACCIDENT DETECTED",
            fg="#f85149"
        )
        color_map = {
            "SEVERE":   "#f85149",
            "MODERATE": "#d29922",
            "MINOR":    "#e3b341"
        }
        self.severity_lbl.config(
            text=f"Severity: {severity}",
            fg=color_map.get(severity, "#f85149")
        )
        self.accel_lbl.config(
            text=f"Acceleration: {accel:.2f}g"
        )
        self.tilt_lbl.config(
            text=f"Tilt: {tilt:.1f} degrees"
        )
        self.speed_lbl.config(
            text=f"Speed at impact: {speed:.1f} mph"
        )
        if lat:
            self.gps_lbl.config(
                text=f"GPS: {lat:.5f}, {lon:.5f}"
            )
        self.type_lbl.config(
            text=f"Type: {atype}"
        )
        if countdown > 0:
            self.countdown_lbl.config(
                text=f"Sending alert in {countdown}s..."
            )
        else:
            self.countdown_lbl.config(
                text="🚨 Alert sent!"
            )

    def update_listening(self):
        self.countdown_lbl.config(
            text="🎤 Listening for response...",
            fg="#58a6ff"
        )

    def update_cancelled(self):
        self.countdown_lbl.config(
            text="✅ Alert cancelled",
            fg="#3fb950"
        )
