# ─────────────────────────────────────
# CrashGuard System - detector.py
# Smart accident detection with
# FALSE POSITIVE FILTERING
# ─────────────────────────────────────

from config import (
    ACCIDENT_THRESHOLD,
    MODERATE_THRESHOLD,
    SEVERE_THRESHOLD,
    TILT_THRESHOLD,
    SPEED_DROP_THRESHOLD,
    CONFIRM_READINGS
)

class AccidentDetector:
    def __init__(self):
        # Rolling history of readings
        self.accel_history = []
        self.tilt_history  = []
        self.prev_speed    = 0.0

    def analyze(self, accel, tilt, speed):
        # Add to rolling history
        self.accel_history.append(accel)
        self.tilt_history.append(abs(tilt))

        # Keep only last 5 readings
        if len(self.accel_history) > 5:
            self.accel_history.pop(0)
        if len(self.tilt_history) > 5:
            self.tilt_history.pop(0)

        # Run all checks
        impact   = self._check_impact(accel)
        rollover = self._check_tilt(tilt, accel)
        speed_ev = self._check_speed(speed)

        # Update speed history
        self.prev_speed = speed

        return self._classify(
            impact, rollover,
            speed_ev, accel, tilt
        )

    def _check_impact(self, accel):
        # SEVERE: single reading enough
        if accel >= SEVERE_THRESHOLD:
            return "SEVERE"

        # MODERATE: require 2 readings
        moderate_count = sum(
            1 for r in self.accel_history
            if r >= MODERATE_THRESHOLD
        )
        if moderate_count >= 2:
            return "MODERATE"

        # MINOR: require CONFIRM_READINGS
        minor_count = sum(
            1 for r in self.accel_history
            if r >= ACCIDENT_THRESHOLD
        )
        if minor_count >= CONFIRM_READINGS:
            return "MINOR"

        return "NONE"

    def _check_tilt(self, tilt, accel):
        # ── FIX: tilt AND accel combined ──
        # Tilt alone is not enough
        # Must also have real movement
        # accel > 1.5 means actually moving
        # not just someone holding it sideways

        if len(self.tilt_history) < 3:
            return "NONE"

        latest = self.tilt_history[-1]

        # Must exceed tilt threshold
        if latest < TILT_THRESHOLD:
            return "NONE"

        # Must also have real acceleration
        # This stops false positives from
        # just tilting the sensor by hand
        if accel <= 1.5:
            return "NONE"

        # Check if tilt is INCREASING
        # Real rollover = continuously increasing
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

    def _check_speed(self, speed):
        # Detect sudden speed loss
        drop = self.prev_speed - speed

        if drop >= SPEED_DROP_THRESHOLD:
            if drop >= 60:
                return "SEVERE"
            elif drop >= 45:
                return "MODERATE"
            return "MINOR"

        return "NONE"

    def _classify(self, impact, rollover,
                  speed_ev, accel, tilt):
        # Nothing triggered
        if (impact   == "NONE" and
            rollover == "NONE" and
            speed_ev == "NONE"):
            return None

        # Rollover = always severe
        if rollover == "ROLLOVER":
            return {
                "severity": "SEVERE",
                "type":     "ROLLOVER",
                "accel":    accel,
                "tilt":     tilt,
                "reason":   "Vehicle rollover detected"
            }

        # Impact + speed loss = worst case
        if (impact   != "NONE" and
            speed_ev != "NONE"):
            return {
                "severity": "SEVERE",
                "type":     "HIGH SPEED CRASH",
                "accel":    accel,
                "tilt":     tilt,
                "reason":   "Impact and speed loss detected"
            }

        # Pure impact
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

        # Speed only
        if speed_ev != "NONE":
            return {
                "severity": speed_ev,
                "type":     "SPEED CRASH",
                "accel":    accel,
                "tilt":     tilt,
                "reason":   "Sudden speed loss detected"
            }

        return None
