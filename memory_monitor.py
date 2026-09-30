import os

import psutil


def get_memory_usage_mb():
    """Return current process RSS memory usage in megabytes."""
    process = psutil.Process(os.getpid())
    memory_bytes = process.memory_info().rss

    return memory_bytes / (1024 * 1024)