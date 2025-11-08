# Benchmark Setup

This phase focuses on setting up **PostgreSQL** and the **TimescaleDB extension** on Ubuntu, along with preparing the **datasets** required for benchmarking time-series database performance.

## 1. Installation procedure

### **Step 1: Install PostgreSQL**
Before installing, ensure your system is up to date. In our benchmark, PostgreSQL serves as baseline 
```bash
sudo apt install postgresql postgresql-contrib -y
```

For verifying installation and login
```bash
sudo systemctl status postgresql
sudo -u postgres psql
```
### **Step 2: Install TimescaleDB Extension**
TimescalDB is a time-series database built as a PostgreSQL extension, optimized for storing and querying large volumes of time-stamped data.

Initially add timescale’s official APT repository
```bash
sudo apt install wget gnupg -y
wget --quiet -O - https://packagecloud.io/timescale/timescaledb/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/timescaledb.gpg
echo "deb [signed-by=/usr/share/keyrings/timescaledb.gpg] https://packagecloud.io/timescale/timescaledb/ubuntu/ $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/timescaledb.list
sudo apt update
```

Install the TimescaleDB extension (for PostgreSQL 16) and tune the extension according to the database and restart the postgreSQL shell.
```bash
sudo apt install timescaledb-2-postgresql-16 -y
sudo timescaledb-tune
sudo systemctl restart postgresql
```

## 2. Datasets

The datasets that are used in this benchmark both real-time and synthetic datasets which include [nyc_dataset](https://www.kaggle.com/datasets/elemento/nyc-yellow-taxi-trip-data), [weather_dataset](https://www.kaggle.com/datasets/parthdande/) and synthetic dataset that was created using the script in

```bash
datasets/synthetic_iot/synthetic_data_genration.py
```

The characteristics of the datasets are present in the below table
| Dataset Name         | Rows (approx.) | Columns | Source         | Type       |
| -------------------- | -------------- | ------- | -------------- | ---------- |
| Weather Dataset      | 380,000+        | 5       | Kaggle         | Real-world |
| NYC Yellow Taxi Data | 30M+           | 18+     | Kaggle         | Real-world |
| Synthetic IoT Data   | 4,000,000      | 7       | Local (Python) | Synthetic  |

For benchmarking two databases per dataset are used
```bash
weather:
weather_pg(postgreSQL)
weather_ts(timescaleDB)

nyc_dataset:
nyc_pg(postgreSQL)
nyc_ts(timescaleDB)

synthetic_dataset:
synthetic_pg(postgreSQL)
synthetic_ts(timescaleDB)
```

After creating a databases, tables are created using the command:

```bash
CREATE TABLE weather_data (
    time TIMESTAMP NOT NULL,
    temperature DOUBLE PRECISION,
    relative_humidity DOUBLE PRECISION,
    dew_point DOUBLE PRECISION,
    precipitation_mm DOUBLE PRECISION,
    rain_mm DOUBLE PRECISION,
    snowfall_cm DOUBLE PRECISION,
    pressure_msl_hpa DOUBLE PRECISION,
    surface_pressure_hpa DOUBLE PRECISION,
    cloud_cover DOUBLE PRECISION,
    cloud_cover_low DOUBLE PRECISION,
    cloud_cover_mid DOUBLE PRECISION,
    cloud_cover_high DOUBLE PRECISION,
    vapour_pressure_deficit DOUBLE PRECISION,
    wind_speed_10m DOUBLE PRECISION,
    wind_direction DOUBLE PRECISION,
    is_day BOOLEAN
);
```

For enabling timescale extension use the command:
```bash
SELECT create_hypertable('weather_data', 'time');
```


The complete setup is present at setup.sql
