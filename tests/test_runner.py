
import pytest

from experiment_runner import run_experiment


def test_runner_completes_list_experiment():
    result = run_experiment(
        workload="list",
        iterations=10,
        measurement_interval=5,
    )

    assert result["iterations_completed"] == 10
    assert result["workload"] == "list"
    assert result["workload_name"] == "Growing List"
    assert len(result["measurements"]) == 3
    assert result["peak_memory_mb"] > 0


def test_runner_completes_dictionary_experiment():
    result = run_experiment(
        workload="dict",
        iterations=10,
        measurement_interval=5,
    )

    assert result["iterations_completed"] == 10
    assert result["workload"] == "dict"
    assert result["workload_name"] == "Growing Dictionary"


def test_runner_rejects_invalid_iterations():
    with pytest.raises(ValueError):
        run_experiment("list", iterations=0)


def test_runner_rejects_unknown_workload():
    with pytest.raises(ValueError):
        run_experiment("string", iterations=10)