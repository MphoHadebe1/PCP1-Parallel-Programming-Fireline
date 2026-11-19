import csv
import matplotlib.pyplot as plt

cutoffs, times = [], []
with open("cutoff_justify.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        cutoffs.append(int(row["cutoff"]))
        times.append(float(row["core_time_ms"]))

plt.figure(figsize=(9, 5))
plt.plot(cutoffs, times, marker="o", linewidth=2)
plt.xscale("log")

# Explicitly show only the cutoff values that were actually tested,
# instead of matplotlib's default log-scale tick marks.
plt.xticks(cutoffs, [str(c) for c in cutoffs], rotation=45)

plt.xlabel("Sequential cutoff (cells)")
plt.ylabel("Core simulation time (ms)")
plt.title("Effect of sequential cutoff on runtime (500x500 wildfire, mixed)")
plt.grid(True, which="both", ls="--", alpha=0.5)

if 80000 in cutoffs:
    plt.axvline(x=80000, color="red", linestyle=":", label="Chosen cutoff (80,000)")
    plt.legend()

plt.tight_layout()
plt.savefig("cutoff_graph.png", dpi=150)
plt.show()