"""
Phase 4 — Concurrency & Throughput Benchmark
Compare PostgreSQL vs TimescaleDB under multi-client load using ThreadPoolExecutor and weather_100pct table.
"""

import time, csv, os, random, statistics
import psycopg2
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys
import json
sys.path.append('..')
from utils import run_query
from plot_generation import summarize

DBS = {
    "pg": {"dbname": "weather_pg", "user": "postgres", "host": "/var/run/postgresql"},
    "ts": {"dbname": "weather_ts", "user": "postgres", "host": "/var/run/postgresql"}
}

CONCURRENCY_LEVELS = [1, 4, 8, 16, 32]
RUNS_PER_THREAD = 10
RESULTS_DIR = "results/"
os.makedirs(RESULTS_DIR, exist_ok=True)
QUERIES_FILE = "queries.json"

def worker(dbconf, dbkey):
    """Thread worker: randomly pick queries and execute them sequentially."""
    latencies = []
    with open(QUERIES_FILE, "r") as f:
        queries_data = json.load(f)
        QUERIES = queries_data["weather"]
    conn = psycopg2.connect(dbname=dbconf["dbname"], user=dbconf["user"], host=dbconf["host"])
    for _ in range(RUNS_PER_THREAD):
        query = random.choice(QUERIES)
        qname = query["query"]
        qsql = query["sql"]
        if (dbkey == "pg" and "time_bucket" in qsql) or (dbkey == "ts" and "date_trunc" in qsql):
            continue
        elapsed, row_count = run_query(conn, qsql)
        latencies.append((elapsed, row_count, qname))
    return latencies

def main():
    all_results = []
    for dbkey, dbconf in DBS.items():
        print(f"Concurrency Benchmark for {dbkey.upper()}")
        for threads in CONCURRENCY_LEVELS:
            print(f"Running with {threads} concurrent clients ...")

            start_all = time.time()
            dbname = dbconf["dbname"]
            dbuser = dbconf["user"]
            dbhost = dbconf["host"]

            with ThreadPoolExecutor(max_workers=threads) as executor:
                futures = [executor.submit(worker, dbconf, dbkey) for _ in range(threads)]
                thread_results = []
                for fut in as_completed(futures):
                    thread_results.extend(fut.result())
            total_time = time.time() - start_all
            all_latencies = [t[0] for t in thread_results]
            all_row_counts = [t[1] for t in thread_results]
            throughput = len(all_latencies) / total_time
            median_lat = statistics.median(all_latencies)
            mean_lat = statistics.mean(all_latencies)
            print(f" → median latency: {median_lat:.2f} ms, mean: {mean_lat:.2f} ms, throughput: {throughput:.2f} QPS")
            out_csv = os.path.join(RESULTS_DIR, f"{dbkey}_concurrency_{threads}.csv")
            with open(out_csv, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp", "db", "threads", "query_name", "elapsed_ms", "row_count"])
                for lat, row_count, qn in thread_results:
                    writer.writerow([datetime.now().isoformat(), dbkey, threads, qn, f"{lat:.3f}", row_count])
            all_results.append((dbkey, threads, median_lat, mean_lat, throughput))
    summarize(all_results, base_path=RESULTS_DIR)


if __name__ == "__main__":
    main()