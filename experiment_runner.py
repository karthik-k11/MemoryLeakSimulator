import time

from config import (
    DEFAULT_MEASUREMENT_INTERVAL,
    MAX_DURATION_SECONDS,
    MAX_ITERATIONS,
)


def run_experiment(
    workload,
    iterations,
    measurement_interval=DEFAULT_MEASUREMENT_INTERVAL,
    max_duration=MAX_DURATION_SECONDS,
):
    """Run a controlled workload and return basic execution measurements."""

    if iterations <= 0:
        raise ValueError("Iterations must be greater than 0.")

    if iterations > MAX_ITERATIONS:
        raise ValueError(f"Iterations cannot exceed {MAX_ITERATIONS}.")

    if measurement_interval <= 0:
        raise ValueError("Measurement interval must be greater than 0.")

    start_time = time.time()
    measurements = []

    for iteration in range(1, iterations + 1):
        workload(iteration)

        if iteration % measurement_interval == 0:
            measurements.append(iteration)

        if time.time() - start_time >= max_duration:
            break

    duration = time.time() - start_time

    return {
        "iterations_completed": iteration,
        "duration": duration,
        "measurements": measurements,
    }