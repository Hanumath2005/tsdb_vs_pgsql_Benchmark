DROP DATABASE IF EXISTS weather_pg;
DROP DATABASE IF EXISTS weather_ts;

CREATE DATABASE weather_pg;
CREATE DATABASE weather_ts;

\c weather_pg;

CREATE TABLE weather_data (
    time TIMESTAMP,
    temperature DOUBLE PRECISION,
    relative_humidity DOUBLE PRECISION,
    dew_point DOUBLE PRECISION,
    precipitation_mm DOUBLE PRECISION,
    rain_mm DOUBLE PRECISION,
    snowfall_cm DOUBLE PRECISION,
    pressure_msl_hPa DOUBLE PRECISION,
    surface_pressure_hPa DOUBLE PRECISION,
    cloud_cover_pct DOUBLE PRECISION,
    cloud_cover_low_pct DOUBLE PRECISION,
    cloud_cover_mid_pct DOUBLE PRECISION,
    cloud_cover_high_pct DOUBLE PRECISION,
    vapour_pressure_deficit_kPa DOUBLE PRECISION,
    wind_speed_10m_kmh DOUBLE PRECISION,
    wind_direction DOUBLE PRECISION,
    is_day INT
);

\copy weather_data FROM 'path/to/weather.csv' CSV HEADER;


-- 1%
DROP TABLE IF EXISTS weather_1pct;
CREATE TABLE weather_1pct AS
SELECT * FROM weather_data WHERE random() < 0.01;

-- 10%
DROP TABLE IF EXISTS weather_10pct;
CREATE TABLE weather_10pct AS
SELECT * FROM weather_data WHERE random() < 0.10;

-- 25%
DROP TABLE IF EXISTS weather_25pct;
CREATE TABLE weather_25pct AS
SELECT * FROM weather_data WHERE random() < 0.25;

-- 50%
DROP TABLE IF EXISTS weather_50pct;
CREATE TABLE weather_50pct AS
SELECT * FROM weather_data WHERE random() < 0.50;

-- 75%
DROP TABLE IF EXISTS weather_75pct;
CREATE TABLE weather_75pct AS
SELECT * FROM weather_data WHERE random() < 0.75;

-- 100%
DROP TABLE IF EXISTS weather_100pct;
CREATE TABLE weather_100pct AS
SELECT * FROM weather_data;

\c weather_ts;

CREATE EXTENSION IF NOT EXISTS timescaledb;

CREATE TABLE weather_data (
    time TIMESTAMP,
    temperature DOUBLE PRECISION,
    relative_humidity DOUBLE PRECISION,
    dew_point DOUBLE PRECISION,
    precipitation_mm DOUBLE PRECISION,
    rain_mm DOUBLE PRECISION,
    snowfall_cm DOUBLE PRECISION,
    pressure_msl_hPa DOUBLE PRECISION,
    surface_pressure_hPa DOUBLE PRECISION,
    cloud_cover_pct DOUBLE PRECISION,
    cloud_cover_low_pct DOUBLE PRECISION,
    cloud_cover_mid_pct DOUBLE PRECISION,
    cloud_cover_high_pct DOUBLE PRECISION,
    vapour_pressure_deficit_kPa DOUBLE PRECISION,
    wind_speed_10m_kmh DOUBLE PRECISION,
    wind_direction DOUBLE PRECISION,
    is_day INT
);

SELECT create_hypertable('weather_data', 'time', if_not_exists => TRUE);
    

\copy weather_data FROM 'path/to/weather.csv' CSV HEADER;


-- 1%
DROP TABLE IF EXISTS weather_1pct;
CREATE TABLE weather_1pct AS
SELECT * FROM weather_data WHERE random() < 0.01;
SELECT create_hypertable('weather_1pct', 'time', if_not_exists => TRUE, migrate_data => TRUE);

-- 10%
DROP TABLE IF EXISTS weather_10pct;
CREATE TABLE weather_10pct AS
SELECT * FROM weather_data WHERE random() < 0.10;
SELECT create_hypertable('weather_10pct', 'time', if_not_exists => TRUE, migrate_data => TRUE);

-- 25%
DROP TABLE IF EXISTS weather_25pct;
CREATE TABLE weather_25pct AS
SELECT * FROM weather_data WHERE random() < 0.25;
SELECT create_hypertable('weather_25pct', 'time', if_not_exists => TRUE, migrate_data => TRUE);

