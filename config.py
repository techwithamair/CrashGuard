# ─────────────────────────────────────
# CrashGuard System - config.py
# All settings in one place (Email Only)
# ─────────────────────────────────────

# Accident detection thresholds
ACCIDENT_THRESHOLD   = 1.2   # g minor
MODERATE_THRESHOLD   = 1.5   # g moderate
SEVERE_THRESHOLD     = 2.0   # g severe
TILT_THRESHOLD       = 30    # degrees rollover
SPEED_DROP_THRESHOLD = 30    # mph sudden loss

# False positive filter
# How many consecutive readings before confirming accident
CONFIRM_READINGS     = 3

# Voice response timeout seconds
RESPONSE_TIMEOUT     = 10

# GPS serial port
GPS_PORT             = "/dev/serial0"
GPS_BAUDRATE         = 9600

# Alert contacts (Email Only)
EMAIL_FROM           = "your_email@gmail.com"
EMAIL_PASSWORD       = "your_app_password"
EMAIL_TO             = "emergency@contact.com"

# Map output file
MAP_OUTPUT_FILE      = "accident_map.html"
LOG_FILE             = "accident_log.csv"
