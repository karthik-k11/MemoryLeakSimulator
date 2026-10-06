import pytest

from analyzer import analyze_memory


def test_analyze_memory_calculates_summary():
    measurements = [
        {"iteration": 10, "memory_mb": 20.0},
        {"iteration": 20, "memory_mb": 25.0},
        {"iteration": 30, "memory_mb": 23.0},
    ]

    result = analyze_memory(measurements)

    assert result["initial_memory_mb"] == 20.0
    assert result["peak_memory_mb"] == 25.0
    assert result["final_memory_mb"] == 23.0
    assert result["memory_growth_mb"] == 3.0


def test_analyze_memory_rejects_empty_measurements():
    with pytest.raises(ValueError):
        analyze_memory([])