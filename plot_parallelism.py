import csv
import matplotlib.pyplot as plt

parallelism_levels, times = [], []

with open("parallelism_results.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        parallelism_levels.append(int(row["parallelism"]))
        times.append(float(row["core_time_ms"]))

plt.figure(figsize=(7, 5))

plt.plot(
    parallelism_levels,
    times,
    marker="o",
    linewidth=2
)

plt.xlabel("ForkJoinPool parallelism level")
plt.ylabel("Core simulation time (ms)")
plt.title("Runtime vs Parallelism Level")
plt.grid(True, ls="--", alpha=0.5)
plt.xticks(parallelism_levels)

plt.tight_layout()
plt.savefig("parallelism_graph.png", dpi=150)
plt.show()

print("Parallelism | Core time (ms)")
for p, t in zip(parallelism_levels, times):
    print(f"{p:11d} | {t:14.3f}")