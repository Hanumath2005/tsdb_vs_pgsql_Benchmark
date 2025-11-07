import os
import pandas as pd
import matplotlib.pyplot as plt


def summarize(base_path: str = None):
    all_files = [os.path.join(base_path, f) for f in os.listdir(base_path) if f.endswith(".csv")]
    dfs = [pd.read_csv(f) for f in all_files if os.path.getsize(f) > 0]
    df = pd.concat(dfs, ignore_index=True)
    df["elapsed_ms"] = df["elapsed_ms"].astype(float)
    summary = df.groupby(["db","query_name","scale"])["elapsed_ms"].median().reset_index()

    out_dir = os.path.join(base_path, "plots")
    os.makedirs(out_dir, exist_ok=True)
    
    for q in summary["query_name"].unique():
        if q == "downsample_pg_day" or q == "downsample_ts_day":
            continue  # skip Timescale-specific 
        plt.figure(figsize=(8,5))
        sub = summary[summary["query_name"]==q]
        for db in ["pg","ts"]:
            part = sub[sub["db"]==db]
            if not part.empty:
                plt.plot(part["scale"], part["elapsed_ms"], marker="o", label=db.upper())
        plt.title(f"Latency Scaling — {q}")
        plt.xlabel("Dataset size (%)")
        plt.ylabel("Median latency (ms)")
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(out_dir, f"latency_{q}.png"))
        plt.close()
        print(f"Saved latency_{q}.png")

    plt.figure(figsize=(8,5))
    sub = summary[summary["query_name"] == "downsample_pg_day"]
    part = sub[sub["db"] == "pg"]
    plt.plot(part["scale"], part["elapsed_ms"], marker="o", label="PG")
    sub = summary[summary["query_name"] == "downsample_ts_day"]
    part = sub[sub["db"] == "ts"]
    plt.plot(part["scale"], part["elapsed_ms"], marker="o", label="TS")
    plt.title(f"Latency Scaling — Downsampling per Day")
    plt.xlabel("Dataset size (%)")
    plt.ylabel("Median latency (ms)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, f"latency_downsample_day.png"))
    plt.close()
    print(f"Saved latency_downsample_day.png")


    merged = summary.pivot_table(index=["query_name","scale"], columns="db", values="elapsed_ms").dropna().reset_index()
    merged["speedup"] = merged["pg"] / merged["ts"]

    plt.figure(figsize=(9,6))
    for q in merged["query_name"].unique():
        part = merged[merged["query_name"]==q]
        plt.plot(part["scale"], part["speedup"], marker="s", label=q)
    plt.axhline(1, color="black", linestyle="--")
    plt.xlabel("Dataset size (%)")
    plt.ylabel("Speedup (PG / TS)")
    plt.title("TimescaleDB Speedup vs Dataset Size")
    plt.legend(ncol=2, fontsize="small")
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "speedup_vs_scale.png"))
    plt.close()
    print("Saved speedup_vs_scale.png")