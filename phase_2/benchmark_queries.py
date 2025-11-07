"""
Benchmarking between PostgreSQL and TimescaleDB databases
Performance comparison across various query types
"""
import time, csv, os, subprocess, statistics
import psycopg2
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import json

from plot_generation import summarize
import sys

RUNS = 10
RESULTS_DIR = "results/"
os.makedirs(RESULTS_DIR, exist_ok=True)
QUERIES_FILE = "queries.json"

DBS = {
    "weather": {
        "pg": {"dbname": "weather_pg", "user": "postgres", "host": "/var/run/postgresql"},
        "ts": {"dbname": "weather_ts", "user": "postgres", "host": "/var/run/postgresql"}
    },
    "nyc": {
        "pg": {"dbname": "nyc_pg", "user": "postgres", "host": "/var/run/postgresql"},
        "ts": {"dbname": "nyc_ts", "user": "postgres", "host": "/var/run/postgresql"}
    },
    "synthetic": {
        "pg": {"dbname": "synthetic_pg", "user": "postgres", "host": "/var/run/postgresql"},
        "ts": {"dbname": "synthetic_ts", "user": "postgres", "host": "/var/run/postgresql"}
    }
}
def drop_caches():
    try:
        subprocess.run(["sudo", "sync"], check=True)
        subprocess.run(["sudo", "sh", "-c", "echo 3 > /proc/sys/vm/drop_caches"], shell=False)
        time.sleep(0.5)
        return True
    except Exception as e:
        print(f"Error dropping caches: {e}")
        return False


def run_query(conn, query):
    start_time = time.time()
    cursor = conn.cursor()
    cursor.execute(query)
    cursor.fetchall()
    try:
        rowcount = cursor.rowcount if cursor.rowcount is not None else 0
    except:
        rowcount = 0
    end_time = time.time()
    return (end_time - start_time) * 1000, rowcount

def run_explain(conn, query, outfile):
    cursor = conn.cursor()
    explain_query = f"EXPLAIN (ANALYZE, BUFFERS) {query}"
    cursor.execute(explain_query)
    explain_result = cursor.fetchall()
    with open(outfile, "w") as f:
        for row in explain_result:
            f.write(row[0] + "\n")
            f.write("\n".join(row[1:]) + "\n")

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <dataset_name>")
        sys.exit(1)
    dataset = sys.argv[1]
    if dataset not in DBS:
        print(f"Invalid dataset. Choose from: {', '.join(DBS.keys())}")
        sys.exit(1)
    
    with open(QUERIES_FILE) as f:
        queries_data = json.load(f)
        QUERIES = queries_data[dataset]
    RESULTS_DB = os.path.join(RESULTS_DIR, f"{dataset}")
    os.makedirs(RESULTS_DB, exist_ok=True)
    EXPLAIN_DIR = os.path.join(RESULTS_DB, "explain_plans")
    os.makedirs(EXPLAIN_DIR, exist_ok=True)
    db_config = DBS[dataset]
    for db_key, db_params in db_config.items():
        dbname = db_params["dbname"]
        user = db_params["user"]
        host = db_params["host"]
        conn = psycopg2.connect(dbname=dbname, user=user, host=host)
        for query in QUERIES:
            qname = query["query"]
            qsql = query["sql"]
            results_file = os.path.join(RESULTS_DB, f"results_{db_key}_{qname}.csv")
            if (db_key == "pg" and "time_bucket" in qsql):
                continue  # skip TimescaleDB-specific queries for PostgreSQL
            times = []
            explain_file = os.path.join(EXPLAIN_DIR, f"explain_{db_key}_{qname}.txt")
            run_explain(conn, qsql, explain_file)
            with open(results_file, "w") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["timestamp","db","query_name","run_index","elapsed_ms","rowcount"])
                for run in range(RUNS):
                    if run == 0:
                        drop_caches()
                        print("Dropped Caches for cold-cache runs")
                    exec_time, rowcount = run_query(conn, qsql)
                    writer.writerow([datetime.now().isoformat(), db_key, qname, run+1, exec_time, rowcount])
                    csvfile.flush()
                    times.append(exec_time)
                    print(f"{db_key.upper()} - Query: {qname}, Run: {run+1}, Time: {exec_time:.2f} ms")
                print(f"{db_key.upper()} - Query: {qname},\nAvg Time: {statistics.mean(times):.2f} ms over {RUNS} runs,\nmedian: {statistics.median(times):.2f} ms, stddev: {statistics.stdev(times):.2f} ms\n")  
        conn.close()
        print(f"Completed benchmarks for database: {db_key}\n")
    
    # Analysis of results
    summarize(base_path=RESULTS_DB)

if __name__ == "__main__":
    main()

                


