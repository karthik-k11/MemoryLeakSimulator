from memory_monitor import get_memory_usage_mb


def create_growing_list(iterations, measurement_interval):
    """Create a list gradually and record memory usage at intervals."""

    items = []
    measurements = []

    for iteration in range(1, iterations + 1):
        items.append(iteration)

        if iteration % measurement_interval == 0:
            measurements.append(
                {
                    "iteration": iteration,
                    "item_count": len(items),
                    "memory_mb": get_memory_usage_mb(),
                }
            )

    return measurements