import torch.nn as nn
from torchvision import models
from torchvision.models import ResNet34_Weights


class ResNet34Model(nn.Module):
    """ResNet34 Model with pretrained ImageNet weights for brain tumor classification"""

    def __init__(self, number_of_classes=4, freeze_features=False):
        super().__init__()

        self.model = models.resnet34(weights=ResNet34_Weights.IMAGENET1K_V1)

        if freeze_features:
            for name, param in self.model.named_parameters():
                if "fc" not in name:
                    param.requires_grad = False

        in_features = self.model.fc.in_features
        self.model.fc = nn.Linear(in_features, number_of_classes)

        self.activations = None
        self.gradients = None

        self.model.layer4.register_forward_hook(self._save_activations)
        self.model.layer4.register_full_backward_hook(self._save_gradients)

    def _save_activations(self, module, input, output):
        self.activations = output.detach()

    def _save_gradients(self, module, grad_input, grad_output):
        self.gradients = grad_output[0].detach()

    def forward(self, x):
        return self.model(x)

    def get_activations_gradient(self):
        return self.gradients

    def get_activations(self):
        return self.activations
