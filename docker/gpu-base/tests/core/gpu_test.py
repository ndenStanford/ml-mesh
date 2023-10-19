"""GPU test."""

# 3rd party libraries
from pynvml import nvmlDeviceGetHandleByIndex, nvmlDeviceGetMemoryInfo, nvmlInit


def test_profiling_device_usage():
    """Test profiling device usage method.

    Checks:
        - access to GPU device indexed at 0 (default when passing at least 0 GPU to docker run)
        - memory cap on idle GPU
    """
    nvmlInit()
    handle = nvmlDeviceGetHandleByIndex(0)
    info = nvmlDeviceGetMemoryInfo(handle)
    memory_used_mb = info.used // 1024**2

    print(f"Idle GPU memory used (MB): {memory_used_mb}")

    assert memory_used_mb < 350
