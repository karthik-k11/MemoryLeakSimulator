from memory_monitor import get_memory_usage_mb


def test_memory_usage_returns_positive_value():
    memory = get_memory_usage_mb()

    assert isinstance(memory, float)
    assert memory > 0