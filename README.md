🚗 CrashGuard System

Smart Accident Detection & Voice-Based Emergency Response

CrashGuard is a real-time accident detection system built using Raspberry Pi that combines motion sensing, GPS tracking, and voice interaction to improve emergency response time after a crash.

The system continuously monitors vehicle movement using an accelerometer and gyroscope. When abnormal motion is detected, it initiates a voice-based interaction with the driver to confirm their condition. Based on the response—or lack of response—it automatically sends an emergency alert with location and incident details.

🔥 Key Features
🚨 Real-time accident detection using motion sensors
🎤 Voice-based driver confirmation system
📍 GPS location tracking
📧 Automatic email alert system
🧠 Smart decision logic (response / no response)
📊 GUI dashboard for live monitoring
📝 Incident logging system

🧩 Hardware Used
Raspberry Pi
MPU6050 Accelerometer + Gyroscope
Neo-6M GPS Module
WM8960 Audio HAT (Mic + Speaker) 

⚙️ Technologies Used
Python 3
Raspberry Pi OS
I2C & UART communication
Speech Recognition
Text-to-Speech (TTS)
Tkinter (GUI) 

🧠 How It Works
The system continuously monitors acceleration and tilt
If abnormal motion is detected → accident suspected
System asks: “Are you okay?”
Driver response is analyzed:
✅ “I am okay” → cancel alert
❌ “Not okay” → send alert
⏳ No response → send alert
GPS location is retrieved
Emergency email is sent with details

📧 Alert Includes
📍 GPS coordinates + Google Maps link
⏱️ Time of incident
⚠️ Severity level
🧾 Incident report

🚀 Future Improvements
GSM module for SMS alerts
Mobile app integration
Cloud-based logging
AI-based crash detection
Camera integration

⚠️ Disclaimer

This is a prototype system designed for educational purposes and may require further testing and optimization for real-world deployment.

⭐ Tagline 

“Detect. Confirm. Respond.”
