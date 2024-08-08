import numpytorch as npt
from numpytorch import Tensor, nn
from numpytorch import reshape
import numpy as np

# conv2d 함수 구현 (벡터화된 버전)
def conv2d(x: Tensor, weight: Tensor, bias: Tensor = None, stride: int = 1, padding: int = 0) -> Tensor:
    x = x.arr
    weight = weight.arr
    if bias is not None:
        bias = bias.arr

    batch_size, in_channels, in_height, in_width = x.shape
    out_channels, _, kernel_height, kernel_width = weight.shape

    out_height = (in_height - kernel_height + 2 * padding) // stride + 1
    out_width = (in_width - kernel_width + 2 * padding) // stride + 1

    if padding > 0:
        x = np.pad(x, ((0, 0), (0, 0), (padding, padding), (padding, padding)), mode='constant')

    out = np.zeros((batch_size, out_channels, out_height, out_width))

    for b in range(batch_size):
        for c_out in range(out_channels):
            for h in range(out_height):
                for w in range(out_width):
                    out[b, c_out, h, w] = np.sum(
                        x[b, :, h*stride:h*stride+kernel_height, w*stride:w*stride+kernel_width] * weight[c_out]
                    ) + (bias[c_out] if bias is not None else 0)

    return Tensor(out)

# max_pool2d 함수 구현 (벡터화된 버전)
def max_pool2d(x: Tensor, kernel_size: int, stride: int) -> Tensor:
    x = x.arr

    batch_size, channels, in_height, in_width = x.shape

    out_height = (in_height - kernel_size) // stride + 1
    out_width = (in_width - kernel_size) // stride + 1

    out = np.zeros((batch_size, channels, out_height, out_width))

    for b in range(batch_size):
        for c in range(channels):
            for h in range(out_height):
                for w in range(out_width):
                    out[b, c, h, w] = np.max(
                        x[b, c, h*stride:h*stride+kernel_size, w*stride:w*stride+kernel_size]
                    )

    return Tensor(out)

# Conv2d와 MaxPool2d 클래스 업데이트
class Conv2d(nn.Module):
    def __init__(self, in_channels: int, out_channels: int, kernel_size: int) -> None:
        super().__init__()
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.kernel_size = kernel_size
        self.weight = Tensor(np.random.randn(out_channels, in_channels, kernel_size, kernel_size), requires_grad=True)
        self.bias = Tensor(np.zeros(out_channels), requires_grad=True)

    def forward(self, x: Tensor) -> Tensor:
        return conv2d(x, self.weight, self.bias)

class MaxPool2d(nn.Module):
    def __init__(self, kernel_size: int, stride: int) -> None:
        super().__init__()
        self.kernel_size = kernel_size
        self.stride = stride

    def forward(self, x: Tensor):
        return max_pool2d(x, self.kernel_size, self.stride)

class MNISTClassificationModel(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.conv1 = Conv2d(1, 32, 3)  # (batch_size, 1, 28, 28) -> (batch_size, 32, 26, 26)
        self.pool = MaxPool2d(2, 2)  # (batch_size, 32, 26, 26) -> (batch_size, 32, 13, 13)
        self.conv2 = Conv2d(32, 64, 3)  # (batch_size, 32, 13, 13) -> (batch_size, 64, 11, 11)
        self.fc1 = nn.Linear(64 * 5 * 5, 128)  # (batch_size, 64*5*5) -> (batch_size, 128)
        self.fc2 = nn.Linear(128, 10)  # (batch_size, 128) -> (batch_size, 10)

    def forward(self, x: Tensor) -> Tensor:
        x = self.conv1(x)
        x = npt.relu(x)
        x = self.pool(x)
        x = self.conv2(x)
        x = npt.relu(x)
        x = self.pool(x)
        x = reshape(x, (x.shape[0], -1))
        x = npt.relu(self.fc1(x))
        logits = self.fc2(x)
        return logits