import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
import base64
import streamlit.components.v1 as components

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
    body {
        background-color: #F8F9FB;
        color: #2C2C2C;
        font-family: 'Poppins', sans-serif;
    }

    .hero-section {
        background: linear-gradient(135deg, #4A47A3 0%, #6E72C9 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.12);
    }

    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        color: white;
    }

    .hero-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
    }

    a, a:visited {
        color: #4A47A3;
        text-decoration: none;
        font-weight: 500;
    }

    a:hover {
        color: #F4B942;
    }

    .project-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 1.5rem;
    }

    .project-card {
        background: white;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        cursor: pointer;
        overflow: hidden;
        position: relative;
    }

    .project-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
    }

    .project-card img {
        width: 100%;
        height: 180px;
        object-fit: cover;
        border-top-left-radius: 15px;
        border-top-right-radius: 15px;
    }

    .project-card h4 {
        padding: 1rem;
        margin: 0;
        color: #4A47A3;
        font-weight: 600;
        text-align: center;
    }

    .project-popup {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        position: relative;
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
            <div style="width:80px;height:3px;background:#F4B942;margin:0 auto 1rem auto;border-radius:2px;"></div>
            <p class="hero-subtitle">{content[language]["hero_subtitle"]}</p>
            <p style="margin-top:1rem;opacity:0.85;">{content[language]["typing_text"]}</p>
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

    # CV İndirme Butonu
    st.markdown(f"""
    <div style="text-align:center;margin-top:1.5rem;">
        <a href="assets/Eda_Celikeloglu_CV.pdf" download
           style="padding:10px 25px;border-radius:30px;
                  background:#4A47A3;color:white;
                  text-decoration:none;font-weight:500;">
           📄 {'CV’mi İndir' if language == 'Türkçe' else 'Download My CV'}
        </a>
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

import streamlit as st
import os
import streamlit.components.v1 as components

def show_projects_section():
    st.markdown(f"## {content[language]['projects_title']}")

    # CSS
    st.markdown("""
    <style>
        .project-tile {
            background: white;
            border-radius: 15px;
            box-shadow: 0 6px 20px rgba(0,0,0,0.08);
            overflow: hidden;
            cursor: pointer;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            margin-bottom: 1rem;
        }
        .project-tile:hover {
            transform: translateY(-4px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        }
        .project-thumb {
            width: 100%;
            height: 190px;
            object-fit: cover;
        }
        .project-title {
            font-weight: 600;
            color: #4B0082;
            text-align: center;
            padding: 0.8rem;
            font-family: 'Poppins', sans-serif;
        }
        .project-details {
            background: linear-gradient(145deg, #f9f9fb, #f1f1f4);
            padding: 1rem 1.5rem;
            border-radius: 10px;
            margin-top: 0.5rem;
            box-shadow: inset 0 0 8px rgba(0,0,0,0.05);
            animation: fadeIn 0.4s ease;
        }
        @keyframes fadeIn {
            from {opacity: 0;}
            to {opacity: 1;}
        }
        .center-buttons {
            text-align:center;
            margin-top:1rem;
        }
        .link-btn {
            margin:5px;
            padding:8px 20px;
            border-radius:20px;
            color:white;
            text-decoration:none;
        }
    </style>
    """, unsafe_allow_html=True)

    # Proje listesi
    projects = [
        {
            "id": "datathon",
            "title_tr": "🏆 UP School & Bitexen Women in Datathon 2024",
            "title_en": "🏆 UP School & Bitexen Women in Datathon 2024",
            "thumb": "https://raw.githubusercontent.com/EdaCelikeloglu/streamlit_portfolyo/master/assets/wid_kapak.PNG",
            "desc_tr": "Kadın istihdamı ve ücret eşitsizliğine yönelik çok değişkenli analiz ve modelleme projesi.",
            "desc_en": "Multivariate analysis and modeling project on women's employment and wage inequality.",
            "video": "https://www.youtube.com/watch?v=c_L3OH6Hng4",
            "links": [
                ("Sunum", "assets/Women in Datathon - Mar24.pptx", "#667eea", "download"),
                ("Kaggle Notebook", "https://www.kaggle.com/code/edacelikeloglu/1st-place-upschoolxbitexen-datathon-mar24/notebook", "#764ba2", "external")
            ]
        },
        {
            "id": "life_sci",
            "title_tr": "🌍 AI for Life Sciences – Yeraltı Suyu Tahmini",
            "title_en": "🌍 AI for Life Sciences – Groundwater Prediction",
            "thumb": "https://raw.githubusercontent.com/EdaCelikeloglu/streamlit_portfolyo/master/assets/yeralti_kapak.PNG",
            "desc_tr": "GRACE uydu verileriyle Avusturya’daki yeraltı suyu seviyelerinin zaman serisi analizi.",
            "desc_en": "Time series analysis and prediction of groundwater levels in Austria using GRACE satellite data.",
            "video": "https://www.youtube.com/watch?v=UTqxLyytgKM&t=191s",
            "links": [
                ("Sunum", "assets/AI_for_Life_Sciences_Presentation.pptx", "#56ab2f", "download"),
                ("GitHub", "https://github.com/dilaracankaya/AI_4_Life_Sciences_Hackathon2_Task2", "#a8edea", "external")
            ]
        },
        {
            "id": "sahibinden",
            "title_tr": "🏠 Konut Piyasası ve Hava Durumu İlişkisi Analizi",
            "title_en": "🏠 Housing Market & Weather Dynamics in Istanbul",
            "thumb": "https://raw.githubusercontent.com/EdaCelikeloglu/streamlit_portfolyo/master/assets/sahibinden_kapak.png",
            "desc_tr": "İstanbul’daki konut piyasası dinamikleri ile hava durumu koşulları arasındaki ilişkiyi açık veri kaynaklarını entegre ederek analiz ettim. Open-Meteo API’si aracılığıyla gerçek zamanlı meteorolojik verileri topladım ve bu verileri satılık dairelerin görüntülenme ve aranma istatistikleriyle birleştirdim. Zaman serisi modellemesi kullanarak sıcaklık, yağış ve diğer hava değişkenlerinin kullanıcı etkileşim eğilimleri üzerindeki etkisini inceledim. Analizde dışsal hava faktörlerinin etkisini ölçmek için SARIMAX modelinden yararlandım ve elde ettiğim bulguları detaylı bir rapor ve görselleştirmeler eşliğinde sundum.",
            "desc_en": "I analyzed the relationship between housing market dynamics and weather conditions in Istanbul by integrating open data sources. Using the Open-Meteo API, I collected real-time meteorological data and combined it with digital metrics on the views and search volumes of apartments listed for sale. Through time series modeling, I examined how changes in temperature, precipitation, and other weather variables influenced user engagement trends. The analysis employed the SARIMAX model to capture the impact of exogenous weather factors, and I presented the key insights through a detailed report and visualization."
        },
        {
            "id": "powerbi",
            "title_tr": "📊 Satış Analizleri – Power BI Dashboard",
            "title_en": "📊 Sales Analyses – Power BI Dashboard",
            "thumb": "https://raw.githubusercontent.com/EdaCelikeloglu/streamlit_portfolyo/master/assets/powerbi1.PNG",
            "desc_tr": "Power BI ile oluşturduğum bu etkileşimli satış özetleri dashboard’u farklı bölge ve ürün kategorilerindeki performans metriklerini görselleştirir.",
            "desc_en": "An interactive Power BI dashboard visualizing performance metrics across regions and product categories.",
            "pdf": "assets/Eda_Celikeloglu_Sales_Summaries.pdf",
            "powerbi_link": "https://app.powerbi.com/reportEmbed?reportId=d8b1f2ec-5c17-4864-a9d3-64f415eb5f6e&autoAuth=true&ctid=92e0b030-5e40-4cdd-8ff8-51fa8a4504e2"
        }
    ]

    if "open_project" not in st.session_state:
        st.session_state["open_project"] = None

    def toggle_project(pid):
        st.session_state["open_project"] = None if st.session_state["open_project"] == pid else pid

    # 1. satır (ilk 2 proje)
    col1, col2 = st.columns(2)
    for idx, col in enumerate([col1, col2]):
        p = projects[idx]
        with col:
            title = p["title_tr"] if language == "Türkçe" else p["title_en"]
            with st.container():
                st.image(p["thumb"], use_container_width=True)
                if st.button(title, key=f"btn_{p['id']}", use_container_width=True):
                    toggle_project(p["id"])
                if st.session_state["open_project"] == p["id"]:
                    desc = p["desc_tr"] if language == "Türkçe" else p["desc_en"]
                    st.markdown(f"<div class='project-details'>{desc}</div>", unsafe_allow_html=True)
                    if "video" in p:
                        st.video(p["video"])
                    if "links" in p:
                        link_buttons = ""
                        for label, href, color, link_type in p["links"]:
                            if link_type == "download":
                                link_buttons += f"<a href='{href}' download class='link-btn' style='background:{color};'>{label}</a>"
                            else:
                                link_buttons += f"<a href='{href}' target='_blank' class='link-btn' style='background:{color};'>{label}</a>"
                        st.markdown(f"<div class='center-buttons'>{link_buttons}</div>", unsafe_allow_html=True)

    # 2. satır (sahibinden + powerbi)
    col3, col4 = st.columns(2)
    for idx, col in enumerate([col3, col4], start=2):
        p = projects[idx]
        with col:
            title = p["title_tr"] if language == "Türkçe" else p["title_en"]
            with st.container():
                st.image(p["thumb"], use_container_width=True)
                if st.button(title, key=f"btn_{p['id']}", use_container_width=True):
                    toggle_project(p["id"])
                if st.session_state["open_project"] == p["id"]:
                    desc = p["desc_tr"] if language == "Türkçe" else p["desc_en"]
                    st.markdown(f"<div class='project-details'>{desc}</div>", unsafe_allow_html=True)
                    if "pdf" in p:
                        pdf_path = p["pdf"]
                        with open(pdf_path, "rb") as f:
                            pdf_bytes = f.read()
                        components.iframe(
                            "https://docs.google.com/gview?url=https://raw.githubusercontent.com/EdaCelikeloglu/streamlit_portfolyo/master/assets/Eda_Celikeloglu_Sales_Summaries.pdf&embedded=true",
                            height=600)
                        st.download_button(
                            label="📥 PDF İndir" if language == "Türkçe" else "📥 Download PDF",
                            data=pdf_bytes,
                            file_name=os.path.basename(pdf_path),
                            mime="application/pdf"
                        )
                        st.markdown(f"""
                            <div style="text-align:center; margin-top:1rem;">
                                <a href="{p['powerbi_link']}" target="_blank"
                                style="background:linear-gradient(45deg,#764ba2,#667eea);
                                       padding:10px 25px; border-radius:25px; color:white; text-decoration:none;">
                                       🔗 {"Power BI'da Görüntüle" if language == "Türkçe" else "View in Power BI"}
                                </a>
                            </div>
                        """, unsafe_allow_html=True)

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