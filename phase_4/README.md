# Phase 4: Concurrency & Throughput Benchmark — PostgreSQL vs TimescaleDB

In **Phase 4**, benchmark the **concurrency performance and throughput** of **PostgreSQL** and **TimescaleDB** when executing multiple queries simultaneously.  
The objective is to understand how well each database scales under **multi-client load**, using the `weather_100pct` dataset as the benchmark table.


## Objective

This phase evaluates:
- **Concurrency scaling** — how query latency changes as the number of simultaneous clients increases.
- **Throughput performance** — how many queries per second (QPS) each database can execute under increasing parallelism.

We compare two databases:
- `weather_pg` → PostgreSQL
- `weather_ts` → TimescaleDB (with hypertable on the `time` column)


## Hypertable Setup

The TimescaleDB database uses a **hypertable** for efficient time-series partitioning:

```sql
SELECT create_hypertable('weather_100pct', 'time', if_not_exists => TRUE);
```
## Benchmark Design

- The benchmark script is defined in
```bash
phase_4/concurrency_throughput_benchmark.py
```
- It performs concurrent query execution using Python’s ThreadPoolExecutor.
- The results are stored in [RESULTS_DIR](results/)

- Characteristics of Experiment

| Parameter            | Description                                                                         |
| -------------------- | ----------------------------------------------------------------------------------- |
| `CONCURRENCY_LEVELS` | [1, 4, 8, 16, 32] — number of concurrent clients (threads)                          |
| `RUNS_PER_THREAD`    | 10 queries per thread                                                               |
| `RESULTS_DIR`        | Directory to store per-run results and plots                                        |
| `QUERIES_FILE`       | JSON file (`queries.json`) containing SQL queries for the `weather` dataset         |
| `DBS`                | Database configuration for PostgreSQL (`weather_pg`) and TimescaleDB (`weather_ts`) |

## Concurrent Query Execution

For each concurrency level:

- A thread pool (ThreadPoolExecutor) is launched with N threads.

- Each thread randomly selects queries from the weather dataset query set (queries.json).
- Executes each query sequentially using run_query() from utils.py.
- Records latency (in milliseconds) and row count for each execution.
- After all threads complete, the following metrics are computed:

| Metric             | Description                               | Unit                     |
| ------------------ | ----------------------------------------- | ------------------------ |
| **Median Latency** | Median execution time across all threads  | ms                       |
| **Mean Latency**   | Average query latency                     | ms                       |
| **Throughput**     | Total queries executed ÷ total time taken | Queries per second (QPS) |
