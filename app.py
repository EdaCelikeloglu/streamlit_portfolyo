import streamlit as st
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

    if language == "Türkçe":
        # 1. Proje
        st.markdown("""
        <div class="project-card" style="animation-delay: 0s;">
            <h3>🏆 UP School & Bitexen Women in Datathon 2024</h3>
            <p>Kadın istihdamı ve ücret eşitsizliğine yönelik çok değişkenli analiz ve modelleme projesi.</p>
        </div>
        """, unsafe_allow_html=True)

        st.video("https://www.youtube.com/watch?v=c_L3OH6Hng4")

        st.markdown("""
        <div style="text-align:center;">
            <a href="assets/Women in Datathon - Mar24.pptx" download 
            style="margin:5px; padding:8px 20px; border-radius:20px; background:#667eea; color:white; text-decoration:none;">Sunum</a>
            <a href="https://www.kaggle.com/code/edacelikeloglu/1st-place-upschoolxbitexen-datathon-mar24/notebook" target="_blank"
            style="margin:5px; padding:8px 20px; border-radius:20px; background:#764ba2; color:white; text-decoration:none;">Kaggle Notebook</a>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)

        # 2. Proje
        st.markdown("""
        <div class="project-card" style="animation-delay: 0.2s;">
            <h3>🌍 AI for Life Sciences – Yeraltı Suyu Tahmini</h3>
            <p>GRACE uydu verileriyle Avusturya'daki yeraltı suyu seviyelerinin zaman serisi analizi.</p>
        </div>
        """, unsafe_allow_html=True)

        st.video("https://www.youtube.com/watch?v=UTqxLyytgKM&t=191s")

        st.markdown("""
        <div style="text-align:center;">
            <a href="assets/AI_for_Life_Sciences_Presentation.pptx" download 
            style="margin:5px; padding:8px 20px; border-radius:20px; background:#56ab2f; color:white; text-decoration:none;">Sunum</a>
            <a href="https://github.com/dilaracankaya/AI_4_Life_Sciences_Hackathon2_Task2" target="_blank"
            style="margin:5px; padding:8px 20px; border-radius:20px; background:#a8edea; color:black; text-decoration:none;">GitHub</a>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)

        # 3. Power BI projesi
        st.markdown("""
        <div class="project-card" style="animation-delay: 0.4s;">
            <h3>📊 Satış Analizleri – Power BI Dashboard</h3>
            <p>Power BI ile oluşturduğum bu etkileşimli satış özetleri dashboard’u,
            farklı bölge ve ürün kategorilerindeki performans metriklerini
            gerçek zamanlı görselleştirir. Veri analizi, görselleştirme ve hikâye
            anlatımı becerilerimin birleştiği bu çalışma, kurumsal karar destek süreçlerinde kullanılabilecek seviyededir.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(
            """
            <iframe title="Eda_Celikeloglu_Sales_Summaries"
            width="100%" height="600"
            src="https://app.powerbi.com/reportEmbed?reportId=d8b1f2ec-5c17-4864-a9d3-64f415eb5f6e&autoAuth=true&ctid=92e0b030-5e40-4cdd-8ff8-51fa8a4504e2"
            frameborder="0" allowFullScreen="true"></iframe>
            """,
            unsafe_allow_html=True
        )

    else:
        # Aynı yapı İngilizce açıklamalarla tekrarlanır
        st.markdown("""
        <div class="project-card" style="animation-delay: 0s;">
            <h3>🏆 UP School & Bitexen Women in Datathon 2024</h3>
            <p>Multivariate analysis and modeling project on women employment and wage inequality.</p>
        </div>
        """, unsafe_allow_html=True)
        st.video("https://www.youtube.com/watch?v=c_L3OH6Hng4")
        st.markdown("""
        <div style="text-align:center;">
            <a href="assets/Women in Datathon - Mar24.pptx" download 
            style="margin:5px; padding:8px 20px; border-radius:20px; background:#667eea; color:white; text-decoration:none;">Slides</a>
            <a href="https://www.kaggle.com/code/edacelikeloglu/1st-place-upschoolxbitexen-datathon-mar24/notebook" target="_blank"
            style="margin:5px; padding:8px 20px; border-radius:20px; background:#764ba2; color:white; text-decoration:none;">Kaggle Notebook</a>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)

        st.markdown("""
        <div class="project-card" style="animation-delay: 0.2s;">
            <h3>🌍 AI for Life Sciences – Groundwater Prediction</h3>
            <p>Time series analysis and prediction of groundwater levels in Austria using GRACE satellite data.</p>
        </div>
        """, unsafe_allow_html=True)
        st.video("https://www.youtube.com/watch?v=UTqxLyytgKM&t=191s")
        st.markdown("""
        <div style="text-align:center;">
            <a href="assets/AI_for_Life_Sciences_Presentation.pptx" download 
            style="margin:5px; padding:8px 20px; border-radius:20px; background:#56ab2f; color:white; text-decoration:none;">Slides</a>
            <a href="https://github.com/dilaracankaya/AI_4_Life_Sciences_Hackathon2_Task2" target="_blank"
            style="margin:5px; padding:8px 20px; border-radius:20px; background:#a8edea; color:black; text-decoration:none;">GitHub</a>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)

        # Power BI (English)
        st.markdown("""
        <div class="project-card" style="animation-delay: 0.4s;">
            <h3>📊 Sales Analyses – Power BI Dashboard</h3>
            <p>This interactive Power BI dashboard visualizes performance metrics
            across regions and product categories in real-time.
            It combines data analysis, visualization, and storytelling skills,
            demonstrating my ability to create decision-support analytics for enterprises.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(
            """
            <iframe title="Eda_Celikeloglu_Sales_Summaries"
            width="100%" height="600"
            src="https://app.powerbi.com/reportEmbed?reportId=d8b1f2ec-5c17-4864-a9d3-64f415eb5f6e&autoAuth=true&ctid=92e0b030-5e40-4cdd-8ff8-51fa8a4504e2"
            frameborder="0" allowFullScreen="true"></iframe>
            """,
            unsafe_allow_html=True
        )




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
        <p style="font-size: 0.8rem;">..</p>
    </div>
    """,
    unsafe_allow_html=True
)