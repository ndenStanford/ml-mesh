
# ML libs
import torch


def test_available_gpu():

    assert torch.cuda.is_available()


def test_current_device():

    torch.cuda.current_device()  # 0


def test_current_device_name():

    gpu_device = torch.cuda.current_device()

    torch.cuda.get_device_name(gpu_device)  # 'Telsa T4' on a G4DN type instance


def test_current_device_usage():

    gpu_device = torch.cuda.current_device()

    torch.cuda.get_device_name(gpu_device)
    round(torch.cuda.memory_allocated(0) / 1024**3, 1)
    round(torch.cuda.memory_reserved(0) / 1024**3, 1)
