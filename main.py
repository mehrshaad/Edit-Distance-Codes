from experiments import *

test_cases = [
    # Small
    (2, 2),
    (4, 2),
    (4, 4),
    (6, 2),
    (6, 4),
    (6, 6),
    # Medium
    (8, 2),
    (8, 4),
    (8, 6),
    (8, 8),
    (10, 2),
    (10, 4),
    (10, 6),
    (10, 8),
    (10, 10),
    # Large
    (12, 2),
    (12, 4),
    (12, 6),
    (12, 8),
    (12, 10),
    (12, 12),
    (14, 2),
    (14, 4),
    (14, 6),
    (14, 8),
    (14, 10),
    (14, 12),
    (14, 14),
]


def main():
    global test_cases
    results = run_all_experiments(test_cases=test_cases)
    save_results_csv(results=results)
    print_results_table(results=results)

    plot_runtime(results=results)
    plot_code_size(results=results)


if __name__ == "__main__":
    main()
