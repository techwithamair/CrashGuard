# ─────────────────────────────────────
# CrashGuard System - config.py
# ─────────────────────────────────────

# Accident detection thresholds
ACCIDENT_THRESHOLD   = 2.5   # g minor
MODERATE_THRESHOLD   = 3.5   # g moderate
SEVERE_THRESHOLD     = 5.0   # g severe
TILT_THRESHOLD       = 45    # degrees rollover
SPEED_DROP_THRESHOLD = 30    # mph sudden loss

# False positive filter
# How many readings before confirming accident
CONFIRM_READINGS     = 3

# Voice response timeout seconds
RESPONSE_TIMEOUT     = 10

# GPS settings (Kept for module compatibility)
GPS_PORT             = "/dev/serial0"
GPS_BAUDRATE         = 9600

# Alert contacts (TELEGRAM REMOVED)
EMAIL_FROM           = "your_email@gmail.com"
EMAIL_PASSWORD       = "your_16_digit_app_password"
EMAIL_TO             = "emergency@contact.com"

# Storage and Output
MAP_OUTPUT_FILE      = "accident_map.html"
LOG_FILE             = "accident_log.csv"
