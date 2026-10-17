import math

Z_95 = 1.96


def wilson_interval(successes, trials, z=Z_95):
    """Return the (low, high) Wilson score interval for a proportion."""
    if trials <= 0:
        raise ValueError("trials must be positive")
    if not 0 <= successes <= trials:
        raise ValueError("successes must be between 0 and trials")
    proportion = successes / trials
    z_squared = z * z
    denominator = 1 + z_squared / trials
    center = (proportion + z_squared / (2 * trials)) / denominator
    spread = (
        z
        * math.sqrt(proportion * (1 - proportion) / trials + z_squared / (4 * trials * trials))
        / denominator
    )
    return center - spread, center + spread
