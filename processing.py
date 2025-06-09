from PIL import Image
import torch
from torchvision import transforms

def preprocess_image(image, device='cpu'):
    """
    PIL Image alır, 200x190 boyutuna getirir,
    ön işlemden geçirir ve tensor olarak döndürür.
    """
    transform = transforms.Compose([
        transforms.Resize((200, 190)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], 
                             [0.229, 0.224, 0.225])
    ])
    
    image = image.convert("RGB")
    img_tensor = transform(image).unsqueeze(0).to(device)
    
    return img_tensor
