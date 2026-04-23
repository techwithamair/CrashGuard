# ─────────────────────────────────────
# CrashGuard System - sensor_mpu6050.py
# Reads acceleration and tilt from
# GY-521 MPU6050 via I2C
# ─────────────────────────────────────

import smbus
import math

MPU_ADDR   = 0x68
PWR_MGMT_1 = 0x6B

class MPU6050:
    def __init__(self, bus_id=1):
        self.bus = smbus.SMBus(bus_id)
        # Wake up sensor
        self.bus.write_byte_data(
            MPU_ADDR, PWR_MGMT_1, 0
        )
        # Maximum sample rate
        self.bus.write_byte_data(
            MPU_ADDR, 0x19, 0
        )
        # Disable low pass filter
        # for fastest impact response
        self.bus.write_byte_data(
            MPU_ADDR, 0x1A, 0
        )
        print("MPU6050 initialized")

    def _read_raw(self, addr):
        high = self.bus.read_byte_data(
            MPU_ADDR, addr
        )
        low  = self.bus.read_byte_data(
            MPU_ADDR, addr + 1
        )
        val  = (high << 8) | low
        if val > 32768:
            val -= 65536
        return val

    def read_accel(self):
        ax = self._read_raw(0x3B) / 16384.0
        ay = self._read_raw(0x3D) / 16384.0
        az = self._read_raw(0x3F) / 16384.0
        return ax, ay, az

    def get_magnitude(self):
        ax, ay, az = self.read_accel()
        return math.sqrt(
            ax**2 + ay**2 + az**2
        )

    def get_tilt(self):
        ax, ay, az = self.read_accel()
        return math.degrees(
            math.atan2(
                ay,
                math.sqrt(ax**2 + az**2)
            )
        )

    def get_all(self):
        ax, ay, az = self.read_accel()
        magnitude = math.sqrt(
            ax**2 + ay**2 + az**2
        )
        tilt = math.degrees(
            math.atan2(
                ay,
                math.sqrt(ax**2 + az**2)
            )
        )
        return magnitude, tilt
