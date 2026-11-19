import subprocess
import re
import csv

CUTOFF = 80000
PARALLELISM_LEVELS = [1, 2, 4, 6, 8]  # matches your 8-core machine
ROWS = 500
COLUMNS = 500
SEED = 17
MODE = "wildfire"
OUTPUT_PREFIX = "output/paralleltest"
MAX_STEPS = 50000
TOLERANCE = 0.05
LANDSCAPE = "mixed"

RESULTS_FILE = "parallelism_results.csv"


def run_one(parallelism):
    cmd = [
        "java",
        f"-Dfireline.cutoff={CUTOFF}",
        f"-Dfireline.parallelism={parallelism}",
        "-cp", "bin", "FirelineParallel",
        str(ROWS), str(COLUMNS), str(SEED), MODE, OUTPUT_PREFIX,
        str(MAX_STEPS), str(TOLERANCE), LANDSCAPE,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    output = result.stdout

    match = re.search(r"Core simulation time:\s*([0-9]+\.[0-9]+)\s*ms", output)
    if not match:
        print(f"  WARNING: could not parse output for parallelism={parallelism}")
        print(output)
        print(result.stderr)
        return None
    return float(match.group(1))


def main():
    rows = []
    for p in PARALLELISM_LEVELS:
        print(f"=== parallelism={p} ===")
        time_ms = run_one(p)
        if time_ms is None:
            continue
        rows.append((p, time_ms))
        print(f"  -> {time_ms} ms")

    with open(RESULTS_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["parallelism", "core_time_ms"])
        writer.writerows(rows)

    print(f"\nDone. Results saved to {RESULTS_FILE}")
    for p, t in rows:
        print(f"{p},{t}")


if __name__ == "__main__":
    main()