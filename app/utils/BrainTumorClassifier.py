import torch
from torchvision import transforms
import cv2
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
        image_size = checkpoint["image_size"]

        self.transform = transforms.Compose(
            [
                transforms.Resize(image_size),
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

        return {"class_name": self.classes[pred_idx], "confidence": confidence}

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
