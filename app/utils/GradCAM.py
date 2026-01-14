import torch
import torch.nn.functional as F
import cv2
import numpy as np


def generate_gradcam(model, img_tensor, original_img, device):
    """
    Generates GradCAM + overlay.
    """
    model.eval()
    img_tensor = (
        img_tensor.unsqueeze(0).to(device)
        if img_tensor.dim() == 3
        else img_tensor.to(device)
    )

    # Forward pass
    out = model(img_tensor)
    probs = F.softmax(out, dim=1)
    class_index = out.argmax(dim=1).item()
    confidence = probs[0, class_index].item()

    # Backward pass
    model.zero_grad()
    out[:, class_index].backward()

    # Grad-CAM
    grads = model.get_activations_gradient()
    pooled_grads = torch.mean(grads, dim=[0, 2, 3])
    activations = model.get_activations().clone()

    for i in range(activations.shape[1]):
        activations[:, i, :, :] *= pooled_grads[i]

    heatmap = torch.mean(activations, dim=1).squeeze()
    heatmap = F.relu(heatmap)
    heatmap /= heatmap.max()
    heatmap = heatmap.cpu().numpy()

    # Resize & overlay
    heatmap_resized = cv2.resize(
        heatmap, (original_img.shape[1], original_img.shape[0])
    )
    heatmap_uint8 = (heatmap_resized * 255).astype(np.uint8)
    heatmap_colored = cv2.applyColorMap(heatmap_uint8, cv2.COLORMAP_JET)

    superimposed = cv2.addWeighted(original_img, 0.6, heatmap_colored, 0.4, 0)

    return {
        "class_index": class_index,
        "probability": confidence,
        "heatmap": heatmap_colored,
        "superimposed": superimposed,
    }
