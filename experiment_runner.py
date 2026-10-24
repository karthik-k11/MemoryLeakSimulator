
import time

from analyzer import analyze_memory
from config import (
    DEFAULT_MEASUREMENT_INTERVAL,
    MAX_DURATION_SECONDS,
    MAX_ITERATIONS,
    MAX_MEMORY_MB,
)
from experiments.growing_dict import create_growing_dict
from experiments.growing_list import create_growing_list
from memory_monitor import get_memory_usage_mb


WORKLOADS = {
    "list": ("Growing List", create_growing_list),
    "dict": ("Growing Dictionary", create_growing_dict),
}


def run_experiment(
    workload="list",
    iterations=10_000,
    measurement_interval=DEFAULT_MEASUREMENT_INTERVAL,
    max_duration=MAX_DURATION_SECONDS,
    max_memory_mb=MAX_MEMORY_MB,
):
    """Run a bounded workload and return its memory analysis."""

    if workload not in WORKLOADS:
        raise ValueError("Unknown workload. Choose 'list' or 'dict'.")

    if (
        not isinstance(iterations, int)
        or isinstance(iterations, bool)
        or iterations <= 0
    ):
        raise ValueError("Iterations must be a positive integer.")

    if iterations > MAX_ITERATIONS:
        raise ValueError(
            f"Iterations cannot exceed {MAX_ITERATIONS}."
        )

    if (
        not isinstance(measurement_interval, int)
        or isinstance(measurement_interval, bool)
        or measurement_interval <= 0
    ):
        raise ValueError(
            "Measurement interval must be a positive integer."
        )

    if max_duration <= 0:
        raise ValueError("Maximum duration must be greater than 0.")

    if max_memory_mb <= 0:
        raise ValueError("Memory limit must be greater than 0.")

    workload_name, _ = WORKLOADS[workload]
    start_time = time.perf_counter()
    deadline = start_time + min(
        float(max_duration),
        MAX_DURATION_SECONDS,
    )

    items = [] if workload == "list" else {}

    measurements = [
        {
            "iteration": 0,
            "item_count": 0,
            "memory_mb": get_memory_usage_mb(),
        }
    ]

    iterations_completed = 0

    for iteration in range(1, iterations + 1):
        if time.perf_counter() >= deadline:
            break

        if get_memory_usage_mb() >= max_memory_mb:
            break

        if workload == "list":
            items.append(iteration)
        else:
            items[iteration] = iteration

        iterations_completed = iteration

        if (
            iteration % measurement_interval == 0
            or iteration == iterations
        ):
            memory_mb = get_memory_usage_mb()

            measurements.append(
                {
                    "iteration": iteration,
                    "item_count": len(items),
                    "memory_mb": memory_mb,
                }
            )

            if memory_mb >= max_memory_mb:
                break

    if measurements[-1]["iteration"] != iterations_completed:
        measurements.append(
            {
                "iteration": iterations_completed,
                "item_count": iterations_completed,
                "memory_mb": get_memory_usage_mb(),
            }
        )

    duration = time.perf_counter() - start_time
    summary = analyze_memory(measurements)

    summary.update(
        {
            "workload": workload,
            "workload_name": workload_name,
            "iterations_completed": iterations_completed,
            "duration_seconds": duration,
            "measurements": measurements,
            "stopped_by_limit": iterations_completed < iterations,
        }
    )

    return summary