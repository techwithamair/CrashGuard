# ─────────────────────────────────────
# CrashGuard System - server.py
# REPLACES gui.py
#
# Flask server that:
#   1. Serves the HTML dashboard
#   2. Streams real sensor data to it via SSE
#   3. Exposes the same interface as gui.py
#      so main.py needs minimal changes
# ─────────────────────────────────────

import threading
import json
import time
from flask import Flask, Response
from datetime import datetime

app = Flask(__name__)

# ── Shared state (written by main.py, read by browser) ──
_state = {
    "status":   "safe",          # "safe" | "warn" | "critical"
    "accel":    0.0,
    "tilt":     0.0,
    "lat":      32.5232,
    "lon":      -92.6379,
    "footer":   "TELEMETRY NOMINAL",
    "g_max":    0.0,
}
_state_lock = threading.Lock()
_clients    = []                 # SSE subscriber queues
_clients_lock = threading.Lock()

def _push(data: dict):
    """Push a JSON update to all connected SSE clients."""
    msg = "data: " + json.dumps(data) + "\n\n"
    with _clients_lock:
        for q in _clients:
            q.append(msg)

def _update_state(patch: dict):
    with _state_lock:
        _state.update(patch)
    _push(_state.copy())


# ─────────────────────────────────────
# ROUTES
# ─────────────────────────────────────

@app.route("/")
def index():
    """Serve the dashboard HTML."""
    with open("dashboard.html", "r") as f:
        return f.read()

@app.route("/stream")
def stream():
    """SSE endpoint — browser connects here for live data."""
    q = []
    with _clients_lock:
        _clients.append(q)

    def generate():
        # Send current state immediately on connect
        yield "data: " + json.dumps(_state) + "\n\n"
        try:
            while True:
                if q:
                    yield q.pop(0)
                else:
                    time.sleep(0.05)
        except GeneratorExit:
            pass
        finally:
            with _clients_lock:
                if q in _clients:
                    _clients.remove(q)

    return Response(generate(), mimetype="text/event-stream",
                    headers={"Cache-Control": "no-cache",
                             "X-Accel-Buffering": "no"})


# ─────────────────────────────────────
# GUI-COMPATIBLE INTERFACE
# (main.py calls these exactly like it
#  called gui.update_safe / update_accident)
# ─────────────────────────────────────

class CrashGuardGUI:
    """Drop-in replacement for the Tkinter CrashGuardGUI class."""

    def __init__(self):
        self._g_max = 0.0
        # Start Flask in a background daemon thread
        t = threading.Thread(
            target=lambda: app.run(host="0.0.0.0", port=5000, threaded=True),
            daemon=True
        )
        t.start()
        print("[CrashGuard] Dashboard live at http://<PI-IP>:5000")

    # Called by main.py via root.after — we just call directly
    def after(self, _delay, fn, *args):
        """Shim so main.py's gui.root.after() calls still work."""
        fn(*args)

    # ── Safe loop ──
    def update_safe(self, accel, tilt, lat, lon):
        if accel > self._g_max:
            self._g_max = accel
        _update_state({
            "status":  "safe",
            "accel":   round(accel, 2),
            "tilt":    round(tilt, 1),
            "lat":     round(lat, 4),
            "lon":     round(lon, 4),
            "g_max":   round(self._g_max, 2),
            "footer":  "TELEMETRY NOMINAL",
        })

    # ── Crash detected ──
    def update_accident(self, *args):
        severity = str(args[0]) if args else "CRITICAL"
        accel    = float(args[1]) if len(args) >= 2 else _state["accel"]
        tilt     = float(args[2]) if len(args) >= 3 else _state["tilt"]
        if accel > self._g_max:
            self._g_max = accel
        _update_state({
            "status":  "critical",
            "accel":   round(accel, 2),
            "tilt":    round(abs(tilt), 1),
            "g_max":   round(self._g_max, 2),
            "footer":  f"🚨 CRASH DETECTED: {severity.upper()}",
        })

    # ── Voice listening ──
    def update_listening(self, *args):
        _update_state({
            "status": "warn",
            "footer": "🎤 LISTENING FOR DRIVER RESPONSE...",
        })

    # ── Alert cancelled ──
    def update_cancelled(self, *args):
        self._g_max = 0.0
        _update_state({
            "status": "safe",
            "footer": "✅ ALERT CANCELLED — RESUMING",
        })

    # ── Hardware/sensor error ──
    def update_hardware_error(self, *args):
        _update_state({
            "status": "warn",
            "footer": "⚠ HARDWARE ERROR — RETRYING...",
        })
