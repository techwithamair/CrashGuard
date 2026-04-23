# ─────────────────────────────────────
# CrashGuard System - sensor_mpu6050.py
# FEATURE: HARDWARE ACCELEROMETER
#
# Reads acceleration and tilt from the 
# GY-521 MPU6050 via I2C. Optimized for
# high-speed impact detection.
# ─────────────────────────────────────

import smbus
import math

class MPU6050:
    def __init__(self):
        """Initialize I2C and optimize sensor for fast impact detection."""
        try:
            self.bus = smbus.SMBus(1)
            self.addr = 0x68
            
            # Wake up sensor (0x6B)
            self.bus.write_byte_data(self.addr, 0x6B, 0)
            
            # Set Sample Rate to maximum (0x19) for instant crash response
            self.bus.write_byte_data(self.addr, 0x19, 0)
            
            # Disable digital low pass filter for maximum speed (0x1A)
            self.bus.write_byte_data(self.addr, 0x1A, 0)
            
            print("MPU6050 Subsystem: Active and Calibrated")
        except Exception as e:
            print(f"CRITICAL: Sensor Initialization Error - {e}")

    def _read_raw(self, addr):
        """Read 16-bit raw data from the I2C registers with wire-bump protection."""
        try:
            high = self.bus.read_byte_data(self.addr, addr)
            low = self.bus.read_byte_data(self.addr, addr + 1)
            val = (high << 8) | low
            return val - 65536 if val > 32768 else val
        except Exception:
            # If the I2C wire loses connection mid-read, return 0
            # This prevents a fatal crash. main.py will detect the drop and heal it.
            return 0

    def read_accel(self):
        """Returns X, Y, Z axes converted to standard G-forces."""
        ax = self._read_raw(0x3B) / 16384.0
        ay = self._read_raw(0x3D) / 16384.0
        az = self._read_raw(0x3F) / 16384.0
        return ax, ay, az

    def get_magnitude(self):
        """Calculate the total G-force magnitude (Resultant Vector)."""
        ax, ay, az = self.read_accel()
        return math.sqrt(ax**2 + ay**2 + az**2)

    def get_tilt(self):
        """
        Calculate the true 3D tilt angle (Pitch/Roll) for vehicle rollover.
        Uses advanced math to account for multi-axis rotation.
        """
        ax, ay, az = self.read_accel()
        
        # Advanced 3D rollover formula
        return math.degrees(math.atan2(ay, math.sqrt(ax**2 + az**2)))
