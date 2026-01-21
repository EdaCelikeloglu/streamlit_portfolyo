# Eda Çelikeloğlu - Portfolyo Uygulaması

Bu Streamlit uygulaması, Eda Çelikeloğlu'nun kişisel portfolyosunu sergileyen modern bir web uygulamasıdır.

## 🚀 Özellikler

- **Çok Dilli Destek**: Türkçe ve İngilizce
- **Modern Tasarım**: Gradient renkler ve animasyonlar
- **Responsive**: Mobil ve masaüstü uyumlu
- **İnteraktif Projeler**: Modal popup'lar ile detaylı proje görünümü
- **İletişim Formu**: Email entegrasyonu ile doğrudan mesaj gönderme
- **CV İndirme**: PDF formatında CV indirme özelliği

## 📋 Gereksinimler

- Python 3.8+
- Virtual environment (önerilen)

## 🛠️ Kurulum

### 1. Projeyi klonlayın veya indirin

```bash
git clone <repository-url>
cd portfolyo-app
```

### 2. Virtual environment oluşturun (önerilen)

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Gerekli paketleri yükleyin

```bash
pip install -r requirements.txt
```

### 4. Environment değişkenlerini ayarlayın

`.env` dosyasını oluşturun ve aşağıdaki değişkenleri ekleyin:

```env
EMAIL_USER=your-email@gmail.com
RECEIVER_EMAIL=receiver@gmail.com
EMAIL_PASSWORD=your-app-password
```

**Not**: Gmail için App Password kullanmanız gerekir. [Gmail App Password Rehberi](https://support.google.com/accounts/answer/185833)

### 5. Uygulamayı çalıştırın

```bash
streamlit run app.py
```

Uygulama varsayılan olarak `http://localhost:8501` adresinde çalışacaktır.

## 📁 Proje Yapısı

```
portfolyo-app/
├── app.py              # Ana uygulama dosyası
├── requirements.txt    # Python bağımlılıkları
├── .env               # Environment değişkenleri (oluşturmanız gerekir)
├── .gitignore         # Git ignore dosyası
├── assets/            # Statik dosyalar
│   ├── CV_Eda_Celikeloglu.pdf
│   ├── powerbi1.PNG
│   ├── sahibinden_kapak.png
│   ├── wid_kapak.PNG
│   ├── yeralti_kapak.PNG
│   └── ...
└── README.md          # Bu dosya
```

## 🎨 Tasarım Özellikleri

- **Modern Gradient Tasarım**: Mor-mavi gradient renk paleti
- **Animasyonlar**: CSS animasyonları ve hover efektleri
- **Responsive Layout**: Tüm cihazlarda uyumlu görünüm
- **İnteraktif Elementler**: Hover efektleri ve geçiş animasyonları

## 📧 İletişim Formu Kurulumu

İletişim formunun çalışması için Gmail App Password gereklidir:

1. Gmail hesabınızda 2-Factor Authentication'ı etkinleştirin
2. App Password oluşturun
3. `.env` dosyasında bu bilgileri güncelleyin

## 🔧 Geliştirme

Uygulamayı geliştirmek için:

1. Değişiklikleri yapın
2. Streamlit otomatik olarak değişiklikleri algılar
3. Tarayıcıda sayfayı yenileyin

## 📱 Mobil Uyumluluk

Uygulama responsive tasarıma sahiptir ve mobil cihazlarda da sorunsuz çalışır.

## 🚀 Deployment

Bu uygulamayı aşağıdaki platformlarda deploy edebilirsiniz:

- **Streamlit Cloud**: Ücretsiz hosting
- **Heroku**: Cloud platform
- **Vercel**: Frontend deployment
- **Railway**: Modern deployment platform

## 📄 Lisans

Bu proje kişisel kullanım içindir.

---

**Geliştirici**: Eda Çelikeloğlu  
**İletişim**: edacelikeloglu@gmail.com  
**LinkedIn**: [linkedin.com/in/eda-celikeloglu](https://www.linkedin.com/in/eda-celikeloglu)