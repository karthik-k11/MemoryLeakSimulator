
from experiments.growing_list import create_growing_list


def test_growing_list_records_measurements():
    result = create_growing_list(
        iterations=10,
        measurement_interval=5,
    )

    measurements = result["measurements"]

    assert len(measurements) == 3
    assert measurements[0]["iteration"] == 0
    assert measurements[1]["iteration"] == 5
    assert measurements[2]["iteration"] == 10
    assert measurements[-1]["item_count"] == 10


def test_growing_list_records_memory():
    result = create_growing_list(
        iterations=10,
        measurement_interval=5,
    )

    for measurement in result["measurements"]:
        assert isinstance(measurement["memory_mb"], float)
        assert measurement["memory_mb"] > 0


def test_growing_list_returns_analysis():
    result = create_growing_list(
        iterations=10,
        measurement_interval=5,
    )

    assert result["initial_memory_mb"] > 0
    assert result["peak_memory_mb"] > 0
    assert result["final_memory_mb"] > 0
    assert isinstance(result["memory_growth_mb"], float)
    assert result["duration_seconds"] >= 0
    assert result["iterations_completed"] == 10