def edit_distance(a: int, b: int, n: int) -> int:
    """
    Compute edit distance between two binary vectors (integers).
    Converts to bit strings of length n.
    """
    s1 = format(a, f'0{n}b')
    s2 = format(b, f'0{n}b')

    dp = [[0] * (n + 1) for _ in range(n + 1)]

    for i in range(n + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                cost = 0
            else:
                cost = 1

            dp[i][j] = min(
                dp[i - 1][j] + 1,  # delete
                dp[i][j - 1] + 1,  # insert
                dp[i - 1][j - 1] + cost  # substitute
            )

    return dp[n][n]


def edit_distance_threshold(a: int, b: int, n: int, d: int) -> bool:
    """
    Returns True if edit distance >= d
    Returns False if edit distance < d
    """
    s1 = format(a, f'0{n}b')
    s2 = format(b, f'0{n}b')

    prev = list(range(n + 1))

    for i in range(1, n + 1):
        curr = [i] + [0] * n

        # Track minimum in row
        min_in_row = curr[0]

        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                cost = 0
            else:
                cost = 1

            curr[j] = min(prev[j] + 1, curr[j - 1] + 1, prev[j - 1] + cost)

            if curr[j] < min_in_row:
                min_in_row = curr[j]

        # Pruning condition
        if min_in_row >= d:
            # this row already guarantees distance >= d
            return True

        prev = curr

    return prev[n] >= d
