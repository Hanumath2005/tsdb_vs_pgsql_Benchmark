# Phase 2: Benchmark Query Latency — PostgreSQL vs TimescaleDB

In this phase, we benchmark **query execution latency** for three datasets across **PostgreSQL** and **TimescaleDB** databases.  
The objective is to measure how well TimescaleDB’s time-series optimizations improve query performance compared to vanilla PostgreSQL.

---

## Overview

For each dataset (`weather`, `nyc`, and `synthetic`):
- Two databases are created:
  - **PostgreSQL** version (e.g., `nyc_pg`)
  - **TimescaleDB** version (e.g., `nyc_ts`)
- A **hypertable** is created in the TimescaleDB version using the time column:
  ```sql
  SELECT create_hypertable('nyc_data', 'tpep_pickup_datetime', if_not_exists => TRUE);
- Each dataset has a corresponding set of queries that cover a variety of SQL operations (aggregations, filters, time-bucketing, group-by, and window queries).
These queries are defined in [benchmark_queries.py](benchmark_queries.py)

- The results of this benchmark are stored in the [results](results) folder

## What the Benchmark Code Does for Each Query

For every query defined in the dataset:

1. **Drops system caches** before the first run using 
   ```bash
   echo 3 > /proc/sys/vm/drop_caches
    ```
    to simulate a cold-cache environment (disk read latency included).
2. **Runs the same SQL query 10 times (RUNS = 10)** for obtaining central latency over runs.
3. **For each run**:
    - Measures execution time (in milliseconds) using Python’s time module.
    - Executes the query through a PostgreSQL connection (psycopg2).
    - Retrieves the number of rows returned.
    - Logs results to a CSV file in the format:
    ```sql
    timestamp, db, query_name, run_index, elapsed_ms, rowcount
    ```
4. Before executing the query, it also captures the execution plan using
    ```sql
    EXPLAIN (ANALYZE, BUFFERS)
    ```
    and saves it in the [results](results/)
5. After all runs:
    - Computes average, median, and standard deviation of latency.
    - Results are stored in per-query CSV files, and later summarized visually using plot_generation.py.