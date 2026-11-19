import csv
import matplotlib.pyplot as plt

def load_times(filename, time_col="core_time_ms", key_col="grid_size"):
    """Returns a dict {grid_size: core_time_ms} from a CSV file."""
    result = {}
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            size = int(row[key_col])
            time = row[time_col].strip()
            if time == "":
                continue  # skip rows not filled in yet
            result[size] = float(time)
    return result

laptop_parallel = load_times("gridsize_justify.csv")
laptop_serial = load_times("gridsize_serial.csv")
server_serial = load_times("server_results_serial.csv")
server_parallel = load_times("server_results_parallel.csv")

# Only plot grid sizes that have data on all four files.
common_sizes = sorted(
    set(laptop_parallel) & set(laptop_serial)
    & set(server_serial) & set(server_parallel)
)

if not common_sizes:
    print("No grid size has data in all four files yet - fill in the CSVs first.")
    print(f"laptop_parallel sizes: {sorted(laptop_parallel)}")
    print(f"laptop_serial sizes: {sorted(laptop_serial)}")
    print(f"server_serial sizes: {sorted(server_serial)}")
    print(f"server_parallel sizes: {sorted(server_parallel)}")
else:
    laptop_speedup = [laptop_serial[s] / laptop_parallel[s] for s in common_sizes]
    server_speedup = [server_serial[s] / server_parallel[s] for s in common_sizes]

    print("Grid size | Laptop speedup | Server speedup")
    for s, ls, ss in zip(common_sizes, laptop_speedup, server_speedup):
        print(f"{s:9d} | {ls:14.3f} | {ss:14.3f}")

    plt.figure(figsize=(8, 5))
    plt.plot(common_sizes, laptop_speedup, marker="o", linewidth=2, label="Laptop")
    plt.plot(common_sizes, server_speedup, marker="s", linewidth=2, label="Department server")
    plt.axhline(y=1.0, color="gray", linestyle="--", alpha=0.6, label="No speedup (parallel = serial)")

    plt.xlabel("Grid size (rows = columns)")
    plt.ylabel("Speedup (serial time / parallel time)")
    plt.title("Parallel speedup vs grid size: laptop vs department server")
    plt.legend()
    plt.grid(True, ls="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig("speedup_graph.png", dpi=150)
    plt.show()
    print("\nSaved speedup_graph.png")
    