-- 50%
DROP TABLE IF EXISTS weather_50pct;
CREATE TABLE weather_50pct AS
SELECT * FROM weather_data WHERE random() < 0.50;
SELECT create_hypertable('weather_50pct', 'time', if_not_exists => TRUE, migrate_data => TRUE);

-- 75%
DROP TABLE IF EXISTS weather_75pct;
CREATE TABLE weather_75pct AS
SELECT * FROM weather_data WHERE random() < 0.75;
SELECT create_hypertable('weather_75pct', 'time', if_not_exists => TRUE, migrate_data => TRUE);

-- 100%
DROP TABLE IF EXISTS weather_100pct;
CREATE TABLE weather_100pct AS
SELECT * FROM weather_data;
SELECT create_hypertable('weather_100pct', 'time', if_not_exists => TRUE, migrate_data => TRUE);



DROP DATABASE IF EXISTS synthetic_pg;
DROP DATABASE IF EXISTS synthetic_ts;

CREATE DATABASE synthetic_pg;
CREATE DATABASE synthetic_ts;

\c synthetic_pg;

CREATE TABLE synthetic_data (
    time TIMESTAMP,
    device_id INT,
    temperature DOUBLE PRECISION,
    humidity DOUBLE PRECISION,
    pressure DOUBLE PRECISION,
    battery_voltage DOUBLE PRECISION,
    status TEXT
);

\copy synthetic_data FROM 'path/to/synthetic.csv' CSV HEADER;

\c synthetic_ts;

CREATE EXTENSION IF NOT EXISTS timescaledb;

CREATE TABLE synthetic_data (
    time TIMESTAMP,
    device_id INT,
    temperature DOUBLE PRECISION,
    humidity DOUBLE PRECISION,
    pressure DOUBLE PRECISION,
    battery_voltage DOUBLE PRECISION,
    status TEXT
);

SELECT create_hypertable('synthetic_data', 'time', if_not_exists => TRUE);


\copy synthetic_data FROM 'path/to/synthetic.csv' CSV HEADER;


DROP DATABASE IF EXISTS nyc_pg;
DROP DATABASE IF EXISTS nyc_ts;

CREATE DATABASE nyc_pg;
CREATE DATABASE nyc_ts;

\c nyc_pg;

CREATE TABLE nyc_data (
    VendorID INT,
    tpep_pickup_datetime TIMESTAMP,
    tpep_dropoff_datetime TIMESTAMP,
    passenger_count INT,
    trip_distance DOUBLE PRECISION,
    pickup_longitude DOUBLE PRECISION,
    pickup_latitude DOUBLE PRECISION,
    RateCodeID INT,
    store_and_fwd_flag TEXT,
    dropoff_longitude DOUBLE PRECISION,
    dropoff_latitude DOUBLE PRECISION,
    payment_type INT,
    fare_amount DOUBLE PRECISION,
    extra DOUBLE PRECISION,
    mta_tax DOUBLE PRECISION,
    tip_amount DOUBLE PRECISION,
    tolls_amount DOUBLE PRECISION,
    improvement_surcharge DOUBLE PRECISION,
    total_amount DOUBLE PRECISION
);

\copy nyc_data FROM 'path/to/nyc_data.csv' CSV HEADER;

\c nyc_ts;

CREATE EXTENSION IF NOT EXISTS timescaledb;

CREATE TABLE nyc_data (
    VendorID INT,
    tpep_pickup_datetime TIMESTAMP,
    tpep_dropoff_datetime TIMESTAMP,
    passenger_count INT,
    trip_distance DOUBLE PRECISION,
    pickup_longitude DOUBLE PRECISION,
    pickup_latitude DOUBLE PRECISION,
    RateCodeID INT,
    store_and_fwd_flag TEXT,
    dropoff_longitude DOUBLE PRECISION,
    dropoff_latitude DOUBLE PRECISION,
    payment_type INT,
    fare_amount DOUBLE PRECISION,
    extra DOUBLE PRECISION,
    mta_tax DOUBLE PRECISION,
    tip_amount DOUBLE PRECISION,
    tolls_amount DOUBLE PRECISION,
    improvement_surcharge DOUBLE PRECISION,
    total_amount DOUBLE PRECISION
);

SELECT create_hypertable('nyc_data', 'tpep_pickup_datetime', if_not_exists => TRUE);

\copy nyc_data FROM 'path/to/nyc_data.csv' CSV HEADER;
