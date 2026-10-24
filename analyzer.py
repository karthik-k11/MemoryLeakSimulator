
def analyze_memory(measurements):
    """Summarize memory usage from an experiment timeline."""

    if not measurements:
        raise ValueError("Measurements cannot be empty.")

    memory_values = [
        float(item["memory_mb"])
        for item in measurements
    ]

    initial_memory = memory_values[0]
    peak_memory = max(memory_values)
    final_memory = memory_values[-1]

    return {
        "initial_memory_mb": initial_memory,
        "peak_memory_mb": peak_memory,
        "final_memory_mb": final_memory,
        "memory_growth_mb": final_memory - initial_memory,
        "measurement_count": len(measurements),
    }