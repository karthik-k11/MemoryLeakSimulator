
import os

import psutil


def get_memory_usage_mb():
    """Return the current Python process's resident memory usage in MB."""
    process = psutil.Process(os.getpid())
    memory_bytes = process.memory_info().rss

    return memory_bytes / (1024 * 1024)