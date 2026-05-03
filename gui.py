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
        self.root       = root
        self.root.title("CrashGuard Telemetry OS")
        self.root.geometry("800x480")

        self.bg_color      = "#0b1120"
        self.card_color    = "#1e293b"
        self.text_main     = "#f8fafc"
        self.text_sub      = "#94a3b8"
        self.accent_safe   = "#10b981"
        self.accent_danger = "#ef4444"

        self.root.configure(bg=self.bg_color)
        self.is_crashed = False

        # TOP BANNER
        self.header_frame = tk.Frame(
            self.root,
            bg=self.card_color, bd=0
        )
        self.header_frame.pack(
            fill="x", pady=10, padx=15
        )

        self.status_indicator = tk.Label(
            self.header_frame,
            text="●",
            font=("Arial", 36),
            fg=self.accent_safe,
            bg=self.card_color
        )
        self.status_indicator.pack(
            side="left", padx=(20, 10)
        )

        self.status_lbl = tk.Label(
            self.header_frame,
            text="SYSTEM ACTIVE - MONITORING",
            font=("Helvetica", 22, "bold"),
            fg=self.text_main,
            bg=self.card_color
        )
        self.status_lbl.pack(side="left", pady=15)

        self.time_lbl = tk.Label(
            self.header_frame,
            text="00:00:00",
            font=("Courier", 18, "bold"),
            fg=self.text_sub,
            bg=self.card_color
        )
        self.time_lbl.pack(side="right", padx=20)

        # MIDDLE — 3 cards only
        self.grid_frame = tk.Frame(
            self.root, bg=self.bg_color
        )
        self.grid_frame.pack(
            fill="both", expand=True,
            padx=15, pady=5
        )

        self.grid_frame.grid_columnconfigure(
            0, weight=1
        )
        self.grid_frame.grid_columnconfigure(
            1, weight=1
        )
        self.grid_frame.grid_columnconfigure(
            2, weight=1
        )

        self.accel_val = self._make_card(
            self.grid_frame,
            "G-FORCE", 0, 0, "0.00", "G"
        )
        self.tilt_val = self._make_card(
            self.grid_frame,
            "TILT ANGLE", 0, 1, "0.0", "°"
        )
        self.gps_val = self._make_card(
            self.grid_frame,
            "GPS LOCATION", 0, 2,
            "Acquiring...", ""
        )

        # FOOTER
        self.footer_frame = tk.Frame(
            self.root, bg=self.bg_color
        )
        self.footer_frame.pack(
            fill="x", side="bottom", pady=10
        )

        self.log_lbl = tk.Label(
            self.footer_frame,
            text="Subsystems: GPS (Linked) | I2C Bus (Active) | Voice Engine (Standby)",
            font=("Courier", 10),
            fg="#64748b",
            bg=self.bg_color
        )
        self.log_lbl.pack()

        self._tick_clock()

    def _make_card(self, parent, title,
                   row, col, default_val, unit):
        card = tk.Frame(
            parent,
            bg=self.card_color,
            highlightbackground="#334155",
            highlightthickness=1
        )
        card.grid(
            row=row, column=col,
            padx=10, pady=10,
            sticky="nsew"
        )

        tk.Label(
            card, text=title,
            font=("Helvetica", 12, "bold"),
            fg=self.text_sub,
            bg=self.card_color
        ).pack(pady=(15, 5))

        val_frame = tk.Frame(
            card, bg=self.card_color
        )
        val_frame.pack(pady=(5, 15))

        val_lbl = tk.Label(
            val_frame, text=default_val,
            font=("Courier", 42, "bold"),
            fg=self.text_main,
            bg=self.card_color
        )
        val_lbl.pack(side="left")

        if unit:
            tk.Label(
                val_frame, text=unit,
                font=("Helvetica", 16, "bold"),
                fg="#64748b",
                bg=self.card_color
            ).pack(
                side="left",
                padx=(5, 0),
                anchor="s"
            )

        return val_lbl

    def _tick_clock(self):
        now = datetime.now().strftime("%H:%M:%S")
        self.time_lbl.config(text=now)
        self.root.after(1000, self._tick_clock)

    def update_safe(self, accel, tilt, lat, lon):
        if self.is_crashed:
            return

        self.status_indicator.config(
            fg=self.accent_safe
        )
        self.status_lbl.config(
            text="SYSTEM ACTIVE - SAFE",
            fg=self.text_main
        )
        self.accel_val.config(
            text=f"{accel:.2f}"
        )
        self.tilt_val.config(
            text=f"{abs(tilt):.1f}"
        )
        self.gps_val.config(
            text=f"{lat:.4f}, {lon:.4f}",
            font=("Courier", 24, "bold")
        )

    def update_accident(self, *args):
        self.is_crashed = True
        crash_info = (
            str(args[0]) if args else "CRITICAL"
        )

        self.status_indicator.config(
            fg=self.accent_danger
        )
        self.status_lbl.config(
            text=f"CRASH DETECTED: {crash_info.upper()}",
            fg=self.accent_danger
        )
        self.accel_val.config(
            fg=self.accent_danger
        )
        self.tilt_val.config(
            fg=self.accent_danger
        )
        self.log_lbl.config(
            text="EMERGENCY PROTOCOL ENGAGED",
            fg=self.accent_danger
        )

    def update_listening(self, *args):
        self.log_lbl.config(
            text="LISTENING FOR DRIVER RESPONSE...",
            fg="#3b82f6"
        )

    def update_cancelled(self, *args):
        self.is_crashed = False
        self.log_lbl.config(
            text="ALERT CANCELLED | RESUMING",
            fg=self.accent_safe
        )
        self.accel_val.config(fg=self.text_main)
        self.tilt_val.config(fg=self.text_main)
