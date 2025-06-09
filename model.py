import torch
import torch.nn as nn
from torchvision import models

num_classes = 4

class ResNet18WithDropout(nn.Module):
    def __init__(self, dropout_prob=0.5):
        super(ResNet18WithDropout, self).__init__()
        self.base_model = models.resnet18(pretrained=True)
        in_features = self.base_model.fc.in_features
        self.base_model.fc = nn.Sequential(
            nn.Dropout(dropout_prob),
            nn.Linear(in_features, num_classes)
        )

    def forward(self, x):
        return self.base_model(x)

def load_model(path="alzheimer_model.pth", device='cpu'):
    model = ResNet18WithDropout(dropout_prob=0.5)
    model.load_state_dict(torch.load(path, map_location=device))
    model.to(device)
    model.eval()
    return model
