import torch
import torch.nn.functional as F
import numpy as np
import cv2
from PIL import Image

def generate_gradcam(model, input_tensor, target_class=None):
    # Hook'lar için değişkenler
    activations = []
    gradients = []

    def forward_hook(module, input, output):
        activations.append(output)

    def backward_hook(module, grad_in, grad_out):
        gradients.append(grad_out[0])

    # Hedef layer (resnet18'de layer4 son evrişim katmanı)
    target_layer = model.base_model.layer4

    # Hook'ları kaydet
    forward_handle = target_layer.register_forward_hook(forward_hook)
    backward_handle = target_layer.register_backward_hook(backward_hook)

    # İleri geçiş
    output = model(input_tensor)
    if target_class is None:
        target_class = torch.argmax(output, dim=1).item()

    # Geri yayılım
    model.zero_grad()
    class_score = output[0, target_class]
    class_score.backward()

    # Hook sonuçlarını çıkar
    acts = activations[0].squeeze(0).detach().cpu().numpy()
    grads = gradients[0].squeeze(0).detach().cpu().numpy()

    # Grad-CAM hesaplama
    weights = np.mean(grads, axis=(1, 2))
    cam = np.zeros(acts.shape[1:], dtype=np.float32)

    for i, w in enumerate(weights):
        cam += w * acts[i]

    cam = np.maximum(cam, 0)
    cam = cv2.resize(cam, (190, 200))  # 200x190 boyutu burada!
    cam = cam - np.min(cam)
    cam = cam / np.max(cam)
    cam = np.uint8(255 * cam)

    # Hook'ları kapat
    forward_handle.remove()
    backward_handle.remove()

    return cam
