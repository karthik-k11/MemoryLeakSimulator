def create_growing_list(iterations, measurement_interval):
    """Create a list gradually and record its size at intervals."""

    items = []
    measurements = []

    for iteration in range(1, iterations + 1):
        items.append(iteration)

        if iteration % measurement_interval == 0:
            measurements.append(
                {
                    "iteration": iteration,
                    "item_count": len(items),
                }
            )

    return measurements