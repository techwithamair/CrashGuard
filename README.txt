# CrashGuard System
Smart Accident Detection and Emergency Response

## Files
- main.py           → Entry point run this
- config.py         → All settings here
- sensor_mpu6050.py → MPU6050 sensor reading
- gps_reader.py     → NEO-6M GPS reading
- detector.py       → False positive filtering
- voice_system.py   → WM8960 speak and listen
- alert_sender.py   → Email and Telegram alerts
- map_display.py    → Folium map generation
- logger.py         → CSV event logging
- gui.py            → Tkinter dashboard

## Setup
1. bash install.sh
2. Edit config.py
3. python3 main.py

## Thresholds
Minor:    2.5g
Moderate: 3.5g
Severe:   5.0g
Tilt:     45 degrees
Speed drop: 30 mph
