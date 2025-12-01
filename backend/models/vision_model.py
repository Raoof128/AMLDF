"""Vision models for AMLD-F."""

import torch.nn as nn
import torch.nn.functional as F


class SimpleCNN(nn.Module):
    """
    A simple Convolutional Neural Network for MNIST-like tasks.

    Structure:
    - Conv2d (1 -> 32)
    - Conv2d (32 -> 64)
    - MaxPool
    - FC (Linear) layers
    """

    def __init__(self):
        """Initialize the network layers."""
        super(SimpleCNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(64 * 7 * 7, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        """
        Forward pass of the network.

        Args:
            x: Input tensor of shape (batch, 1, 28, 28).

        Returns:
            Output logits of shape (batch, 10).
        """
        # Expects x of shape (batch, 1, 28, 28)
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 64 * 7 * 7)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x


def get_vision_model(pretrained=False):
    """
    Create and return a vision model instance.

    Args:
        pretrained: Whether to load pretrained weights (not implemented in demo).

    Returns:
        An instance of SimpleCNN in eval mode.
    """
    model = SimpleCNN()
    if pretrained:
        # In a real scenario, load weights here.
        # model.load_state_dict(torch.load("models/vision_model.pth"))
        pass
    model.eval()
    return model
