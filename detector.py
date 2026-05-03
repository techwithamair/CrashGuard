# ─────────────────────────────────────
# CrashGuard System - detector.py
# Smart accident detection with
# FALSE POSITIVE FILTERING
# ─────────────────────────────────────

# ─────────────────────────────────────
# CrashGuard - detector.py
# Speed detection removed
# Tilt + accel combined fix applied
# ─────────────────────────────────────

from config import (
    ACCIDENT_THRESHOLD,
    MODERATE_THRESHOLD,
    SEVERE_THRESHOLD,
    TILT_THRESHOLD,
    CONFIRM_READINGS
)

class AccidentDetector:
    def __init__(self):
        self.accel_history = []
        self.tilt_history  = []

    def analyze(self, accel, tilt):
        self.accel_history.append(accel)
        self.tilt_history.append(abs(tilt))

        if len(self.accel_history) > 5:
            self.accel_history.pop(0)
        if len(self.tilt_history) > 5:
            self.tilt_history.pop(0)

        impact   = self._check_impact(accel)
        rollover = self._check_tilt(tilt, accel)

        return self._classify(
            impact, rollover, accel, tilt
        )

    def _check_impact(self, accel):
        if accel >= SEVERE_THRESHOLD:
            return "SEVERE"

        moderate_count = sum(
            1 for r in self.accel_history
            if r >= MODERATE_THRESHOLD
        )
        if moderate_count >= 2:
            return "MODERATE"

        minor_count = sum(
            1 for r in self.accel_history
            if r >= ACCIDENT_THRESHOLD
        )
        if minor_count >= CONFIRM_READINGS:
            return "MINOR"

        return "NONE"

    def _check_tilt(self, tilt, accel):
        if len(self.tilt_history) < 3:
            return "NONE"

        latest = self.tilt_history[-1]

        if latest < TILT_THRESHOLD:
            return "NONE"

        if accel <= 1.5:
            return "NONE"

        increasing = all(
            self.tilt_history[i] <=
            self.tilt_history[i + 1]
            for i in range(
                len(self.tilt_history) - 2,
                len(self.tilt_history) - 1
            )
        )

        if increasing and latest >= TILT_THRESHOLD:
            return "ROLLOVER"

        return "NONE"

    def _classify(self, impact, rollover,
                  accel, tilt):
        if (impact   == "NONE" and
            rollover == "NONE"):
            return None

        if rollover == "ROLLOVER":
            return {
                "severity": "SEVERE",
                "type":     "ROLLOVER",
                "accel":    accel,
                "tilt":     tilt,
                "reason":   "Vehicle rollover detected"
            }

        if impact == "SEVERE":
            return {
                "severity": "SEVERE",
                "type":     "IMPACT",
                "accel":    accel,
                "tilt":     tilt,
                "reason":   "Severe impact detected"
            }
        if impact == "MODERATE":
            return {
                "severity": "MODERATE",
                "type":     "IMPACT",
                "accel":    accel,
                "tilt":     tilt,
                "reason":   "Moderate impact detected"
            }
        if impact == "MINOR":
            return {
                "severity": "MINOR",
                "type":     "IMPACT",
                "accel":    accel,
                "tilt":     tilt,
                "reason":   "Minor impact detected"
            }

        return None
