import streamlit as st
from email_validator import validate_email, EmailNotValidError
from io import BytesIO
from PIL import Image
from model import load_model
from processing import preprocess_image
from gradcam import generate_gradcam
import torch
import numpy as np
import cv2
from report import create_report_image
import sqlite3
import os
from datetime import datetime


# Veritabanı işlemleri
def create_connection():
    return sqlite3.connect("users.db", check_same_thread=False)

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(""" CREATE TABLE IF NOT EXISTS users (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   ad TEXT,
                   yas TEXT,
                   cinsiyet TEXT,
                   email TEXT UNIQUE,
                   sifre TEXT) """)
    conn.commit()
    conn.close()

def insert_user(ad, yas, cinsiyet, email, sifre):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (ad, yas, cinsiyet, email, sifre) VALUES (?, ?, ?, ?, ?)",
                   (ad, yas, cinsiyet, email, sifre))
    conn.commit()
    conn.close()

def check_login(email, sifre):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ? AND sifre = ?", (email, sifre))
    user = cursor.fetchone()
    conn.close()
    return user

def save_report_image(report_img, email):
    # Klasör oluştur (varsa geç)
    os.makedirs("saved_reports", exist_ok=True)

    # Dosya adı oluştur
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{email}_{timestamp}.png"
    filepath = os.path.join("saved_reports", filename)

    # Görüntüyü kaydet
    report_img.save(filepath)

    return filepath  # Dosya yolunu geri döndür

def create_reports_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT,
            image_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


create_table()
create_reports_table()

# Session State Başlangıcı
if "show_register" not in st.session_state:
    st.session_state.show_register = False
if "kayit_oldu" not in st.session_state:
    st.session_state.kayit_oldu = False
if "giris_yapti" not in st.session_state:
    st.session_state.giris_yapti = False
if "accepted" not in st.session_state:
    st.session_state.accepted = False

# Sayfa geçiş fonksiyonları
def switch_to_register():
    st.session_state.show_register = True

def switch_to_login():
    st.session_state.show_register = False


# Giriş ekranı
def login_page():
    st.markdown("<h2 style='text-align:center;'>🔐 Giriş Yap</h2>", unsafe_allow_html=True)
    email = st.text_input("Email")
    sifre = st.text_input("Şifre", type="password")
    if st.button("Giriş Yap"):
        if email and sifre:
            user = check_login(email, sifre)
            if user:
                st.success(f"🎉 Hoş geldiniz, {user[1]}!")
                st.session_state.giris_yapti = True
                st.session_state["email"] = email
            else:
                st.error("❌ E-posta veya şifre hatalı.")
        else:
            st.warning("Lütfen tüm alanları doldurun.")

    st.markdown("""
        <div style='text-align: center; margin-top: 20px;'>
            Henüz hesabınız yok mu? 
        </div>
    """, unsafe_allow_html=True)
    st.button("Kayıt Ol", on_click=switch_to_register)

# Kayıt ekranı
def register_page():
    st.markdown("<h2 style='text-align:center;'>📝 Kullanıcı Kaydı</h2>", unsafe_allow_html=True)
    with st.form("kayit_formu"):
        ad = st.text_input("Ad Soyad")
        yas = st.text_input("Yaş")
        cinsiyet = st.selectbox("Cinsiyet:", ("Kadın", "Erkek", "Diğer"))
        email = st.text_input("Email")
        sifre = st.text_input("Şifre", type="password")
        kaydet = st.form_submit_button("Kayıt Ol")

        if kaydet:
            if ad and yas and cinsiyet and email and sifre:
                try:
                    valid = validate_email(email)
                    insert_user(ad, yas, cinsiyet, email, sifre)
                    st.success("✅ Kayıt başarılı. Lütfen giriş yapın.")
                    st.session_state.show_register = False
                    st.session_state.kayit_oldu = False
                    st.rerun()
                except EmailNotValidError as e:
                    st.error(f"Geçersiz e-posta ❌: {str(e)}")
                except sqlite3.IntegrityError:
                    st.error("❌ Bu e-posta zaten kayıtlı.")
            else:
                st.warning("Lütfen tüm alanları doldurun")

    st.button("Giriş Yap", on_click=switch_to_login)

# Giriş veya kayıt kontrolü
if not st.session_state.giris_yapti and not st.session_state.kayit_oldu:
    if st.session_state.show_register:
        register_page()
    else:
        login_page()


# Giriş başarılıysa
if st.session_state.giris_yapti:
    st.set_page_config(page_title="Alzheimer Sınıflandırma", layout="wide")
    st.markdown("""
    <div style="text-align: center; margin-top: 20px; margin-bottom: 20px;">
        <h1>🧠 Alzheimer Sınıflandırma Sistemi</h1>
        <p style="font-size:18px; color: #555;">Görüntünüzü yükleyin, ön bilgi amaçlı Alzheimer sınıflandırma sonucunu görün.</p>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.accepted:
        st.markdown("""
        <div style="border: 1px solid #ccc; border-radius: 12px; padding: 20px; background-color: #f9f9f9; text-align: center; margin-top: 30px;">
            <h3>📢 Kullanım Bilgilendirmesi</h3>
            <p style="font-size: 16px; line-height: 1.6;">
                Bu sistem yalnızca ön bilgi amaçlıdır. Kullanılan modelin doğruluğu %93'tür. Sağlıkla ilgili nihai kararlar için doktorunuza danışınız.<br>
                Sistemin sunduğu sonuçlar, yüklediğiniz görüntüye dayalı istatistiksel tahminlerdir.<br><br>
                Devam ederek bu sorumluluğu kabul etmiş olursunuz.
            </p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("✅ Kabul Ediyorum"):
                st.session_state.accepted = True
                st.rerun()
        with col2:
            if st.button("❌ Kabul Etmiyorum"):
                st.warning("❗ Devam etmek için kullanım koşullarını kabul etmelisiniz.")

    else:
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

            report_img = create_report_image(orig_np, overlay, label)
            buf = BytesIO()
            report_img.save(buf, format="PNG")
            byte_im = buf.getvalue()

            # Kaydet ve yolunu al
            email = st.session_state.email
            image_path = save_report_image(report_img, st.session_state["email"])

            # Veritabanına bu yolu kaydet
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET mri_image_path = ? WHERE email = ?", (image_path, email))
            conn.commit()
            conn.close()
                     
            # 📥 Raporu kaydet ve yolunu al
            image_path = save_report_image(report_img, st.session_state["email"])

            # 🔄 Veritabanına rapor kaydını ekle
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO reports (user_email, image_path) VALUES (?, ?)", 
               (st.session_state["email"], image_path))
            conn.commit()
            conn.close()

            st.download_button(
                label="📥 Raporu İndir",
                data=byte_im,
                file_name="alzheimer_raporu.png",
                mime="image/png"
            )


            st.markdown("### 📚 Geçmiş Raporlarınız")

            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT image_path, created_at FROM reports WHERE user_email = ? ORDER BY created_at DESC", 
               (st.session_state["email"],))
            raporlar = cursor.fetchall()
            conn.close()

            if raporlar:
              for path, tarih in raporlar:
                if os.path.exists(path):
                  st.image(path, caption=f"Yüklenme Tarihi: {tarih}", use_container_width=True)

            else:
              st.info("Henüz rapor yüklemediniz.")







                              


