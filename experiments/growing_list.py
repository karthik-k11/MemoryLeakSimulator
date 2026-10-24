
from memory_monitor import get_memory_usage_mb


def create_growing_list(iterations, measurement_interval):
    """Create a list gradually and record process memory usage."""

    if not isinstance(iterations, int) or isinstance(iterations, bool) or iterations <= 0:
        raise ValueError("Iterations must be a positive integer.")

    if (
        not isinstance(measurement_interval, int)
        or isinstance(measurement_interval, bool)
        or measurement_interval <= 0
    ):
        raise ValueError("Measurement interval must be a positive integer.")

    items = []
    measurements = [
        {
            "iteration": 0,
            "item_count": 0,
            "memory_mb": get_memory_usage_mb(),
        }
    ]

    for iteration in range(1, iterations + 1):
        items.append(iteration)

        if (
            iteration % measurement_interval == 0
            or iteration == iterations
        ):
            measurements.append(
                {
                    "iteration": iteration,
                    "item_count": len(items),
                    "memory_mb": get_memory_usage_mb(),
                }
            )

    return measurements