# Phase 3: Scalability Benchmark — PostgreSQL vs TimescaleDB

## Objective

This phase evaluates the **scalability and performance behavior** of PostgreSQL and TimescaleDB when query workloads are executed on datasets of increasing size.

The benchmark measures **query latency trends** across scaled subsets of the data to analyze how efficiently each database handles growth in data volume.

---

The database was scaled to different percentages of its original size to test scalability:

```bash
1%, 10%, 25%, 50%, 75%, and 100%
```

For each scale, identical queries were executed on both PostgreSQL and TimescaleDB.

## Benchmarking Workflow

The main benchmarking script (scalability_benchmark.py) automates the entire process:

1. Configuration

- Databases defined in the DBS dictionary:
```python
DBS = {
    "pg": {"dbname": "weather_pg", "user": "postgres", "host": "/var/run/postgresql"},
    "ts": {"dbname": "weather_ts", "user": "postgres", "host": "/var/run/postgresql"}
}
```
- Queries are loaded from queries.json (weather section is only used for scaling).
- Scaling factors: [1, 10, 25, 50, 75, 100]
- Each query is executed 10 times (RUNS = 10) per scale.

2. Query Execution Process
- For each combination of database, scale, and query:
- The code dynamically substitutes the correct scaled table name (e.g., weather_10pct).
- For the first run, system caches are dropped using:

```bash
echo 3 > /proc/sys/vm/drop_caches
```
to simulate cold-cache behavior.
- Each query is executed 10 times using psycopg2.
- The execution time (ms) and row count are logged to CSV:
```pgsql
timestamp, db, scale, query_name, run_index, elapsed_ms, row_count
```
- Median and mean latencies are displayed for each query.

3. Results Storage
- All raw results are stored in [results](results/)