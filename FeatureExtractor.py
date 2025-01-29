import torch
import torch.nn as nn
from stable_baselines3.common.torch_layers import BaseFeaturesExtractor

class CustomCNN(BaseFeaturesExtractor):
    def __init__(self, observation_space, features_dim=64):
        super().__init__(observation_space, features_dim)

        # Assuming input shape is (channels, 8, 8)
        n_input_channels = observation_space.shape[0]  # 1 for grayscale, 3 for RGB

        self.cnn = nn.Sequential(
            nn.Conv2d(n_input_channels, 16, kernel_size=3, stride=1, padding=1),  # (8x8) -> (8x8)
            nn.ReLU(),
            nn.Conv2d(16, 32, kernel_size=3, stride=1, padding=1),  # (8x8) -> (8x8)
            nn.ReLU(),
            nn.Flatten(),
        )

        # Compute the output size after convolutions
        with torch.no_grad():
            sample_input = torch.zeros(1, *observation_space.shape)  # (batch, channels, H, W)
            n_flatten = self.cnn(sample_input).shape[1]

        self.linear = nn.Sequential(
            nn.Linear(n_flatten, features_dim),  # Reduce to feature dimension
            nn.ReLU()
        )

    def forward(self, observations):
        return self.linear(self.cnn(observations))
