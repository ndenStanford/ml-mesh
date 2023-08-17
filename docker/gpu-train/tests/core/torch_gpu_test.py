# Standard Library
import os

# ML libs
import torch

# 3rd party libraries
import pytest
from pynvml import nvmlDeviceGetHandleByIndex, nvmlDeviceGetMemoryInfo, nvmlInit


def gpu_utilization():
    nvmlInit()
    handle = nvmlDeviceGetHandleByIndex(0)
    info = nvmlDeviceGetMemoryInfo(handle)
    memory_used_mb = info.used // 1024**2

    return memory_used_mb


@pytest.mark.order(1)
def test_nvidia_smi():
    """Checks the availability of the nvidia driver CLI utility inside the container"""
    os.system("nvidia-smi")


@pytest.mark.order(2)
def test_available_gpu():
    """Checks if torch can see GPU device"""

    assert torch.cuda.is_available()


@pytest.mark.order(3)
def test_current_device():
    """Checks if torch can index the GPU device"""

    gpu_device = torch.cuda.current_device()  # 0

    print(f"GPU device: {gpu_device}")


@pytest.mark.order(4)
def test_current_device_name():
    """Checks if torch can see the specs of GPU device"""

    gpu_device = torch.cuda.current_device()

    gpu_device_name = torch.cuda.get_device_name(
        gpu_device
    )  # 'Telsa T4' on a G4DN type instance

    print(f"GPU device name: {gpu_device_name}")


@pytest.mark.order(5)
def test_current_device_usage():
    """Checks torch's in-built profiling methods"""

    gpu_idle_memory_mb = round(torch.cuda.memory_allocated(0) / 1024**2, 1)
    gpu_idle_reserved_mb = round(torch.cuda.memory_reserved(0) / 1024**2, 1)

    print(f"GPU device allocated memory: {gpu_idle_memory_mb}")
    print(f"GPU device reserved memory: {gpu_idle_reserved_mb}")


@pytest.mark.order(6)
def test_profiling_device_usage():
    """Checks the profiling method of additional library nvidia-ml-py3 by checking for expected GPU
    memory overhead as per
    https://huggingface.co/docs/transformers/perf_train_gpu_one#efficient-training-on-a-single-gpu
    """
    # no data/model pinned to GPU yet
    print(f"GPU device reserved memory (before kernel init): {gpu_utilization()}")
    assert gpu_utilization() < 300

    torch.ones((1, 1)).to("cuda")
    # GPU kernel overhead should be more than 0.75GB
    print(f"GPU device reserved memory (after kernel init): {gpu_utilization()}")
    assert gpu_utilization() > 750
