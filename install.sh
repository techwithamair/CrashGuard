#!/bin/bash
# ──────────────────────────────────────────────────────────
# CrashGuard System - Final Expo Setup Script
# Run this once on your Raspberry Pi: sudo bash install.sh
# ──────────────────────────────────────────────────────────

echo "🚀 Starting CrashGuard Pro Installation..."

# 1. Update the System
echo "🔄 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# 2. Install System Dependencies
echo "📦 Installing system dependencies..."
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

# 3. Install Python Libraries
echo "🐍 Installing Python libraries..."
pip3 install \
    pynmea2 \
    p_serial \
    SpeechRecognition \
    pyttsx3 \
    vosk \
    requests

# 4. Install WM8960 Audio HAT Drivers
echo "🔊 Installing WM8960 Audio HAT drivers..."
if [ ! -d "WM8960-Audio-HAT" ]; then
    git clone https://github.com/waveshare/WM8960-Audio-HAT
fi
cd WM8960-Audio-HAT
sudo ./install.sh
cd ..

# 5. Download and Setup Vosk Voice Model
echo "🧠 Downloading Vosk Offline Voice Model..."
MODEL_URL="https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"
MODEL_NAME="vosk-model-small-en-us-0.15"

if [ ! -d "$MODEL_NAME" ]; then
    wget -q $MODEL_URL
    unzip -q "${MODEL_NAME}.zip"
    rm "${MODEL_NAME}.zip"
    echo "✅ Voice model installed successfully."
else
    echo "ℹ️ Voice model already exists. Skipping."
fi

echo ""
echo "──────────────────────────────────────────────────────────"
echo "✅ INSTALLATION COMPLETE!"
echo "──────────────────────────────────────────────────────────"
echo "NEXT STEPS:"
echo "1. Run 'sudo raspi-config' to enable I2C."
echo "2. Edit 'config.py' with your Gmail App Password."
echo "3. Run 'alsamixer' to turn up the Speaker & Mic volume."
echo "4. REBOOT YOUR PI NOW: sudo reboot"
echo "──────────────────────────────────────────────────────────"
