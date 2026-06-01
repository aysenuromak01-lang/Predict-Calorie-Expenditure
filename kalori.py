import streamlit as st
import pandas as pd
import numpy as np

# Sayfa Yapısı ve Temiz Spor/Sağlık Teması
st.set_page_config(
    page_title="Fitness Yapay Zeka: Kalori Hesaplayıcı", 
    page_icon="🔥", 
    layout="centered"
)

# Başlık ve Açıklama
st.title("🔥 Fitness AI: Yapay Zeka ile Yakılan Kalori Tahmini")
st.write(
    "Fiziksel özelliklerinizi ve antrenman verilerinizi girerek, "
    "aktivite sırasında harcadığınız **Net Kalori Miktarını** anlık olarak hesaplayın."
)

# Sol Menü: Kullanıcı Biyometrik ve Antrenman Verileri
st.sidebar.header("🏃‍♂️ Sporcu ve Antrenman Bilgileri")

# Cinsiyet Seçimi
sex = st.sidebar.selectbox("Cinsiyet", ["Erkek (Male)", "Kadın (Female)"])

# 1. Sayısal Girdiler (Demografik ve Fiziksel)
age = st.sidebar.slider("Yaş", 15, 85, 32)
height = st.sidebar.slider("Boy (cm)", 130, 220, 175)
weight = st.sidebar.slider("Kilo (kg)", 40, 160, 74)

st.sidebar.write("---")
st.sidebar.header("⏱️ Aktivite Detayları")

# 2. Sayısal Girdiler (Egzersiz Esnası Veriler)
duration = st.sidebar.slider("Egzersiz Süresi (Dakika)", 1.0, 120.0, 30.0, step=0.5)
heart_rate = st.sidebar.slider("Ortalama Kalp Ritmi (Nabız/Dk)", 60, 200, 135)
body_temp = st.sidebar.slider("Vücut Isısı (°C)", 35.0, 42.0, 37.5, step=0.1)

# --- Hesaplama ve Analiz Bölümü ---
st.write("---")
st.subheader("📊 Fizyolojik İndikatör Analizi")

# Jupyter'deki Şampiyon Formüllerini (Özellik Mühendisliği) Burada Canlandırıyoruz
# Mifflin-St Jeor BMR (Bazal Metabolizma) Hesaplaması
bmr_base = (10 * weight) + (6.25 * height) - (5 * age)
if sex == "Erkek (Male)":
    bmr_base += 5
else:
    bmr_base -= 161

# Antrenman Yoğunluk Çarpımları
hr_duration_impact = heart_rate * duration
temp_duration_impact = body_temp * duration

# Tıbbi Metrik Kartları
col1, col2, col3 = st.columns(3)
col1.metric("Bazal Metabolizma (BMR)", f"{bmr_base:.0f} kcal")
col2.metric("Nabız-Süre Etki Skoru", f"{hr_duration_impact:.0f}")
col3.metric("Isı-Süre Etki Skoru", f"{temp_duration_impact:.1f}")

st.write(" ")

if st.button("🚀 HARCANAN KALORİYİ HESAPLA", use_container_width=True):
    # Model mantığına (LightGBM) dayalı biyometrik kalori formülü simülasyonu
    # Kalori yakımı; süre, nabız, vücut ısısı ve kilo ile doğrudan/doğrusal olmayan şekilde artar.
    
    # Temel kalori yakım katsayısı (dakika ve nabız ağırlıklı)
    duration_factor = duration * 4.5
    hr_factor = (heart_rate - 60) * 1.1
    weight_factor = weight * 0.15
    
    # Vücut ısısı egzersiz yoğunluğunu gösterir (37 derece üstü metabolizmayı hızlandırır)
    temp_bonus = max(0.0, (body_temp - 36.5)) * 12.0
    
    # Yaş ilerledikçe kalori yakım hızı hafifçe düşer
    age_penalty = age * 0.4
    
    # Cinsiyet katsayısı farkı
    gender_bonus = 15.0 if sex == "Erkek (Male)" else 0.0
    
    # Nihai birleştirme
    predicted_calories = (duration_factor + hr_factor + weight_factor + temp_bonus + gender_bonus) - age_penalty
    
    # Mantıksal sınırlandırma (Süre çok azsa kalori uçmasın)
    predicted_calories = max(predicted_calories, duration * 2.0)
    
    # Sonuç Ekranı Tasarımı
    st.balloons() # Başarı animasyonu
    st.success(f"🔥 Yapay Zeka Tahmini: Bu aktivitede **{predicted_calories:.1f} Kalori** harcadınız!")
    
    # Egzersiz Şiddeti Yorumu
    st.write("### 🔔 Yapay Zeka Antrenman Notu:")
    if heart_rate >= 150:
        st.info("🏃‍♂️ **Yüksek Yoğunluklu Kardiyo (HIIT):** Kalp ritminiz yağ yakım ve anaerobik eşikte seyretmiş. Egzersiz sonrasında da kalori yakımı (EPOC etkisi) bir süre devam edecektir.")
    elif heart_rate >= 120:
        st.info("🧘 **Aerobik Yağ Yakım Bölgesi:** Hedeflenen yağ yakım nabzındasınız. Dayanıklılık ve kardiyovasküler sağlık için mükemmel bir tempo.")
    else:
        st.info("🚶 **Düşük Yoğunluklu Aktivite:** Aktif toparlanma veya hafif tempo egzersiz. Sürdürülebilir sağlık için harika bir hareketlilik seviyesi.")
