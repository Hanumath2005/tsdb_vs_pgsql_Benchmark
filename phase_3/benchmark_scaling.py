"""
Phase 3 — Scalability Benchmark
Compare PostgreSQL vs TimescaleDB across scaled tables:
Scale the database into 1%, 10%, 25%, 50%, 75%, and 100% of the original data and measure query performance scaling behavior.
"""

import time, csv, os, subprocess, statistics
import psycopg2
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import os
import json
import sys
from plot_generation import summarize
sys.path.append("..")
from utils import drop_caches, run_query

DBS = {
    "pg": {"dbname": "weather_pg", "user": "postgres", "host": "/var/run/postgresql"},
    "ts": {"dbname": "weather_ts", "user": "postgres", "host": "/var/run/postgresql"}
}

RUNS = 10
SCALES = [1, 10, 25, 50, 75, 100]

BASE_RESULTS = "results/"
QUERIES_FILE = "queries.json"
os.makedirs(BASE_RESULTS, exist_ok=True)


def main():
    with open(QUERIES_FILE, "r") as f:
        queries_data = json.load(f)
        QUERIES = queries_data["weather"]
    for dbkey, dbconf in DBS.items():
        conn = psycopg2.connect(dbname=dbconf["dbname"], user=dbconf["user"], host=dbconf["host"])
        for s in SCALES:
            print(f"Benchmarking {dbkey.upper()} at {s}% scale")
            table = f"weather_{s}pct"
            for query in QUERIES:
                qname = query["query"]
                qsql_template = query["sql"]
                if (dbkey == "pg" and "time_bucket" in qsql_template) or (dbkey == "ts" and "date_trunc" in qsql_template):
                    continue  # skip Timescale-specific
                qsql = qsql_template.format(table=table)

                results_path = os.path.join(BASE_RESULTS, f"{dbkey}_{qname}_{s}pct.csv")
                os.makedirs(os.path.dirname(results_path), exist_ok=True)

                times = []
                with open(results_path, "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(["timestamp", "db", "scale", "query_name", "run_index", "elapsed_ms","row_count"])
                    for run in range(RUNS):
                        drop_caches()
                        elapsed, row_count = run_query(conn, qsql)
                        writer.writerow([datetime.now().isoformat(), dbkey, s, qname, run+1, f"{elapsed:.3f}", row_count])
                        times.append(elapsed)
                        print(f"   {qname} | run {run+1}/{RUNS} | {elapsed:.2f} ms")
                
                print(f" → {qname}: median {statistics.median(times):.2f} ms, mean {statistics.mean(times):.2f} ms")
        conn.close()
        print(f"Completed benchmarks for {dbkey}.\n")

    print("Benchmarking finished for all scales and DBs.")
    summarize(base_path=BASE_RESULTS)

if __name__ == "__main__":
    main()
