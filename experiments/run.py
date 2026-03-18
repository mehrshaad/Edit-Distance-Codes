import os
import sys
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from experiments.func import (load_results_csv, parse_float, parse_int,
                              plot_code_size, plot_runtime,
                              print_results_table, save_codewords,
                              save_results_csv)
from src import (build_code_multiple_runs, build_code_multiple_runs_parallel,
                 generate_binary_vectors)


def run_experiment(n: int,
                   d: int,
                   num_runs: int = 50,
                   run_normal: bool = True) -> dict:
    w = n // 2
    vectors = generate_binary_vectors(n, w)

    # NORMAL (will skip for n > 10 to save time)
    if run_normal:
        start = time.time()
        code_normal = build_code_multiple_runs(vectors, n, d, num_runs)
        t1 = time.time() - start
        M_normal = len(code_normal)
    else:
        t1 = None
        M_normal = None

    # OPTIMIZED (always run)
    start = time.time()
    code_fast = build_code_multiple_runs_parallel(vectors, n, d, num_runs)
    t2 = time.time() - start

    save_codewords(code_fast, n, d)

    return {
        "n": n,
        "d": d,
        "w": w,
        "M_normal": M_normal,
        "M_fast": len(code_fast),
        "time_normal": round(t1, 4) if t1 else None,
        "time_fast": round(t2, 4),
    }


def run_all_experiments(
    test_cases: list[tuple[int, int]] = [
        (4, 2),
        (4, 4),
        (6, 2),
        (6, 4),
        (6, 6),
        (8, 2),
        (8, 4),
        (8, 6),
        (10, 2),
        (10, 4),
        (10, 6),
    ]
) -> list[dict]:
    results = []

    existing_results = load_results_csv()

    # Track existing (n, d)
    existing_keys = set((int(r["n"]), int(r["d"])) for r in existing_results)

    # Convert existing results to correct format (optional but clean)
    for r in existing_results:
        results.append({
            "n": int(r["n"]),
            "d": int(r["d"]),
            "w": int(r["w"]),
            "M_normal": parse_int(r["M_normal"]),
            "M_fast": parse_int(r["M_fast"]),
            "time_normal": parse_float(r["time_normal"]),
            "time_fast": parse_float(r["time_fast"]),
        })

    for n, d in test_cases:
        if (n, d) in existing_keys:
            print(f"Skipping (n={n}, d={d}) — already exists")
            continue

        print(f"Running (n={n}, d={d})...")
        if n <= 10:
            num_runs = 100
        elif n == 12:
            num_runs = 50
        else:
            num_runs = 10
        result = run_experiment(n,
                                d,
                                num_runs=num_runs,
                                run_normal=((n - d) < 10) and (n <= 12))
        results.append(result)

    results.sort(key=lambda x: (x["n"], x["d"]))
    return results


if __name__ == "__main__":
    results = run_all_experiments()

    save_results_csv(results=results)
    print_results_table(results=results)

    plot_runtime(results=results)
    plot_code_size(results=results)
