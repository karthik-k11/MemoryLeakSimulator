from experiments.growing_list import create_growing_list


def test_growing_list_records_measurements():
    measurements = create_growing_list(
        iterations=10,
        measurement_interval=5,
    )

    assert len(measurements) == 2
    assert measurements[0]["iteration"] == 5
    assert measurements[0]["item_count"] == 5
    assert measurements[1]["iteration"] == 10
    assert measurements[1]["item_count"] == 10