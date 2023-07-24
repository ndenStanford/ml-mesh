import torch

def test_available_gpu():
    
    assert torch.cuda.is_available()
    
def test_current_devive():
    
    torch.cuda.current_device()