# ML libs
import torch

# 3rd party libraries
from pynvml import nvmlDeviceGetHandleByIndex, nvmlDeviceGetMemoryInfo, nvmlInit


def test_available_gpu():
    """Checks if torch can see GPU device"""

    assert torch.cuda.is_available()


def test_current_device():
    """Checks if torch can index the GPU device"""

    torch.cuda.current_device()  # 0


def test_current_device_name():
    """Checks if torch can see the specs of GPU device"""

    gpu_device = torch.cuda.current_device()

    torch.cuda.get_device_name(gpu_device)  # 'Telsa T4' on a G4DN type instance


def test_current_device_usage():
    """Checks torch's in-built profiling methods"""

    gpu_device = torch.cuda.current_device()

    torch.cuda.get_device_name(gpu_device)
    round(torch.cuda.memory_allocated(0) / 1024**3, 1)
    round(torch.cuda.memory_reserved(0) / 1024**3, 1)


def test_profiling_device_usage():
    """Checks the profiling method of additional library nvidia-ml-py3 by checking for expected GPU
    memory overhead as per
    https://huggingface.co/docs/transformers/perf_train_gpu_one#efficient-training-on-a-single-gpu
    """

    torch.ones((1, 1)).to("cuda")

    nvmlInit()
    handle = nvmlDeviceGetHandleByIndex(0)
    info = nvmlDeviceGetMemoryInfo(handle)
    mb_used = info.used // 1024**2
    # GPU kernel overhead should be more than one GB
    assert mb_used > 1000
