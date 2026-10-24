
import pytest

from experiments.growing_dict import create_growing_dict


def test_growing_dict_records_measurements():
    measurements = create_growing_dict(
        iterations=10,
        measurement_interval=5,
    )

    assert len(measurements) == 3
    assert measurements[0]["iteration"] == 0
    assert measurements[1]["iteration"] == 5
    assert measurements[2]["iteration"] == 10
    assert measurements[-1]["item_count"] == 10


def test_growing_dict_records_memory():
    measurements = create_growing_dict(
        iterations=10,
        measurement_interval=5,
    )

    for measurement in measurements:
        assert isinstance(measurement["memory_mb"], float)
        assert measurement["memory_mb"] > 0


def test_growing_dict_rejects_invalid_iterations():
    with pytest.raises(ValueError):
        create_growing_dict(
            iterations=0,
            measurement_interval=5,
        )


def test_growing_dict_rejects_invalid_interval():
    with pytest.raises(ValueError):
        create_growing_dict(
            iterations=10,
            measurement_interval=0,
        )