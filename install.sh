#!/bin/bash
# ─────────────────────────────────────
# CrashGuard System - install.sh
# Run this once to set everything up
# sudo bash install.sh
# ─────────────────────────────────────

echo "Installing CrashGuard dependencies..."

# Update system
sudo apt update && sudo apt upgrade -y

# System packages
sudo apt install -y \
    python3-pip \
    python3-tk \
    python3-pyaudio \
    python3-smbus \
    i2c-tools \
    espeak \
    flac \
    git \
    unzip \
    wget

# Python packages
pip3 install \
    pynmea2 \
    pyserial \
    SpeechRecognition \
    pyttsx3 \
    vosk \
    requests \
    folium

# Install WM8960 Audio HAT driver
echo "Installing WM8960 driver..."
cd /home/pi
git clone https://github.com/waveshare/WM8960-Audio-HAT
cd WM8960-Audio-HAT
sudo ./install.sh
cd ..

# Download Vosk small English model
echo "Downloading Vosk offline model (50MB)..."
wget -q https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
unzip -q vosk-model-small-en-us-0.15.zip
rm vosk-model-small-en-us-0.15.zip

echo ""
echo "Installation complete!"
echo ""
echo "Next steps:"
echo "1. Enable I2C: sudo raspi-config"
echo "   Interface Options > I2C > Enable"
echo "2. Enable Serial: sudo raspi-config"
echo "   Interface Options > Serial Port"
echo "   Login shell: NO"
echo "   Serial hardware: YES"
echo "3. Edit config.py with your:"
echo "   - Telegram token and chat ID"
echo "   - Gmail address and app password"
echo "   - Emergency contact email"
echo "4. Reboot: sudo reboot"
echo "5. Run: python3 main.py"
