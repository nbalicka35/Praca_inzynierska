import torch.nn as nn
from torchvision import models
from torchvision.models import EfficientNet_B0_Weights


class EfficientNetModel(nn.Module):
    """EfficientNet Model with pretrained ImageNet weights for brain tumor classification"""

    def __init__(self, number_of_classes=4, freeze_features=False):
        super().__init__()

        self.model = models.efficientnet_b0(
            weights=EfficientNet_B0_Weights.IMAGENET1K_V1
        )

        if freeze_features:
            for name, param in self.model.named_parameters():
                if "classifier" not in name:
                    param.requires_grad = True

        in_features = self.model.classifier[1].in_features
        self.model.classifier[1] = nn.Linear(in_features, number_of_classes)

    def forward(self, x):
        return self.model(x)
