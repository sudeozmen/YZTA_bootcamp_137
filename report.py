from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

def create_report_image(orig_np, overlay_np, label):
    """
    Orijinal ve Grad-CAM görüntüsünü yan yana koyup altına
    yalnızca sınıf adını yazan bir PIL Image döner.

    Parameters:
    - orig_np: numpy array, orijinal görüntü (RGB)
    - overlay_np: numpy array, Grad-CAM overlay (RGB)
    - label: str, tahmin edilen sınıf adı

    Returns:
    - PIL.Image object, rapor görseli
    """

    orig_img = Image.fromarray(orig_np)
    overlay_img = Image.fromarray(overlay_np)

    # Görsellerin yan yana toplam genişliği ve en yüksek yükseklik
    total_width = orig_img.width + overlay_img.width
    max_height = max(orig_img.height, overlay_img.height)

    # Alt kısım için ekstra boşluk (sadece etiket için)
    # Metin yüksekliğine göre bu değeri ayarlayabilirsiniz.
    bottom_space = 60 

    # Beyaz arka planlı yeni görsel oluştur
    report_img = Image.new('RGB', (total_width, max_height + bottom_space), (255, 255, 255))

    # Görselleri yapıştır
    report_img.paste(orig_img, (0, 0))
    report_img.paste(overlay_img, (orig_img.width, 0))

    # Metin için çizim aracı
    draw = ImageDraw.Draw(report_img)

    # Yazı tipi dene, yoksa default kullan
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()

    # Metin konumu
    text_x = 10
    text_y = max_height + 10

    # Sadece tahmin edilen sınıfı yaz
    draw.text((text_x, text_y), f"Tahmin Edilen Sınıf: {label}", fill="black", font=font)

    return report_img