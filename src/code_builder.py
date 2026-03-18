import os
import random
import sys
from typing import Literal

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from multiprocessing import Pool, cpu_count

from src.distance import edit_distance, edit_distance_threshold


def is_valid(candidate: list,
             code: list,
             n: int,
             d: int,
             mode: Literal["normal", "threshold"] = "threshold") -> bool:
    """
    Check if candidate can be added to the code.
    """
    for c in code:
        if mode == "normal":
            if edit_distance(candidate, c, n) < d:
                return False
        elif mode == "threshold":
            if not edit_distance_threshold(candidate, c, n, d):
                return False
    return True


def build_code_greedy(vectors: list, n: int, d: int) -> list:
    """
    Deterministic greedy (no shuffle).
    """
    code = []

    for v in vectors:
        if is_valid(v, code, n, d):
            code.append(v)

    return code


def build_code_greedy_random(args: tuple[list, int, int]) -> list:
    """
    Single greedy run with random order.
    """
    vectors, n, d = args
    shuffled = vectors[:]
    random.shuffle(shuffled)
    return build_code_greedy(shuffled, n, d)


def build_code_multiple_runs(vectors: list,
                             n: int,
                             d: int,
                             num_runs: int = 50) -> list:
    """
    Run randomized greedy multiple times and return best result.
    """
    best_code = []

    for _ in range(num_runs):
        code = build_code_greedy_random([vectors, n, d])

        if len(code) > len(best_code):
            best_code = code

    return best_code


def build_code_multiple_runs_parallel(vectors: list,
                                      n: int,
                                      d: int,
                                      num_runs: int = 50) -> list:
    """
    Parallel version of multiple runs.
    """
    with Pool(cpu_count()) as pool:
        results = pool.map(build_code_greedy_random,
                           [(vectors, n, d)] * num_runs)

    # pick best result
    best_code = max(results, key=len)
    return best_code
