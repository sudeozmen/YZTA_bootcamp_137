import streamlit as st
from io import BytesIO
from PIL import Image
from model import load_model
from processing import preprocess_image
from gradcam import generate_gradcam
import torch
import numpy as np
import cv2
from report import create_report_image

st.set_page_config(page_title="Alzheimer Sınıflandırma", layout="wide")
st.markdown("""
    <div style="text-align: center; margin-top: 20px; margin-bottom: 20px;">
        <h1>🧠 Alzheimer Sınıflandırma Sistemi</h1>
        <p style="font-size:18px; color: #555;">Görüntünüzü yükleyin, ön bilgi amaçlı Alzheimer sınıflandırma sonucunu görün.</p>
    </div>
""", unsafe_allow_html=True)


# Kabul durumu için session state
if "accepted" not in st.session_state:
    st.session_state.accepted = False

if not st.session_state.accepted:
    st.markdown(
        """
        <div style="border: 1px solid #ccc; border-radius: 12px; padding: 20px; background-color: #f9f9f9; text-align: center; margin-top: 30px;">
            <h3>📢 Kullanım Bilgilendirmesi</h3>
            <p style="font-size: 16px; line-height: 1.6;">
                Bu sistem yalnızca ön bilgi amaçlıdır. Kullanılan modelin doğruluğu %93'tür. Sağlıkla ilgili nihai kararlar için doktorunuza danışınız.<br>
                Sistemin sunduğu sonuçlar, yüklediğiniz görüntüye dayalı istatistiksel tahminlerdir.<br><br>
                Devam ederek bu sorumluluğu kabul etmiş olursunuz.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Use a container for centering the columns
    with st.container():
        # Apply custom CSS to center the columns (buttons)
        st.markdown(
            """
            <style>
            .st-emotion-cache-1jm6gmx { /* This targets the columns container specifically */
                display: flex;
                justify-content: center;
                gap: 20px; /* Adjust gap between buttons as needed */
            }
            /* You might need to inspect your Streamlit app to find the exact class name
            for the div that wraps the buttons, as it can change with Streamlit updates.
            Look for something like .st-emotion-cache-xxxxxx where xxxxxx is a hash. */
            </style>
            """,
            unsafe_allow_html=True
        )
        
        col1, col2 = st.columns([1, 1]) # Use equal width columns
        with col1:
            if st.button("✅ Kabul Ediyorum"):
                st.session_state.accepted = True
                st.rerun() # Rerun to hide the disclaimer and show the app content
        with col2:
            if st.button("❌ Kabul Etmiyorum"):
                st.warning("❗ Devam etmek için kullanım koşullarını kabul etmelisiniz.")

else:

    # Asıl uygulama kısmı
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = load_model("alzheimer_model.pth", device=device)

    uploaded_file = st.file_uploader("📤 MRI görüntüsü yükleyin (jpg, png)", type=["jpg", "jpeg", "png"])

    class_info = {
        0: ("Hafif Derecede Demans", "Birey günlük işlevlerini genellikle sürdürebilir; ancak unutkanlık ve karar verme gibi konularda belirgin zorluklar yaşayabilir."),
        1: ("Orta Derecede Demans", "Unutkanlık artmıştır, kişi gündelik aktivitelerde ciddi yardıma ihtiyaç duyabilir."),
        2: ("Demans Yok", "Bireyde Alzheimer’a dair herhangi bir belirti saptanmamıştır."),
        3: ("Çok Hafif Derecede Demans", "Genellikle yaşa bağlı unutkanlıkla karıştırılır; bazı bilişsel zorluklar görülebilir ancak yaşam kalitesini etkilemez.")
    }

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        input_tensor = preprocess_image(image, device=device)

        with torch.no_grad():
            outputs = model(input_tensor)
            probs = torch.softmax(outputs, dim=1)
            predicted_class = torch.argmax(probs, dim=1).item()

        label, description = class_info[predicted_class]

        st.markdown(f"""
            <div style='text-align: center; margin-top: 20px;'>
                <span style='font-size: 20px; font-weight: bold;'>📌 Tahmin Edilen Sınıf:</span><br>
                <span style='font-size: 24px; color: #4CAF50; font-weight: bold;'>{label}</span>
            </div>
        """, unsafe_allow_html=True)

        with st.expander("🧠 Bu sınıf ne anlama geliyor?"):
            st.write(description)

        cam = generate_gradcam(model, input_tensor, target_class=predicted_class)
        orig = image.resize((190, 200)).convert("RGB")
        orig_np = np.array(orig)

        heatmap = cv2.applyColorMap(cam, cv2.COLORMAP_JET)
        heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)
        overlay = cv2.addWeighted(orig_np, 0.6, heatmap, 0.4, 0)

        st.markdown("<h3 style='text-align: center;'>🖼️ Görüntü Karşılaştırması</h3>", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 1], gap="small")

        with col1:
            st.image(orig_np, caption="Orijinal Görüntü", use_container_width=True)
        with col2:
            st.image(overlay, caption="Isı haritası", use_container_width=True)

        with st.expander("📌 Isı Haritası Açıklaması"):
            st.write(
                "- Grad-CAM, modelin tahmin sırasında en çok dikkat ettiği bölgeleri vurgular.\n"
                "- **Kırmızı alanlar** modelin kararında daha etkili bölgeleri gösterir.\n"
                "- Bu sayede modelin nasıl düşündüğünü daha iyi anlayabiliriz."
            )

            # İndirilebilir rapor oluştur
        report_img = create_report_image(orig_np, overlay, label)

        # PIL Image'ı byte stream'e dönüştür
        buf = BytesIO()
        report_img.save(buf, format="PNG")
        byte_im = buf.getvalue()

        st.download_button(
            label="📥 Raporu İndir",
            data=byte_im,
            file_name="alzheimer_raporu.png",
            mime="image/png"
        )
