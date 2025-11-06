import csv
import random
from datetime import datetime, timedelta

NUM_DEVICES = 200
ROWS_PER_DEVICE = 20000
OUTPUT_FILE = "synthetic_iot_dataset.csv"
START_TIME = datetime(2024, 1, 1, 0, 0, 0)

def random_status():
    return random.choices(["OK", "WARN", "FAIL"], weights=[0.85, 0.1, 0.05])[0]

def generate_row(device_id, time):
    temperature = round(random.uniform(15, 40), 2)
    humidity = round(random.uniform(30, 95), 2)
    pressure = round(random.uniform(980, 1050), 2)
    battery_voltage = round(random.uniform(3.2, 4.2), 2)
    status = random_status()
    return [time, device_id, temperature, humidity, pressure, battery_voltage, status]

def generate_device_data(device_id, writer):
    time = START_TIME
    for _ in range(ROWS_PER_DEVICE):
        row = generate_row(device_id, time)
        writer.writerow(row)
        time += timedelta(seconds=30)

def generate_iot_dataset():
    total_rows = NUM_DEVICES * ROWS_PER_DEVICE
    print(f"Generating IoT dataset: {total_rows:,} rows...")
    print("This may take ~2–4 minutes depending on your CPU speed.")

    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["time", "device_id", "temperature", "humidity", "pressure", "battery_voltage", "status"])

        for device_id in range(1, NUM_DEVICES + 1):
            generate_device_data(device_id, writer)


if __name__ == "__main__":
    generate_iot_dataset()
