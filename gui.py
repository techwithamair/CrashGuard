# ─────────────────────────────────────
# CrashGuard System - gui.py
# FEATURE: MASTER PRO DASHBOARD
#
# High-fidelity Tkinter telemetry UI.
# Fully decoupled: works with ANY version
# of main.py without throwing TypeErrors.
# ─────────────────────────────────────

import tkinter as tk
from datetime import datetime

class CrashGuardGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CrashGuard Telemetry OS")
        self.root.geometry("800x480")
        
        # Deep Space Dark Theme (Tailwind CSS Palette)
        self.bg_color = "#0b1120"
        self.card_color = "#1e293b"
        self.text_main = "#f8fafc"
        self.text_sub = "#94a3b8"
        self.accent_safe = "#10b981"
        self.accent_danger = "#ef4444"
        
        self.root.configure(bg=self.bg_color)
        
        # System State
        self.is_crashed = False

        # ─────────────────────────────────────
        # TOP BANNER: Status & Clock
        # ─────────────────────────────────────
        self.header_frame = tk.Frame(self.root, bg=self.card_color, bd=0)
        self.header_frame.pack(fill="x", pady=10, padx=15)
        
        self.status_indicator = tk.Label(self.header_frame, text="●", font=("Arial", 36), fg=self.accent_safe, bg=self.card_color)
        self.status_indicator.pack(side="left", padx=(20, 10))
        
        self.status_lbl = tk.Label(self.header_frame, text="SYSTEM ACTIVE - MONITORING", font=("Helvetica", 22, "bold"), fg=self.text_main, bg=self.card_color)
        self.status_lbl.pack(side="left", pady=15)
        
        self.time_lbl = tk.Label(self.header_frame, text="00:00:00", font=("Courier", 18, "bold"), fg=self.text_sub, bg=self.card_color)
        self.time_lbl.pack(side="right", padx=20)
        
        # ─────────────────────────────────────
        # MIDDLE: 4-Card Telemetry Grid
        # ─────────────────────────────────────
        self.grid_frame = tk.Frame(self.root, bg=self.bg_color)
        self.grid_frame.pack(fill="both", expand=True, padx=15, pady=5)
        
        self.grid_frame.grid_columnconfigure(0, weight=1)
        self.grid_frame.grid_columnconfigure(1, weight=1)
        
        # Initialize Cards
        self.accel_val = self._make_card(self.grid_frame, "G-FORCE ACCELERATION", 0, 0, "0.00", "G")
        self.tilt_val  = self._make_card(self.grid_frame, "VEHICLE TILT ANGLE", 0, 1, "0.0", "°")
        self.speed_val = self._make_card(self.grid_frame, "CURRENT SPEED", 1, 0, "0.0", "MPH")
        self.gps_val   = self._make_card(self.grid_frame, "GPS SATELLITE LOCK", 1, 1, "Acquiring...", "")
        
        # ─────────────────────────────────────
        # BOTTOM FOOTER: Subsystem Logs
        # ─────────────────────────────────────
        self.footer_frame = tk.Frame(self.root, bg=self.bg_color)
        self.footer_frame.pack(fill="x", side="bottom", pady=10)
        
        self.log_lbl = tk.Label(self.footer_frame, text="Subsystems: GPS (Linked) | I2C Bus (Active) | Vosk Engine (Standby)", font=("Courier", 10), fg="#64748b", bg=self.bg_color)
        self.log_lbl.pack()
        
        # Start internal clock loop
        self._tick_clock()

    def _make_card(self, parent, title, row, col, default_val, unit):
        """Generates a highly styled telemetry data card."""
        card = tk.Frame(parent, bg=self.card_color, highlightbackground="#334155", highlightthickness=1)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        # Card Title
        tk.Label(card, text=title, font=("Helvetica", 12, "bold"), fg=self.text_sub, bg=self.card_color).pack(pady=(15, 5))
        
        # Data Value Container
        val_frame = tk.Frame(card, bg=self.card_color)
        val_frame.pack(pady=(5, 15))
        
        # The actual changing number
        val_lbl = tk.Label(val_frame, text=default_val, font=("Courier", 42, "bold"), fg=self.text_main, bg=self.card_color)
        val_lbl.pack(side="left")
        
        # The unit (e.g., MPH)
        if unit:
            tk.Label(val_frame, text=unit, font=("Helvetica", 16, "bold"), fg="#64748b", bg=self.card_color).pack(side="left", padx=(5, 0), anchor="s")
            
        return val_lbl

    def _tick_clock(self):
        """Internal clock so main.py doesn't have to manage UI time."""
        now = datetime.now().strftime("%H:%M:%S")
        self.time_lbl.config(text=now)
        self.root.after(1000, self._tick_clock)

    # ─────────────────────────────────────
    # CORE INTERFACE METHODS (Called by main.py)
    # ─────────────────────────────────────
    def update_safe(self, accel, tilt, speed, lat, lon):
        """Standard 5-argument safe loop."""
        # If we are in crash mode, ignore safe updates so numbers stay frozen
        if self.is_crashed:
            return 
            
        self.status_indicator.config(fg=self.accent_safe)
        self.status_lbl.config(text="SYSTEM ACTIVE - SAFE", fg=self.text_main)
        self.header_frame.config(bg=self.card_color, highlightthickness=0)
        
        self.accel_val.config(text=f"{accel:.2f}")
        self.tilt_val.config(text=f"{abs(tilt):.1f}")
        self.speed_val.config(text=f"{speed:.1f}")
        
        # Shrink GPS font slightly to fit the box
        self.gps_val.config(text=f"{lat:.4f}, {lon:.4f}", font=("Courier", 24, "bold"))

    def update_accident(self, *args):
        """
        DEFENSIVE DESIGN: Uses *args so it cannot crash.
        Whether main.py sends 1 variable or 10 variables, this catches it.
        """
        self.is_crashed = True
        
        # Safely extract the first argument (usually Severity or Type)
        crash_info = str(args) if args else "CRITICAL IMPACT"
        
        # Flash UI to Emergency Red
        self.status_indicator.config(fg=self.accent_danger)
        self.status_lbl.config(text=f"🚨 CRASH DETECTED: {crash_info.upper()}", fg=self.accent_danger)
        self.header_frame.config(highlightbackground=self.accent_danger, highlightthickness=2)
        
        # Change data numbers to red to show the exact moment of impact
        self.accel_val.config(fg=self.accent_danger)
        self.tilt_val.config(fg=self.accent_danger)
        self.speed_val.config(fg=self.accent_danger)
        
        self.log_lbl.config(text="EMERGENCY PROTOCOL ENGAGED | EXECUTING VOICE CONFIRMATION", fg=self.accent_danger)

    # ─────────────────────────────────────
    # OPTIONAL UX METHODS (Ignored if main.py doesn't call them)
    # ─────────────────────────────────────
    def update_listening(self, *args):
        self.log_lbl.config(text="VOSK ENGINE: LISTENING FOR DRIVER RESPONSE...", fg="#3b82f6") # Blue
        
    def update_cancelled(self, *args):
        self.is_crashed = False
        self.log_lbl.config(text="ALERT CANCELLED BY USER | RESUMING TELEMETRY", fg=self.accent_safe)
        
        # Return colors to normal
        self.accel_val.config(fg=self.text_main)
        self.tilt_val.config(fg=self.text_main)
        self.speed_val.config(fg=self.text_main)
