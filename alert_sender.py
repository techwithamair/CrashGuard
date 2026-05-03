# ─────────────────────────────────────
# CrashGuard System - alert_sender.py
# FEATURE: SMART EMAIL WITH MAPS LINK
#
# Sends professional emergency HTML email
# with clickable Google Maps link
# and full accident details.
# ─────────────────────────────────────


import smtplib
import threading
from datetime import datetime
from email.mime.text      import MIMEText
from email.mime.multipart import MIMEMultipart
from config import (
    EMAIL_FROM,
    EMAIL_PASSWORD,
    EMAIL_TO
)

def send_email(severity, lat, lon,
               accel, tilt, reason):
    if lat and lon:
        maps_link = (
            f"https://maps.google.com"
            f"/?q={lat},{lon}"
        )
        coords = f"{lat:.6f}, {lon:.6f}"
    else:
        maps_link = "Location unavailable"
        coords    = "Not available"

    now = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    color_map = {
        "SEVERE":   "#cc0000",
        "MODERATE": "#ff6600",
        "MINOR":    "#ffaa00"
    }
    color = color_map.get(severity, "#cc0000")

    html_body = f"""
    <html>
    <body style="font-family:Arial,sans-serif;
                 max-width:600px;
                 margin:0 auto;padding:20px;">

        <div style="background:{color};
                    color:white;padding:20px;
                    border-radius:8px;
                    text-align:center;">
            <h1 style="margin:0">
                ACCIDENT DETECTED
            </h1>
            <h2 style="margin:5px 0">
                Severity: {severity}
            </h2>
        </div>

        <div style="background:#f5f5f5;
                    padding:20px;margin-top:15px;
                    border-radius:8px;">
            <h3>Accident Details</h3>
            <table style="width:100%;
                          border-collapse:collapse;">
                <tr>
                    <td style="padding:8px;
                               font-weight:bold;">
                        Time
                    </td>
                    <td style="padding:8px;">
                        {now}
                    </td>
                </tr>
                <tr style="background:#ebebeb;">
                    <td style="padding:8px;
                               font-weight:bold;">
                        Severity
                    </td>
                    <td style="padding:8px;
                               color:{color};
                               font-weight:bold;">
                        {severity}
                    </td>
                </tr>
                <tr>
                    <td style="padding:8px;
                               font-weight:bold;">
                        Type
                    </td>
                    <td style="padding:8px;">
                        {reason}
                    </td>
                </tr>
                <tr style="background:#ebebeb;">
                    <td style="padding:8px;
                               font-weight:bold;">
                        Acceleration
                    </td>
                    <td style="padding:8px;">
                        {accel:.2f}g
                    </td>
                </tr>
                <tr>
                    <td style="padding:8px;
                               font-weight:bold;">
                        Tilt angle
                    </td>
                    <td style="padding:8px;">
                        {tilt:.1f} degrees
                    </td>
                </tr>
                <tr style="background:#ebebeb;">
                    <td style="padding:8px;
                               font-weight:bold;">
                        Coordinates
                    </td>
                    <td style="padding:8px;">
                        {coords}
                    </td>
                </tr>
            </table>
        </div>

        <div style="text-align:center;
                    margin-top:20px;">
            <a href="{maps_link}"
               style="background:#cc0000;
                      color:white;
                      padding:15px 30px;
                      text-decoration:none;
                      border-radius:8px;
                      font-size:18px;
                      font-weight:bold;">
                VIEW LOCATION ON MAP
            </a>
        </div>

        <div style="margin-top:20px;
                    padding:15px;
                    background:#fff3f3;
                    border-left:4px solid {color};
                    border-radius:4px;">
            <p style="margin:0;font-size:14px;
                      color:#555;">
                This is an automated alert from
                CrashGuard. Please contact
                emergency services if needed.
            </p>
        </div>
    </body>
    </html>
    """

    plain_body = (
        f"ACCIDENT DETECTED!\n\n"
        f"Severity: {severity}\n"
        f"Type: {reason}\n"
        f"Time: {now}\n"
        f"Acceleration: {accel:.2f}g\n"
        f"Tilt: {tilt:.1f} degrees\n\n"
        f"LOCATION:\n{maps_link}\n\n"
        f"Please send help immediately!"
    )

    try:
        msg            = MIMEMultipart("alternative")
        msg["From"]    = EMAIL_FROM
        msg["To"]      = EMAIL_TO
        msg["Subject"] = (
            f"ACCIDENT ALERT - "
            f"{severity} | CrashGuard"
        )

        msg.attach(MIMEText(plain_body, "plain"))
        msg.attach(MIMEText(html_body,  "html"))

        server = smtplib.SMTP(
            "smtp.gmail.com", 587
        )
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("Email sent!")

    except Exception as e:
        print(f"Email failed: {e}")

def send_all_alerts(severity, lat, lon,
                    accel, tilt, reason):
    t1 = threading.Thread(
        target=send_email,
        args=(
            severity, lat, lon,
            accel, tilt, reason
        ),
        daemon=True
    )
    t1.start()
