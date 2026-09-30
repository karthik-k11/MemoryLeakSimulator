from experiment_runner import run_experiment


def test_runner_completes_workload():
    executed = []

    def workload(iteration):
        executed.append(iteration)

    result = run_experiment(
        workload=workload,
        iterations=10,
        measurement_interval=5,
    )

    assert result["iterations_completed"] == 10
    assert result["measurements"] == [5, 10]
    assert len(executed) == 10


def test_runner_rejects_invalid_iterations():
    def workload(iteration):
        pass

    try:
        run_experiment(workload, 0)
        assert False
    except ValueError:
        assert True