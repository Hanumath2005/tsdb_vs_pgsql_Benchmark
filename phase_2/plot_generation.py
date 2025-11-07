import os
import pandas as pd
import matplotlib.pyplot as plt

def summarize(base_path: str = None):
    # Collect all CSV result files in the given directory
    all_csvs = [os.path.join(base_path, f) for f in os.listdir(base_path) if f.endswith(".csv")]

    dfs = []
    for file in all_csvs:
        try:
            df = pd.read_csv(file)

            # Drop repeated header rows (common when appending benchmark runs)
            if "elapsed_ms" in df.columns:
                df = df[df["elapsed_ms"] != "elapsed_ms"]

                # Convert elapsed_ms to numeric and drop invalid rows
                df["elapsed_ms"] = pd.to_numeric(df["elapsed_ms"], errors="coerce")
                df = df.dropna(subset=["elapsed_ms"])

            dfs.append(df)
        except Exception as e:
            print(f"⚠️ Skipping {file}: {e}")

    if not dfs:
        print("❌ No result files found. Please run benchmarks first.")
        return

    # Combine all CSVs into one DataFrame
    df = pd.concat(dfs, ignore_index=True)

    # Print quick summary for debug
    print(f"✅ Loaded {len(df)} total benchmark entries.")
    print(f"Databases present: {df['db'].unique().tolist()}")
    print(f"Queries present: {df['query_name'].unique().tolist()}")

    # Compute summary statistics for each (db, query_name)
    summary = (
        df.groupby(["db", "query_name"])["elapsed_ms"]
          .agg(["median", "mean", "std"])
          .reset_index()
    )

    # Separate PostgreSQL and TimescaleDB results
    pg = summary[summary["db"] == "pg"].set_index("query_name")
    ts = summary[summary["db"] == "ts"].set_index("query_name")

    # Merge and compute speedup ratios
    merged = pg.join(ts, lsuffix="_pg", rsuffix="_ts")
    merged["speedup"] = merged["median_pg"] / merged["median_ts"]

    # Categorize performance
    merged["speedup_category"] = merged["speedup"].apply(
        lambda x: "Timescale Faster" if x > 1.05 else
                  ("Postgres Faster" if x < 0.95 else "Equal Performance")
    )

    # Save summary to CSV
    summary_path = os.path.join(base_path, "benchmark_summary.csv")
    merged.to_csv(summary_path)
    print(f"✅ Saved summary CSV → {summary_path}")

    # Create a horizontal bar chart for speedup visualization
    plt.figure(figsize=(12, 6))
    merged["color"] = merged["speedup_category"].apply(
        lambda x: "green" if x == "Timescale Faster"
        else ("red" if x == "Postgres Faster" else "blue")
    )

    out_dir = os.path.join(base_path, "plots")
    os.makedirs(out_dir, exist_ok=True)

    merged.sort_values("speedup", inplace=True)
    plt.barh(merged.index, merged["speedup"], color=merged["color"])

    plt.axvline(1.0, color="black", linestyle="--", linewidth=1)
    plt.xlabel("Speedup (PostgreSQL Median / TimescaleDB Median)")
    plt.ylabel("Query Name")
    plt.title("TimescaleDB Speedup over PostgreSQL (Phase 2 Weather Benchmark)")
    plt.tight_layout()

    plot_path = os.path.join(out_dir, "speedup_plot_weather.png")
    plt.savefig(plot_path)
    print(f"📈 Speedup plot saved → {plot_path}")
