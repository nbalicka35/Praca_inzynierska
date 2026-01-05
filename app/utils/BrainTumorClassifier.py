import torch
from torchvision import transforms
import cv2
import torch.nn.functional as F
import numpy as np
from PIL import Image

from HistogramEqualization import HistogramEqualization
from ResNet34Model import ResNet34Model


class BrainTumorClassifier:
    def __init__(self, checkpoint_path):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        checkpoint = torch.load(
            checkpoint_path, map_location=self.device, weights_only=False
        )

        self.classes = checkpoint.get(
            "classes",
            ["glioma_tumor", "meningioma_tumor", "no_tumor", "pituitary_tumor"],
        )  # load "classes" key, replace with list of classes if not available.

        self.model = ResNet34Model()
        self.model.load_state_dict(checkpoint["weights"])
        self.model.to(self.device)
        self.model.eval()

        mean = checkpoint["mean"]
        std = checkpoint["std"]
        self.image_size = checkpoint["image_size"]

        self.transform = transforms.Compose(
            [
                transforms.Resize(self.image_size),
                HistogramEqualization(),
                transforms.ToTensor(),
                transforms.Normalize(mean=[mean] * 3, std=[std] * 3),
            ]
        )

    def predict(self, img_path):
        """
        Classifies single picture.
        """
        img = Image.open(img_path).convert("RGB")

        img_trans = self.transform(img)
        img_tensor = img_trans.unsqueeze(0).to(self.device)
        with torch.no_grad():
            out = self.model(img_tensor)
            probs = torch.softmax(out, dim=1)
            pred_idx = probs.argmax(dim=1).item()
            confidence = probs[0, pred_idx].item()

        return {
            "class_name": self.classes[pred_idx],
            "confidence": confidence,
        }

    def predict_batch(self, img_paths):
        """
        Classifies batch of pictures.
        """
        results = []
        for img_path in img_paths:
            res = self.predict(img_path)
            res["filepath"] = img_path
            results.append(res)

        return results

    def generate_gradcam(self, img_tensor, original):
        """
        Generates GradCAM + overlay.
        """
        self.model.eval()
        img_tensor = (
            img_tensor.unsqueeze(0).to(self.device)
            if img_tensor.dim() == 3
            else img_tensor.to(self.device)
        )

        # Forward pass
        out = self.model(img_tensor)
        probs = F.softmax(out, dim=1)
        class_index = out.argmax(dim=1).item()
        confidence = probs[0, class_index].item()

        # Backward pass
        self.model.zero_grad()
        out[:, class_index].backward()

        # Grad-CAM
        grads = self.model.get_activations_gradient()
        pooled_grads = torch.mean(grads, dim=[0, 2, 3])
        activations = self.model.get_activations().clone()

        for i in range(activations.shape[1]):
            activations[:, i, :, :] *= pooled_grads[i]

        heatmap = torch.mean(activations, dim=1).squeeze()
        heatmap = F.relu(heatmap)
        heatmap /= heatmap.max()
        heatmap = heatmap.cpu().numpy()

        # Resize & overlay
        heatmap_resized = cv2.resize(heatmap, (original.shape[1], original.shape[0]))
        heatmap_uint8 = (heatmap_resized * 255).astype(np.uint8)
        heatmap_colored = cv2.applyColorMap(heatmap_uint8, cv2.COLORMAP_JET)

        superimposed = cv2.addWeighted(original, 0.6, heatmap_colored, 0.4, 0)

        return {
            "class_index": class_index,
            "confidence": confidence,
            "heatmap": heatmap_colored,
            "superimposed": superimposed,
        }
