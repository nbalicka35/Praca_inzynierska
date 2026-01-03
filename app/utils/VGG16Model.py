import torch.nn as nn
from torchvision import models
from torchvision.models import VGG16_Weights


class VGG16Model(nn.Module):
    """VGG-16 Model with pretrained ImageNet weights for brain tumor classification"""

    def __init__(self, number_of_classes=4, freeze_features=False):
        super().__init__()
        self.model = models.vgg16(weights=VGG16_Weights.IMAGENET1K_V1)

        if freeze_features:
            for param in self.model.features.parameters():
                param.requires_grad = False

        self.model.classifier[-1] = nn.Linear(4096, number_of_classes)

    def forward(self, x):
        return self.model(x)
