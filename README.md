# Eda Çelikeloğlu - Portfolyo Uygulaması

[![Streamlit](https://img.shields.io/badge/Streamlit-1.48.0-FF4B4B?logo=streamlit)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-Personal-blue)](LICENSE)

Bu Streamlit uygulaması, Eda Çelikeloğlu'nun kişisel portfolyosunu sergileyen modern ve interaktif bir web uygulamasıdır.

## 🌟 Canlı Demo

🔗 [Uygulamayı Görüntüle](https://your-app-url.streamlit.app)

## 🚀 Özellikler

- ✅ **Çok Dilli Destek**: Türkçe ve İngilizce
- ✅ **Modern Tasarım**: Gradient renkler ve animasyonlar
- ✅ **Responsive**: Mobil ve masaüstü uyumlu
- ✅ **İnteraktif Projeler**: Modal popup'lar ile detaylı proje görünümü
- ✅ **İletişim Formu**: Email entegrasyonu ile doğrudan mesaj gönderme
- ✅ **CV İndirme**: PDF formatında CV indirme özelliği
- ✅ **Session State**: Kullanıcı tercihlerini saklama
- ✅ **SEO Friendly**: Meta tags ve açıklamalar

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
├── app.py                          # Ana uygulama dosyası
├── app_backup.py                   # Yedek dosya
├── requirements.txt                # Python bağımlılıkları
├── .env                           # Environment değişkenleri (oluşturmanız gerekir)
├── .gitignore                     # Git ignore dosyası
├── README.md                      # Bu dosya
├── KULLANIM_KILAVUZU.md          # Detaylı kullanım rehberi
├── PROJE_DOKUMANTASYONU.md       # Teknik dokümantasyon
├── API_DOKUMANTASYONU.md         # API ve fonksiyon referansı
├── DEPLOYMENT_GUIDE.md           # Deployment rehberi
├── GUVENLIK_REHBERI.md           # Güvenlik best practices
├── CHANGELOG.md                   # Versiyon geçmişi
├── CONTRIBUTING.md                # Katkıda bulunma rehberi
└── assets/                        # Statik dosyalar
    ├── profile_picture.jpg        # Profil fotoğrafı
    ├── CV_Eda_Celikeloglu.pdf    # CV dosyası
    ├── powerbi1.PNG               # Power BI dashboard
    ├── sahibinden_kapak.png       # Proje görselleri
    ├── wid_kapak.PNG
    ├── yeralti_kapak.PNG
    └── ...
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

## 📚 Dokümantasyon

Detaylı bilgi için aşağıdaki dokümanlara göz atın:

- 📖 [Kullanım Kılavuzu](KULLANIM_KILAVUZU.md) - Adım adım kullanım rehberi
- 🏗️ [Proje Dokümantasyonu](PROJE_DOKUMANTASYONU.md) - Teknik mimari ve detaylar
- 🔧 [API Dokümantasyonu](API_DOKUMANTASYONU.md) - Fonksiyon ve API referansı
- 🚀 [Deployment Rehberi](DEPLOYMENT_GUIDE.md) - Canlıya alma adımları
- 🔒 [Güvenlik Rehberi](GUVENLIK_REHBERI.md) - Güvenlik best practices
- 📝 [Changelog](CHANGELOG.md) - Versiyon geçmişi
- 🤝 [Contributing](CONTRIBUTING.md) - Katkıda bulunma rehberi

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Lütfen [CONTRIBUTING.md](CONTRIBUTING.md) dosyasını okuyun.

### Hızlı Başlangıç
1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/yeni-ozellik`)
3. Commit edin (`git commit -m 'feat: yeni özellik eklendi'`)
4. Push edin (`git push origin feature/yeni-ozellik`)
5. Pull Request açın

## 🐛 Hata Bildirimi

Hata bulduysanız lütfen [issue açın](https://github.com/kullanici-adi/portfolyo-app/issues).

## 📊 İstatistikler

- **Toplam Satır**: ~1000+ satır kod
- **Dosya Sayısı**: 15+ dosya
- **Proje Sayısı**: 4 ana proje
- **Dil Desteği**: 2 dil (TR/EN)

## 🙏 Teşekkürler

- [Streamlit](https://streamlit.io) - Framework
- [Google Fonts](https://fonts.google.com) - Poppins font
- [Font Awesome](https://fontawesome.com) - İkonlar

## 📄 Lisans

Bu proje kişisel portfolyo amaçlı geliştirilmiştir.

## 📞 İletişim

**Geliştirici**: Eda Çelikeloğlu  
**E-posta**: edacelikeloglu@gmail.com  
**LinkedIn**: [linkedin.com/in/eda-celikeloglu](https://www.linkedin.com/in/eda-celikeloglu)  
**GitHub**: [github.com/EdaCelikeloglu](https://github.com/EdaCelikeloglu)  
**Kaggle**: [kaggle.com/edacelikeloglu](https://www.kaggle.com/edacelikeloglu)

---

⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın!

**Son Güncelleme**: 23 Ocak 2026 | **Versiyon**: 1.0.0