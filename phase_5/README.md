# Phase 5: Compression & Continuous Aggregates Benchmark — PostgreSQL vs TimescaleDB

This phase evaluates **storage and query performance optimizations** in **TimescaleDB** compared to standard **PostgreSQL**, focusing on two advanced time-series database features:

1. **Compression** — Reduces storage size and improves query performance on historical data.  
2. **Continuous Aggregates** — Provides real-time precomputed aggregations (similar to PostgreSQL materialized views, but automatically maintained).

---

## Objectives

The goal of this phase is to:

- Measure the **impact of compression** on query latency and storage size in TimescaleDB.  
- Compare **TimescaleDB continuous aggregates** with **PostgreSQL materialized views** in terms of creation and query performance.  
- Quantify differences in **storage efficiency** and **query performance** between:
  - **PostgreSQL** (baseline)
  - **TimescaleDB (uncompressed)**
  - **TimescaleDB (compressed)**
  - **Continuous Aggregates / Materialized Views**


## Experimental Setup

The benchmark uses two databases:

| Database | Description |
|-----------|--------------|
| `weather_pg` | PostgreSQL database (baseline) |
| `weather_ts` | TimescaleDB database with hypertables enabled |

Hypertable creation (for TimescaleDB):
```sql
SELECT create_hypertable('weather_data_dup', 'time', if_not_exists => TRUE);
```

## Benchmark Configuration

| Parameter           | Description                                                            |
| ------------------- | ---------------------------------------------------------------------- |
| `RUNS`              | 10 query executions per test                                           |
| `RESULTS_DIR`       | Directory to store CSVs and plots                                      |
| `QUERIES`           | SQL query set (`queries.json`)                                         |
| `DBS`               | Database connection dictionary for PG and TS                           |
| `utils.run_query()` | Helper function to execute queries and return elapsed time + row count |

- It performs three sub-benchmarks for each database:
    1. Baseline Queries
    2. Compression
    3. Continuous Aggregates / Materialized Views

## Compression Evaluation (TimescaleDB only)
- Compression is applied to the Timescale hypertable:
```sql
ALTER TABLE weather_data_dup SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'time'
);

SELECT compress_chunk(i) FROM show_chunks('weather_data_dup') i;
```

- After compression:
    1. Queries are rerun to measure performance improvements.
    2. Compression typically reduces storage and speeds up scans on large historical data.
    3. Storage size before and after compression is collected via:
```sql
SELECT table_name, pg_total_relation_size(table_name)
FROM information_schema.tables
WHERE table_name = 'weather_data_dup';
```

## Continuous Aggregates vs Materialized Views
- Each database creates an aggregated hourly temperature view:

### TimescaleDB Continuous Aggregate

```sql
CREATE MATERIALIZED VIEW daily_avg_temp
WITH (timescaledb.continuous) AS
SELECT time_bucket('1 hour', time) AS hour, AVG(temperature) AS avg_temp
FROM weather_small GROUP BY hour WITH DATA;
```

### PostgreSQL Materialized View

```sql
CREATE MATERIALIZED VIEW daily_avg_temp AS
SELECT date_trunc('hour', time) AS hour, AVG(temperature) AS avg_temp
FROM weather_small GROUP BY hour;
```

- A test query is of the form
```sql
SELECT * FROM daily_avg_temp LIMIT 100;
```

- This measures the query latency of pre-aggregated data retrieval.