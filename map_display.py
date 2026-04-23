# ─────────────────────────────────────
# CrashGuard System - map_display.py
# FEATURE 1: MAP DISPLAY WITH FOLIUM
#
# Generates an interactive HTML map
# showing exact accident location
# with red pin and info popup
# Opens in any browser
# ─────────────────────────────────────

import folium
from datetime import datetime
from config import MAP_OUTPUT_FILE

def generate_map(lat, lon, severity,
                 speed, accel, tilt):
    try:
        # Create map centered on accident
        accident_map = folium.Map(
            location=[lat, lon],
            zoom_start=16,
            tiles="OpenStreetMap"
        )

        # Popup info shown when pin clicked
        popup_text = f"""
        <div style="font-family:Arial;
                    font-size:14px;
                    padding:10px;
                    min-width:200px">
            <h3 style="color:red;margin:0">
                🚨 ACCIDENT DETECTED
            </h3>
            <hr/>
            <b>Severity:</b> {severity}<br/>
            <b>Time:</b> {datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )}<br/>
            <b>Speed:</b> {speed:.1f} mph<br/>
            <b>Acceleration:</b> {accel:.2f}g<br/>
            <b>Tilt:</b> {tilt:.1f} degrees<br/>
            <hr/>
            <b>Coordinates:</b><br/>
            {lat:.6f}, {lon:.6f}
        </div>
        """

        # Add red marker at accident location
        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(
                popup_text,
                max_width=280
            ),
            tooltip=f"🚨 {severity} Accident",
            icon=folium.Icon(
                color="red",
                icon="exclamation-sign",
                prefix="glyphicon"
            )
        ).add_to(accident_map)

        # Add circle around accident area
        folium.Circle(
            location=[lat, lon],
            radius=50,
            color="red",
            fill=True,
            fill_color="red",
            fill_opacity=0.2,
            tooltip="Accident zone"
        ).add_to(accident_map)

        # Save map as HTML file
        accident_map.save(MAP_OUTPUT_FILE)
        print(f"Map saved: {MAP_OUTPUT_FILE}")
        return True

    except Exception as e:
        print(f"Map generation failed: {e}")
        return False
