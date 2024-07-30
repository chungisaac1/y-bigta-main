import numpytorch as npt
from numpytorch import Tensor, nn
from numpytorch import reshape


"""
Example model.
If you want to see how main.py works (before you finish the assignment),
try running it through this model.
"""
class MNISTClassificationModel(nn.Module):
    def __init__(self) -> None:
        self.seq = nn.Sequential(
            nn.Linear(784, 256),
            nn.ReLU(),
            nn.Linear(256, 256),
            nn.ReLU(),
            nn.Linear(256, 10, bias=False)
        )

    def forward(self, x: Tensor) -> Tensor:
        x = reshape(x, (x.shape[0], -1))
        logits = self.seq(x)
        return logits

"""
Your model!

class Conv2d(nn.Module):
    def __init__(self, in_channels: int, out_channels: int, kernel_size: int) -> None:
        pass

    def forward(self, x: Tensor) -> Tensor:
        pass


class MaxPool2d(nn.Module):
    def __init__(self, kernel_size: int, stride: int) -> None:
        pass

    def forward(self, x: Tensor):
        pass


class MNISTClassificationModel(nn.Module):
    def __init__(self) -> None:
        pass

    def forward(self, x: Tensor) -> Tensor:
        # Input shape: (batch_size, 1, 28, 28)
        # Return shape: (batch_size, 10)
        pass
"""