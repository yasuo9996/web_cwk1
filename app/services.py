from typing import List


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    numerator = sum(a * b for a, b in zip(vec_a, vec_b))
    denom_a = sum(a * a for a in vec_a) ** 0.5
    denom_b = sum(b * b for b in vec_b) ** 0.5
    if denom_a == 0 or denom_b == 0:
        return 0.0
    return numerator / (denom_a * denom_b)
