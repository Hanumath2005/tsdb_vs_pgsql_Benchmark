import pandas as pd
import os

import matplotlib.pyplot as plt

def summarize(all_results, base_path : str = None):
    df = pd.DataFrame(all_results, columns=["db","threads","median_lat","mean_lat","throughput"])
    RESULTS_DIR = os.path.join(base_path if base_path else ".", "results")
    os.makedirs(RESULTS_DIR, exist_ok=True)

    out_dir = os.path.join(RESULTS_DIR, "plots")
    os.makedirs(out_dir, exist_ok=True)

    plt.figure(figsize=(8,5))
    for db in ["pg","ts"]:
        sub = df[df["db"]==db]
        plt.plot(sub["threads"], sub["median_lat"], marker="o", label=db.upper())
    plt.title("Median Latency vs Concurrency Level")
    plt.xlabel("Concurrent clients")
    plt.ylabel("Median latency (ms)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "latency_vs_concurrency.png"))
    plt.close()
    print("Saved latency_vs_concurrency.png")

    plt.figure(figsize=(8,5))
    for db in ["pg","ts"]:
        sub = df[df["db"]==db]
        plt.plot(sub["threads"], sub["throughput"], marker="s", label=db.upper())
    plt.title("Throughput vs Concurrency Level")
    plt.xlabel("Concurrent clients")
    plt.ylabel("Throughput (queries/sec)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "throughput_vs_concurrency.png"))
    plt.close()
    print("Saved throughput_vs_concurrency.png")

    merged = df.pivot_table(index="threads", columns="db", values="throughput").dropna().reset_index()
    merged["speedup"] = merged["ts"] / merged["pg"]

    plt.figure(figsize=(8,5))
    plt.plot(merged["threads"], merged["speedup"], marker="^", label="TimescaleDB Throughput speedup")
    plt.axhline(1, color="black", linestyle="--")
    plt.title("TimescaleDB Speedup (Throughput ratio TS/PG)")
    plt.xlabel("Concurrent clients")
    plt.ylabel("Speedup (TS / PG)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "speedup_vs_concurrency.png"))
    plt.close()
    print("Saved speedup_vs_concurrency.png")