import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

# .env dosyasını yükle
load_dotenv()

# Ortam değişkenlerinden değerleri al
SENDER_EMAIL = os.getenv("EMAIL_USER")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Sayfa konfigürasyonu
st.set_page_config(
    page_title="Eda Çelikeloğlu - Data Scientist & Mathematician",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Session state varsayılan değerleri (dil ve sekme)
if "language" not in st.session_state:
    st.session_state.language = "Türkçe"
if "selected_section" not in st.session_state:
    st.session_state.selected_section = "home"

# Özel CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

    .main {
        padding-top: 2rem;
    }

    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }

    .hero-title {
        font-family: 'Poppins', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        background: linear-gradient(45deg, #fff, #f0f0f0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: fadeInUp 1s ease-out;
    }

    .hero-subtitle {
        font-family: 'Poppins', sans-serif;
        font-size: 1.2rem;
        font-weight: 300;
        opacity: 0.9;
        animation: fadeInUp 1s ease-out 0.2s both;
    }

    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .skill-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
        border: 1px solid #e0e0e0;
        transition: all 0.3s ease;
        animation: slideInLeft 0.6s ease-out;
    }

    .skill-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(0,0,0,0.15);
    }

    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    .project-card {
        background: linear-gradient(145deg, #f8f9fa, #e9ecef);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        border: 1px solid #dee2e6;
        animation: fadeIn 0.8s ease-out;
    }

    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    .contact-card {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }

    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
        animation: bounceIn 0.8s ease-out;
    }

    @keyframes bounceIn {
        0%, 20%, 40%, 60%, 80% {
            transform: scale(0.8);
            opacity: 0.5;
        }
        100% {
            transform: scale(1);
            opacity: 1;
        }
    }

    .stProgress .st-bo {
        background-color: #667eea;
    }

    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }

    .typing-animation {
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        color: #667eea;
        animation: typing 3s steps(40, end), blink-caret 0.75s step-end infinite;
        white-space: nowrap;
        overflow: hidden;
        border-right: 3px solid #667eea;
    }

    @keyframes typing {
        from { width: 0 }
        to { width: 100% }
    }

    @keyframes blink-caret {
        from, to { border-color: transparent }
        50% { border-color: #667eea }
    }
</style>
""", unsafe_allow_html=True)



# Sekme anahtarlarını sabitle
sections = ["home", "about", "skills", "projects", "contact"]

# Çeviriler
section_labels = {
    "Türkçe": {
        "home": "🏠 Ana Sayfa",
        "about": "👨‍💼 Hakkımda",
        "skills": "🛠️ Yetenekler",
        "projects": "📊 Projeler",
        "contact": "📞 İletişim"
    },
    "English": {
        "home": "🏠 Home",
        "about": "👨‍💼 About",
        "skills": "🛠️ Skills",
        "projects": "📊 Projects",
        "contact": "📞 Contact"
    }
}


# Sidebar tasarımı
with st.sidebar:
    st.markdown("### 🌐 Dil Seçimi / Language")

    def on_language_change():
        st.session_state.language = st.session_state.language_selector

    language = st.selectbox(
        "",
        ["Türkçe", "English"],
        index=["Türkçe", "English"].index(st.session_state.language),
        key="language_selector",
        on_change=on_language_change
    )

    st.markdown("---")
    st.markdown("### 📍 Hızlı Navigasyon")

    labels = [section_labels[st.session_state.language][s] for s in sections]
    current_label = section_labels[st.session_state.language][st.session_state.selected_section]

    selected_label = st.radio(
        "",
        labels,
        index=labels.index(current_label),
        key="nav_selector"
    )

    # Ters eşleme: label -> anahtar
    reverse_map = {v: k for k, v in section_labels[st.session_state.language].items()}
    st.session_state.selected_section = reverse_map[selected_label]

# Kısa değişkenler
language = st.session_state.language
selected_section = st.session_state.selected_section


# İçerik sözlüğü
content = {
    "Türkçe": {
        "hero_title": "Eda Çelikeloğlu",
        "hero_subtitle": "Veri Bilimci | Veri Analisti | Matematikçi",
        "typing_text": "Verilerle hikayeler anlatıyorum...",
        "about_title": "Hakkımda",
        "about_text": """
        Merhaba! Ben Eda, matematik geçmişine sahip, veri bilimi alanına geçiş yapmış tutkulu bir analiz uzmanıyım. 
        6 yıl matematik öğretmenliği yaptıktan sonra, veriye olan ilgim beni bu alana yönlendirdi. Gerçek projelerle 
        veri analizi, görselleştirme ve makine öğrenmesi konularında pratik deneyim kazandım.

        🎓 **Eğitim:** Marmara Üniversitesi Matematik Bölümü (2010-2014)
        
        💼 **Deneyim:** Sahibinden.com Junior Data Scientist (2025)
        
        🔬 **Uzmanlık:** Veri Analizi, Machine Learning, Time Series Modelling
        
        📍 **Konum:** Maltepe, İstanbul
        
        🏆 **Başarılar:** Women in Datathon 1.lik, AI for Life Sciences 3.lük
        """,
        "skills_title": "Teknik Yetenekler",
        "projects_title": "Projelerim",
        "contact_title": "İletişim",
        "stats_title": "İstatistiklerim"
    },
    "English": {
        "hero_title": "Eda Çelikeloğlu",
        "hero_subtitle": "Data Scientist | Data Analyst | Mathematician",
        "typing_text": "I tell stories with data...",
        "about_title": "About Me",
        "about_text": """
        Hello! I'm Eda, a passionate analyst with a mathematics background who transitioned into data science. 
        After 6 years as a mathematics teacher, my interest in data led me to this field. I've gained practical 
        experience in data analysis, visualization, and machine learning through real-world projects.

        🎓 **Education:** Marmara University Mathematics (2010-2014)
        
        💼 **Experience:** Sahibinden.com Junior Data Scientist (2025)
        
        🔬 **Expertise:** Data Analysis, Machine Learning, Time Series Modelling
        
        📍 **Location:** Maltepe, Istanbul
        
        🏆 **Achievements:** Women in Datathon 1st Place, AI for Life Sciences 3rd Place
        """,
        "skills_title": "Technical Skills",
        "projects_title": "My Projects",
        "contact_title": "Contact",
    }
}


# Ana içerik
def show_hero_section():
    st.markdown(f"""
    <div class="hero-section">
        <h1 class="hero-title">{content[language]["hero_title"]}</h1>
        <p class="hero-subtitle">{content[language]["hero_subtitle"]}</p>
        <br>
        <p class="typing-animation">{content[language]["typing_text"]}</p>
    </div>
    """, unsafe_allow_html=True)

    # Profil fotoğrafı bölümü
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 2rem;">
            <div style="width: 250px; height: 250px; border-radius: 50%; 
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        margin: 0 auto; display: flex; align-items: center; justify-content: center;
                        box-shadow: 0 15px 35px rgba(0,0,0,0.2); animation: bounceIn 1.2s ease-out;">
                <span style="font-size: 6rem; color: white;">👩‍💼</span>
            </div>
        </div>
        """, unsafe_allow_html=True)


