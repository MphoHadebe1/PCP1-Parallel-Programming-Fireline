# CSC2002S PCP1: Parallel Wildfire Heat Diffusion

Parallel version of a wildfire / heat diffusion stencil simulation, written in Java using the Fork/Join framework. It uses divide-and-conquer with a configurable sequential cutoff, and produces the same results and output as the serial version.

## Files

**Parallel solution**
- `FirelineParallel.java`: command-line processing, simulation loop and timing
- `FireMapParallel.java`: landscape, simulation state and parallel timestep update
- `FireTask.java`: Fork/Join task (divide-and-conquer with sequential cutoff)
- `TerrainType.java`: fixed terrain and combustion constants (unchanged)
- `Makefile`: compiles with Java 11 and runs the parallel program

**Benchmarking and analysis**
- `sweep_parallelism.py`: sweeps the ForkJoinPool parallelism level
- `plot_cutoff.py`, `plot_parallelism.py`, `plot_speedup.py`: generate the report graphs
- `cutoff_justify.csv`: sequential cutoff experiment results
- `gridsize_justify.csv`, `gridsize_serial.csv`: grid size experiments
- `parallelism_results.csv`: parallelism level results
- `server_results_serial.csv`, `server_results_parallel.csv`: departmental server benchmarks

**Documentation**
- `REPORT PDF.pdf`: final report
- `git_log.txt`: output of `git log --all`
- `CSC2002S_PCP1_Assignment_...`: assignment brief

## Requirements

- Java 11 or later
- `make`
- Python 3 with `matplotlib` and `pandas` (only for the plotting scripts)

## Build and run

```bash
make run ARGS="500 500 17 wildfire output/run17 50000 0.05 mixed"
```

Make sure the `output/` folder exists, since the program writes its PNG files there.

### Arguments

```
rows columns seed mode output-prefix [max-steps] [tolerance] [landscape] [ignition-top-row ignition-left-column patch-size]
```

| Argument | Description |
|---|---|
| `rows`, `columns` | Grid dimensions |
| `seed` | Seed for the mixed landscape |
| `mode` | `diffusion` or `wildfire` |
| `output-prefix` | Prefix for the output images |
| `max-steps` | Optional limit on timesteps |
| `tolerance` | Optional convergence tolerance |
| `landscape` | Optional: `mixed` (default) or `grass` |
| ignition args | Optional: top row, left column and patch size (all three together) |

### Output

- Console: configuration, timesteps, convergence status, cells burned, peak temperature, final max change, core simulation time (excludes image writing)
- `<prefix>_terrain.png`, `<prefix>_peak.png`, `<prefix>_final.png`

## Parallel design

- Fork/Join divide-and-conquer: the grid is split recursively into row ranges, forked and joined with `fork()` / `join()` only.
- Sequential cutoff: ranges at or below the cutoff are processed serially.
- No locks, atomics, barriers or `synchronized`. Each task writes only to its own rows of the next-state grid, so there are no data races.
- The model, constants and numerical update rules are identical to the serial version.

## Reproducing the benchmarks

```bash
python3 sweep_parallelism.py
python3 plot_cutoff.py
python3 plot_parallelism.py
python3 plot_speedup.py
```

## Machines tested

- Personal computer: *(add CPU, cores, Java version)*
- Departmental server: *(add CPU, cores, Java version)*

## AI use

*(Add a short declaration of the tools used, what for, and how the output was verified. This must match your report.)*
