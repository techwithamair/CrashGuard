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
            # Set Sample Rate to maximum (0x19)
            self.bus.write_byte_data(self.addr, 0x19, 0)
            # Disable digital low pass filter for speed (0x1A)
            self.bus.write_byte_data(self.addr, 0x1A, 0)
        except Exception as e:
            print(f"Sensor Initialization Error: {e}")

    def _read_raw(self, addr):
        """Read 16-bit raw data from the I2C registers."""
        high = self.bus.read_byte_data(self.addr, addr)
        low = self.bus.read_byte_data(self.addr, addr + 1)
        val = (high << 8) | low
        return val - 65536 if val > 32768 else val

    def get_magnitude(self):
        """Calculate the total G-force magnitude (Resultant Vector)."""
        ax = self._read_raw(0x3B) / 16384.0
        ay = self._read_raw(0x3D) / 16384.0
        az = self._read_raw(0x3F) / 16384.0
        return math.sqrt(ax**2 + ay**2 + az**2)

    def get_tilt(self):
        """Calculate the tilt angle to detect vehicle rollover."""
        ay = self._read_raw(0x3D) / 16384.0
        az = self._read_raw(0x3F) / 16384.0
        return math.degrees(math.atan2(ay, az))
