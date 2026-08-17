"""
Raspberry Pi CPU Temperature Monitoring System
------------------------------------------------
Reads the Pi's onboard CPU temperature at regular intervals,
logs it with a timestamp to a CSV file, and raises an alert
if temperature crosses a defined threshold.
"""

import subprocess
import csv
import time
from datetime import datetime

LOG_FILE = "temperature_log.csv"
THRESHOLD_TEMP = 60.0   # in Celsius - adjust as needed
READ_INTERVAL = 5       # seconds between readings


def get_cpu_temperature():
    """Reads CPU temperature using Raspberry Pi's vcgencmd tool."""
    try:
        output = subprocess.check_output(["vcgencmd", "measure_temp"]).decode()
        # Output format: temp=45.6'C
        temp_str = output.replace("temp=", "").replace("'C\n", "")
        return float(temp_str)
    except Exception as e:
        print(f"Error reading temperature: {e}")
        return None


def log_temperature(timestamp, temp):
    """Appends a temperature reading to the CSV log file."""
    file_exists = False
    try:
        with open(LOG_FILE, "r"):
            file_exists = True
    except FileNotFoundError:
        pass

    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "Temperature (C)", "Status"])
        status = "ALERT" if temp is not None and temp >= THRESHOLD_TEMP else "OK"
        writer.writerow([timestamp, temp, status])


def monitor():
    print("Starting CPU Temperature Monitoring System...")
    print(f"Threshold set at {THRESHOLD_TEMP}°C | Logging to {LOG_FILE}\n")

    try:
        while True:
            temp = get_cpu_temperature()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if temp is not None:
                status = "ALERT: HIGH TEMPERATURE" if temp >= THRESHOLD_TEMP else "NORMAL"
                print(f"[{timestamp}] Temp: {temp}°C -> {status}")
                log_temperature(timestamp, temp)

            time.sleep(READ_INTERVAL)

    except KeyboardInterrupt:
        print("\nMonitoring stopped by user. Log saved to", LOG_FILE)


if __name__ == "__main__":
    monitor()
