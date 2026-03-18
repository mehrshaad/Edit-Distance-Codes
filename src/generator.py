from itertools import combinations


def generate_binary_vectors(n: int, w: int) -> list:
    """
    Generate all binary vectors of length n with exactly w ones.
    Returns list of integers (bit representation).
    """
    vectors = []

    for ones_positions in combinations(range(n), w):
        num = 0
        for pos in ones_positions:
            num |= (1 << pos)
        vectors.append(num)

    return vectors