def show_about_section():
    st.markdown(f"## {content[language]['about_title']}")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(content[language]["about_text"])

    with col2:
        # Profil fotoğrafı placeholder
        st.markdown("""
        <div style="text-align: center; padding: 2rem;">
            <div style="width: 200px; height: 200px; border-radius: 50%; 
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        margin: 0 auto; display: flex; align-items: center; justify-content: center;
                        box-shadow: 0 10px 30px rgba(0,0,0,0.2);">
                <span style="font-size: 4rem; color: white;">👩‍💼</span>
            </div>
        </div>
        """, unsafe_allow_html=True)


def show_skills_section():
    st.markdown(f"## {content[language]['skills_title']}")

    skills_data = {
        "Türkçe": {
            "Programlama": ["Python", "SQL"],
            "Veri Bilimi": ["Pandas", "NumPy", "Scikit-learn", "XGBoost", "LightGBM", "TensorFlow", "Keras"],
            "Görselleştirme": ["Matplotlib", "Seaborn", "Plotly", "Power BI", "Tableau", "Streamlit"],
            "Analiz": ["EDA", "Feature Engineering", "Time Series", "Regression", "Classification"],
            "Araçlar": ["Jupyter", "PyCharm", "VS Code", "GitHub", "Excel"]
        },
        "English": {
            "Programming": ["Python", "SQL"],
            "Data Science": ["Pandas", "NumPy", "Scikit-learn", "XGBoost", "LightGBM", "TensorFlow", "Keras"],
            "Visualization": ["Matplotlib", "Seaborn", "Plotly", "Power BI", "Tableau", "Streamlit"],
            "Analysis": ["EDA", "Feature Engineering", "Time Series", "Regression", "Classification"],
            "Tools": ["Jupyter", "PyCharm", "VS Code", "GitHub", "Excel"]
        }
    }

    cols = st.columns(3)

    for i, (category, skills) in enumerate(skills_data[language].items()):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="skill-card">
                <h4 style="color: #667eea; margin-bottom: 1rem;">{category}</h4>
                {"".join([f"<span style='background: linear-gradient(45deg, #667eea, #764ba2); color: white; padding: 0.3rem 0.8rem; border-radius: 15px; margin: 0.2rem; display: inline-block; font-size: 0.8rem;'>{skill}</span>" for skill in skills])}
            </div>
            """, unsafe_allow_html=True)


def show_projects_section():
    st.markdown(f"## {content[language]['projects_title']}")

    # Yardımcı fonksiyonlar
    def pptx_download_button(label: str, path: str):
        try:
            # Bu örnekte dosya yolu gösterilmiş, gerçek uygulamada dosyayı kontrol edin
            st.markdown(f"""
            <div style="text-align: center; margin: 0.5rem 0;">
                <a href="#" onclick="alert('Sunum dosyası: {path}')" 
                   style="background: linear-gradient(45deg, #667eea, #764ba2); 
                          color: white; padding: 0.7rem 1.5rem; border-radius: 25px; 
                          text-decoration: none; font-weight: 600; display: inline-block;
                          box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
                    {label}
                </a>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Dosya yüklenirken hata: {e}")

    def link_button(label: str, url: str, color_scheme="primary"):
        colors = {
            "primary": "linear-gradient(45deg, #667eea, #764ba2)",
            "secondary": "linear-gradient(45deg, #ff9a9e, #fecfef)",
            "success": "linear-gradient(45deg, #56ab2f, #a8edea)"
        }

        st.markdown(f"""
        <div style="text-align: center; margin: 0.5rem 0;">
            <a href="{url}" target="_blank" 
               style="background: {colors[color_scheme]}; 
                      color: white; padding: 0.7rem 1.5rem; border-radius: 25px; 
                      text-decoration: none; font-weight: 600; display: inline-block;
                      box-shadow: 0 4px 15px rgba(0,0,0,0.2); transition: transform 0.3s;"
               onmouseover="this.style.transform='translateY(-2px)'"
               onmouseout="this.style.transform='translateY(0)'">
                {label}
            </a>
        </div>
        """, unsafe_allow_html=True)

    # Gerçek projeler
    projects = {
        "Türkçe": [
            {
                "başlık": "🏆 UP School & Bitexen Women in Datathon 2024",
                "açıklama": "Kadın istihdamı ve ücret eşitsizliğine yönelik çok değişkenli analiz ve modelleme projesi. Bu çalışmada, istatistiksel yöntemler ve makine öğrenmesi teknikleriyle kadınların iş hayatındaki durumunu analiz ettik.",
                "video": "https://www.youtube.com/watch?v=c_L3OH6Hng4",
                "sunum_link": "assets/Women in Datathon - Mar24.pptx",
                "kodlar": "https://www.kaggle.com/code/edacelikeloglu/1st-place-upschoolxbitexen-datathon-mar24/notebook",
                "etiketler": ["1.lik 🥇", "Python", "Pandas", "Scikit-learn", "Plotly"],
                "sonuçlar": {"Sıralama": "1.lik 🥇", "Katılımcı": "Tüm Takımlar", "Model": "Linear Regression"}
            },
            {
                "başlık": "🌍 AI for Life Sciences – Yeraltı Suyu Tahmini",
                "açıklama": "GRACE uydu verileriyle Avusturya'daki yeraltı suyu seviyelerinin zaman serisi analizi ve 2022-2024 dönemi için tahmin modeli. Meteorolojik değişkenler ve tarihsel verilerle (1930-2021) SMAPE metrikleriyle değerlendirilen tahmin sistemi geliştirdik.",
                "video": "https://www.youtube.com/watch?v=UTqxLyytgKM&t=191s",
                "sunum_link": "assets/AI_for_Life_Sciences_Presentation.pptx",
                "kodlar": "https://github.com/dilaracankaya/AI_4_Life_Sciences_Hackathon2_Task2",
                "etiketler": ["3.lük 🥉", "Time Series", "GRACE Data", "TensorFlow", "SMAPE"],
                "sonuçlar": {"Sıralama": "3.lük 🥉", "Metrik": "SMAPE", "Dönem": "2022-2024"}
            }
        ],
        "English": [
            {
                "title": "🏆 UP School & Bitexen Women in Datathon 2024",
                "desc": "Multivariate analysis and modeling project on women employment and wage inequality. We analyzed women's situation in work life using statistical methods and machine learning techniques.",
                "video": "https://www.youtube.com/watch?v=c_L3OH6Hng4",
                "slide_link": "assets/Women in Datathon - Mar24.pptx",
                "codes": "https://www.kaggle.com/code/edacelikeloglu/1st-place-upschoolxbitexen-datathon-mar24/notebook",
                "tags": ["1st Place 🥇", "Python", "Pandas", "Scikit-learn", "Plotly"],
                "results": {"Ranking": "1st Place 🥇", "Participants": "All Teams", "Model": "Linear Regression"}
            },
            {
                "title": "🌍 AI for Life Sciences – Groundwater Prediction",
                "desc": "Time series analysis and prediction of groundwater levels in Austria using GRACE satellite data. Developed prediction system for 2022-2024 period using historical data (1930-2021) and meteorological variables, evaluated with SMAPE metrics.",
                "video": "https://www.youtube.com/watch?v=UTqxLyytgKM&t=191s",
                "slide_link": "assets/AI_for_Life_Sciences_Presentation.pptx",
                "codes": "https://github.com/dilaracankaya/AI_4_Life_Sciences_Hackathon2_Task2",
                "tags": ["3rd Place 🥉", "Time Series", "GRACE Data", "TensorFlow", "SMAPE"],
                "results": {"Ranking": "3rd Place 🥉", "Metric": "SMAPE", "Period": "2022-2024"}
            }
        ]
    }

    # Türkçe projeler
    if language == "Türkçe":
        for i, proje in enumerate(projects["Türkçe"]):
            # Proje kartı
            st.markdown(f"""
            <div class="project-card" style="animation-delay: {i * 0.2}s;">
                <h3 style="color: #333; margin-bottom: 1rem; font-size: 1.5rem;">{proje["başlık"]}</h3>
                <p style="color: #666; margin-bottom: 1.5rem; line-height: 1.6;">{proje["açıklama"]}</p>
            """, unsafe_allow_html=True)

            # Etiketler
            st.markdown("<div style='margin-bottom: 1rem;'>", unsafe_allow_html=True)
            for etiket in proje["etiketler"]:
                if "1. lik" in etiket:
                    color = "#FFD700"  # Altın renk
                elif "3. lük" in etiket:
                    color = "#CD7F32"  # Bronz renk
                else:
                    color = "#667eea"
                st.markdown(f"""
                <span style='background: {color}; color: white; padding: 0.3rem 0.8rem; 
                           border-radius: 15px; margin: 0.2rem; display: inline-block; 
                           font-size: 0.8rem; font-weight: 600;'>{etiket}</span>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # Video
            if proje["video"]:
                st.video(proje["video"])

            # Sonuçlar
            col1, col2, col3 = st.columns(3)
            for j, (metric, value) in enumerate(proje["sonuçlar"].items()):
                with [col1, col2, col3][j]:
                    st.metric(metric, value)

            # Butonlar
            st.markdown("<br>", unsafe_allow_html=True)
            bcol1, bcol2 = st.columns(2)
            with bcol1:
                pptx_download_button("📥 Sunumu İndir (PPTX)", proje["sunum_link"])
            with bcol2:
                link_button("💻 Kodlara Ulaş", proje["kodlar"], "success")

            st.markdown("</div>", unsafe_allow_html=True)

            if i < len(projects["Türkçe"]) - 1:
                st.markdown("<br><hr><br>", unsafe_allow_html=True)

    # İngilizce projeler
    else:
        for i, project in enumerate(projects["English"]):
            # Project card
            st.markdown(f"""
            <div class="project-card" style="animation-delay: {i * 0.2}s;">
                <h3 style="color: #333; margin-bottom: 1rem; font-size: 1.5rem;">{project["title"]}</h3>
                <p style="color: #666; margin-bottom: 1.5rem; line-height: 1.6;">{project["desc"]}</p>
            """, unsafe_allow_html=True)

            # Tags
            st.markdown("<div style='margin-bottom: 1rem;'>", unsafe_allow_html=True)
            for tag in project["tags"]:
                if "1st Place" in tag:
                    color = "#FFD700"  # Gold color
                elif "3rd Place" in tag:
                    color = "#CD7F32"  # Bronze color
                else:
                    color = "#667eea"
                st.markdown(f"""
                <span style='background: {color}; color: white; padding: 0.3rem 0.8rem; 
                           border-radius: 15px; margin: 0.2rem; display: inline-block; 
                           font-size: 0.8rem; font-weight: 600;'>{tag}</span>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # Video
            if project["video"]:
                st.video(project["video"])

            # Results
            col1, col2, col3 = st.columns(3)
            for j, (metric, value) in enumerate(project["results"].items()):
                with [col1, col2, col3][j]:
                    st.metric(metric, value)

            # Buttons
            st.markdown("<br>", unsafe_allow_html=True)
            bcol1, bcol2 = st.columns(2)
            with bcol1:
                pptx_download_button("📥 Download Slides (PPTX)", project["slide_link"])
            with bcol2:
                link_button("💻 View Code", project["codes"], "success")

            st.markdown("</div>", unsafe_allow_html=True)

            if i < len(projects["English"]) - 1:
                st.markdown("<br><hr><br>", unsafe_allow_html=True)



def show_contact_section():
    st.markdown(f"## {content[language]['contact_title']}")

    col1, col2 = st.columns([2, 1])

    # Sol taraf (bilgi kartı)
    with col1:
        if language == "Türkçe":
            st.markdown("""
            <div class="contact-card">
                <h3>İletişime Geçelim! 🚀</h3>
                <p>Projeleriniz için benimle iletişime geçmekten çekinmeyin.</p>
                <br>
                <p>📧 edacelikeloglu@gmail.com</p>
                <p>💼 linkedin.com/in/eda-celikeloglu</p>
                <p>🐙 github.com/EdaCelikeloglu</p>
                <p>📊 kaggle.com/edacelikeloglu</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="contact-card">
                <h3>Let's Get in Touch! 🚀</h3>
                <p>Feel free to reach out for collaborations or projects.</p>
                <br>
                <p>📧 edacelikeloglu@gmail.com</p>
                <p>💼 linkedin.com/in/eda-celikeloglu</p>
                <p>🐙 github.com/EdaCelikeloglu</p>
                <p>📊 kaggle.com/edacelikeloglu</p>
            </div>
            """, unsafe_allow_html=True)

    # Sağ taraf (form)
    with col2:
        with st.form("contact_form"):
            if language == "Türkçe":
                st.markdown("### Mesaj Gönder")
                name = st.text_input("İsminiz")
                email = st.text_input("E-posta Adresiniz")
                message = st.text_area("Mesaj")
                submit_label = "Gönder"
                success_msg = "Mesajınız gönderildi! Teşekkürler 🙏"
                warning_msg = "Lütfen tüm alanları doldurun."
                subject_prefix = "Yeni mesaj:"
            else:
                st.markdown("### Send a Message")
                name = st.text_input("Your Name")
                email = st.text_input("Your Email")
                message = st.text_area("Message")
                submit_label = "Send"
                success_msg = "Your message has been sent successfully! Thank you 🙏"
                warning_msg = "Please fill out all fields."
                subject_prefix = "New message:"

            submitted = st.form_submit_button(submit_label, use_container_width=True)

            if submitted:
                if name and email and message:
                    sender_email = SENDER_EMAIL
                    receiver_email = RECEIVER_EMAIL
                    password = EMAIL_PASSWORD

                    subject = f"{subject_prefix} {name}"
                    body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

                    msg = MIMEMultipart()
                    msg["From"] = sender_email
                    msg["To"] = receiver_email
                    msg["Subject"] = subject
                    msg["Reply-To"] = email
                    msg.attach(MIMEText(body, "plain"))

                    try:
                        server = smtplib.SMTP("smtp.gmail.com", 587)
                        server.starttls()
                        server.login(sender_email, password)
                        server.send_message(msg)
                        server.quit()
                        st.success(success_msg)
                    except Exception as e:
                        st.error(f"E-posta gönderilirken hata oluştu: {e}")
                else:
                    st.warning(warning_msg)



if selected_section == "home":
    show_hero_section()
elif selected_section == "about":
    show_about_section()
elif selected_section == "skills":
    show_skills_section()
elif selected_section == "projects":
    show_projects_section()
elif selected_section == "contact":
    show_contact_section()


# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; padding: 2rem; color: #666;">
        <p>© 2025 Eda Çelikeloğlu | Made with ❤️ and Streamlit</p>
        <p style="font-size: 0.8rem;">Bu portfolio sürekli güncellenmektedir.</p>
    </div>
    """,
    unsafe_allow_html=True
)