import csv
import os

import matplotlib.pyplot as plt

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RESULTS_DIR = os.path.join(BASE_DIR, "report")
CODEWORDS = os.path.join(RESULTS_DIR, "codewords")
os.makedirs(CODEWORDS, exist_ok=True)


def parse_int(value: str | None) -> int | None:
    return int(value) if value not in ("", None) else None


def parse_float(value: str | None) -> float | None:
    return float(value) if value not in ("", None) else None


def load_results_csv() -> list[dict]:
    filepath = os.path.join(RESULTS_DIR, "results.csv")

    if not os.path.exists(filepath):
        return []

    with open(filepath, "r") as f:
        reader = csv.DictReader(f)
        return list(reader)


def save_results_csv(results: list[dict]) -> None:
    filepath = os.path.join(RESULTS_DIR, "results.csv")
    keys = results[0].keys()

    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()

        for row in results:
            clean_row = {k: ("" if v is None else v) for k, v in row.items()}
            writer.writerow(clean_row)


def print_results_table(results: list[dict]) -> None:
    print("\n=== Comparison Table ===")
    print(
        f"{'n':<5}{'d':<5}{'M_norm':<10}{'M_fast':<10}{'t_norm':<12}{'t_fast':<12}"
    )
    print("-" * 65)

    for r in results:
        m_norm = r["M_normal"] if r["M_normal"] is not None else "—"
        t_norm = (f"{r['time_normal']:.4f}"
                  if r["time_normal"] is not None else "—")
        t_fast = f"{r['time_fast']:.4f}"

        print(
            f"{r['n']:<5}{r['d']:<5}{m_norm:<10}{r['M_fast']:<10}{t_norm:<12}{t_fast:<12}"
        )


def save_codewords(code: list, n: int, d: int) -> None:
    filepath = os.path.join(CODEWORDS, f"code_n{n}_d{d}.txt")

    with open(filepath, "w") as f:
        for v in code:
            f.write(format(v, f'0{n}b') + "\n")


def plot_runtime(results: list[dict]) -> None:
    labels = [f"({r['n']},{r['d']})" for r in results]

    t_norm = [
        r["time_normal"] if r["time_normal"] is not None else float('nan')
        for r in results
    ]
    t_fast = [
        r["time_fast"] if r["time_fast"] is not None else float('nan')
        for r in results
    ]

    x = range(len(labels))

    plt.figure()
    plt.plot(x, t_norm, marker='o', label="Normal")
    plt.plot(x, t_fast, marker='o', label="Optimized")

    plt.xticks(x, labels, rotation=45)
    plt.ylabel("Time (seconds)")
    plt.title("Runtime Comparison")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    filepath = os.path.join(RESULTS_DIR, "runtime_comparison.png")
    plt.savefig(filepath)
    plt.close()


def plot_code_size(results: list[dict]) -> None:
    labels = [f"({r['n']},{r['d']})" for r in results]

    m_norm = [
        r["M_normal"] if r["M_normal"] is not None else float('nan')
        for r in results
    ]
    m_fast = [
        r["M_fast"] if r["M_fast"] is not None else float('nan')
        for r in results
    ]

    x = range(len(labels))

    plt.figure()

    # Normal → solid
    plt.plot(x,
             m_norm,
             marker='o',
             linestyle='-',
             label="Normal",
             markersize=6)

    # Optimized → dashed + different marker
    plt.plot(x,
             m_fast,
             marker='s',
             linestyle='--',
             label="Optimized",
             markersize=6,
             alpha=0.5)

    plt.xticks(x, labels, rotation=45)
    plt.ylabel("Code Size (M)")
    plt.title("Code Size Comparison")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    filepath = os.path.join(RESULTS_DIR, "code_size.png")
    plt.savefig(filepath)
    plt.close()
