import subprocess
import time
import os
import psycopg2



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


