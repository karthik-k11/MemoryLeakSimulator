
import time

from analyzer import analyze_memory
from memory_monitor import get_memory_usage_mb


def create_growing_list(iterations, measurement_interval):
    """Create a list and record memory usage at intervals."""

    if iterations <= 0:
        raise ValueError("Iterations must be greater than 0.")

    if measurement_interval <= 0:
        raise ValueError("Measurement interval must be greater than 0.")

    items = []
    measurements = []

    initial_memory = get_memory_usage_mb()
    start_time = time.perf_counter()

    measurements.append({
        "iteration": 0,
        "item_count": 0,
        "memory_mb": initial_memory,
    })

    for iteration in range(1, iterations + 1):
        items.append(iteration)

        if (
            iteration % measurement_interval == 0
            or iteration == iterations
        ):
            measurements.append({
                "iteration": iteration,
                "item_count": len(items),
                "memory_mb": get_memory_usage_mb(),
            })

    duration = time.perf_counter() - start_time
    result = analyze_memory(measurements)

    result["duration_seconds"] = duration
    result["iterations_completed"] = len(items)
    result["measurements"] = measurements

    return result