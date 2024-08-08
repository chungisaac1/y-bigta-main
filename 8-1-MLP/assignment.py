import numpytorch as npt
from numpytorch import Tensor, nn
from numpytorch import reshape


import numpytorch as npt
from numpytorch import Tensor, nn

class Conv2d(nn.Module):
    def __init__(self, in_channels: int, out_channels: int, kernel_size: int) -> None:
        super().__init__()
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.kernel_size = kernel_size
        self.weight = Tensor(npt.randn(out_channels, in_channels, kernel_size, kernel_size), requires_grad=True)
        self.bias = Tensor(npt.zeros(out_channels), requires_grad=True)

    def forward(self, x: Tensor) -> Tensor:
        return npt.conv2d(x, self.weight, self.bias)

class MaxPool2d(nn.Module):
    def __init__(self, kernel_size: int, stride: int) -> None:
        super().__init__()
        self.kernel_size = kernel_size
        self.stride = stride

    def forward(self, x: Tensor):
        return npt.max_pool2d(x, self.kernel_size, self.stride)

class MNISTClassificationModel(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.conv1 = Conv2d(1, 32, 3)  # (batch_size, 1, 28, 28) -> (batch_size, 32, 26, 26)
        self.pool = MaxPool2d(2, 2)  # (batch_size, 32, 26, 26) -> (batch_size, 32, 13, 13)
        self.conv2 = Conv2d(32, 64, 3)  # (batch_size, 32, 13, 13) -> (batch_size, 64, 11, 11)
        self.fc1 = nn.Linear(64 * 11 * 11, 128)  # (batch_size, 64*11*11) -> (batch_size, 128)
        self.fc2 = nn.Linear(128, 10)  # (batch_size, 128) -> (batch_size, 10)

    def forward(self, x: Tensor) -> Tensor:
        x = self.conv1(x)
        x = self.pool(x)
        x = self.conv2(x)
        x = self.pool(x)
        x = reshape(x, (x.shape[0], -1))
        x = npt.relu(self.fc1(x))
        logits = self.fc2(x)
        return logits