import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
import streamlit.components.v1 as components
import pyperclip

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
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    body {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8eaf6 50%, #f3e5f5 100%);
        color: #2C2C2C;
        font-family: 'Poppins', sans-serif;
    }

    /* Streamlit main container background */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8eaf6 50%, #f3e5f5 100%);
    }

    /* Header background fix */
    header[data-testid="stHeader"] {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8eaf6 50%, #f3e5f5 100%);
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }

    [data-testid="stSidebar"] * {
        color: white !important;
    }

    [data-testid="stSidebar"] .stMarkdown {
        color: white !important;
    }

    [data-testid="stSidebar"] .stSelectbox label {
        color: white !important;
    }

    [data-testid="stSidebar"] .stRadio label {
        color: white !important;
    }

    /* Selectbox dropdown styling - More specific selectors */
    [data-testid="stSidebar"] .stSelectbox > div > div {
        background-color: rgba(255, 255, 255, 0.95) !important;
    }

    [data-testid="stSidebar"] .stSelectbox option {
        color: #2C2C2C !important;
        background-color: white !important;
    }

    [data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] > div {
        background-color: rgba(255, 255, 255, 0.95) !important;
    }

    [data-testid="stSidebar"] .stSelectbox input {
        color: #2C2C2C !important;
    }

    /* Force all text inside selectbox to be dark */
    [data-testid="stSidebar"] .stSelectbox * {
        color: #2C2C2C !important;
    }

    /* Selected value in selectbox - multiple approaches */
    [data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] span {
        color: #2C2C2C !important;
    }

    [data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] div[role="button"] {
        color: #2C2C2C !important;
    }

    [data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] div[role="button"] span {
        color: #2C2C2C !important;
    }

    [data-testid="stSidebar"] .stSelectbox svg {
        fill: #2C2C2C !important;
    }

    /* Override any white color in selectbox */
    [data-testid="stSidebar"] .stSelectbox [style*="color: white"],
    [data-testid="stSidebar"] .stSelectbox [style*="color: rgb(255, 255, 255)"],
    [data-testid="stSidebar"] .stSelectbox [style*="color:#fff"] {
        color: #2C2C2C !important;
    }

    /* Radio button styling */
    [data-testid="stSidebar"] .stRadio > div {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 0.5rem;
        border-radius: 10px;
    }

    [data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.3) !important;
    }

    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 4rem 2rem;
        border-radius: 25px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 15px 50px rgba(102,126,234,0.3);
        position: relative;
        overflow: hidden;
    }

    .hero-section::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: float 6s ease-in-out infinite;
    }

    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(180deg); }
    }

    .hero-title {
        font-size: 4rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
    }

    .hero-subtitle {
        font-size: 1.4rem;
        opacity: 0.95;
        font-weight: 400;
        position: relative;
        z-index: 1;
    }

    .typing-text {
        font-size: 1.1rem;
        opacity: 0.9;
        font-style: italic;
        margin-top: 1rem;
        position: relative;
        z-index: 1;
    }

    a, a:visited {
        color: #667eea;
        text-decoration: none;
        font-weight: 500;
        transition: all 0.3s ease;
    }

    a:hover {
        color: #764ba2;
        transform: translateY(-1px);
    }

    .project-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
        gap: 2rem;
        margin-top: 2rem;
    }

    .project-card {
        background: white;
        border-radius: 20px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        cursor: pointer;
        overflow: hidden;
        position: relative;
        border: 1px solid rgba(102,126,234,0.1);
    }

    .project-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 20px 40px rgba(102,126,234,0.2);
        border-color: rgba(102,126,234,0.3);
    }

    .project-card img {
        width: 100%;
        height: 200px;
        object-fit: cover;
        transition: transform 0.4s ease;
    }

    .project-card:hover img {
        transform: scale(1.1);
    }

    .project-card h4 {
        padding: 1.5rem;
        margin: 0;
        color: #667eea;
        font-weight: 600;
        text-align: center;
        font-size: 1.1rem;
        line-height: 1.4;
    }

    .skill-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
        border: 1px solid rgba(102,126,234,0.1);
    }

    .skill-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(102,126,234,0.15);
    }

    .skill-tag {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.3rem;
        display: inline-block;
        font-size: 0.9rem;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(102,126,234,0.3);
    }

    .skill-tag:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102,126,234,0.4);
    }

    .contact-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        box-shadow: 0 10px 30px rgba(102,126,234,0.4);
        margin-bottom: 2rem;
    }

    .contact-form-card {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        padding: 2rem 2rem 0.5rem 2rem;
        border-radius: 20px 20px 0 0;
        box-shadow: 0 10px 30px rgba(118,75,162,0.4);
        border: 1px solid rgba(255,255,255,0.2);
        margin-bottom: 0;
    }

    /* Form container - daha spesifik selector */
    div[data-testid="stForm"] {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%) !important;
        padding: 0.5rem 2rem 2rem 2rem !important;
        border-radius: 0 0 20px 20px !important;
        margin-top: 0 !important;
        box-shadow: 0 10px 30px rgba(118,75,162,0.4) !important;
    }

    div[data-testid="stForm"] label {
        color: white !important;
        font-weight: 500 !important;
    }

    div[data-testid="stForm"] input,
    div[data-testid="stForm"] textarea {
        background-color: rgba(255, 255, 255, 0.95) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        color: #2C2C2C !important;
        border-radius: 10px !important;
    }

    /* Gönder butonu - çok spesifik selector */
    div[data-testid="stForm"] button[type="submit"],
    div[data-testid="stForm"] button[kind="primary"],
    div[data-testid="stForm"] .stButton > button {
        background: white !important;
        background-color: white !important;
        color: #764ba2 !important;
        border: none !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        padding: 0.7rem 1.5rem !important;
        border-radius: 25px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
        transition: all 0.3s ease !important;
    }

    div[data-testid="stForm"] button[type="submit"]:hover,
    div[data-testid="stForm"] button[kind="primary"]:hover,
    div[data-testid="stForm"] .stButton > button:hover {
        background: rgba(255, 255, 255, 0.9) !important;
        background-color: rgba(255, 255, 255, 0.9) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 16px rgba(0,0,0,0.3) !important;
    }

    .about-card {
        background: white;
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        border: 1px solid rgba(102,126,234,0.1);
    }

    .profile-avatar {
        width: 280px;
        height: 280px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        margin: 0 auto;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 20px 40px rgba(102,126,234,0.3);
        animation: pulse 2s infinite;
        position: relative;
        overflow: hidden;
    }

    .profile-avatar::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: conic-gradient(transparent, rgba(255,255,255,0.3), transparent);
        animation: rotate 4s linear infinite;
    }

    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }

    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    .stats-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }

    .stat-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        border: 1px solid rgba(102,126,234,0.1);
        transition: all 0.3s ease;
    }

    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(102,126,234,0.15);
    }

    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: #667eea;
        margin-bottom: 0.5rem;
    }

    .stat-label {
        color: #666;
        font-weight: 500;
    }

    /* CV Download Button Styling */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        padding: 15px 35px !important;
        border-radius: 30px !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        box-shadow: 0 8px 25px rgba(102,126,234,0.4) !important;
        transition: all 0.3s ease !important;
        font-family: 'Poppins', sans-serif !important;
    }

    .stDownloadButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 35px rgba(102,126,234,0.6) !important;
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%) !important;
    }

    .stDownloadButton > button:active {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(102,126,234,0.5) !important;
    }

    /* Profile Image Styling */
    .profile-image-hero img {
        border-radius: 50% !important;
        width: 280px !important;
        height: 280px !important;
        object-fit: cover !important;
        box-shadow: 0 20px 40px rgba(102,126,234,0.3) !important;
        border: 5px solid white !important;
    }

    .profile-image-about img {
        border-radius: 50% !important;
        width: 200px !important;
        height: 200px !important;
        object-fit: cover !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2) !important;
        border: 4px solid white !important;
    }

    /* Streamlit image container override */
    div[data-testid="stImage"] img {
        border-radius: inherit !important;
    }

    .profile-image-hero div[data-testid="stImage"] img {
        border-radius: 50% !important;
        width: 280px !important;
        height: 280px !important;
        object-fit: cover !important;
    }

    .profile-image-about div[data-testid="stImage"] img {
        border-radius: 50% !important;
        width: 200px !important;
        height: 200px !important;
        object-fit: cover !important;
    }

    /* Testimonials Styling */
    .testimonial-card {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        border-left: 5px solid #667eea;
        transition: all 0.3s ease;
    }
    
    .testimonial-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 35px rgba(102,126,234,0.2);
    }
    
    .testimonial-header {
        display: flex;
        align-items: center;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid #f0f0f0;
    }
    
    .testimonial-avatar {
        width: 70px;
        height: 70px;
        border-radius: 50%;
        margin-right: 1.5rem;
        border: 3px solid #667eea;
        object-fit: cover;
    }
    
    .testimonial-info h4 {
        margin: 0;
        color: #667eea;
        font-size: 1.2rem;
        font-weight: 600;
    }
    
    .testimonial-info .role {
        margin: 0.3rem 0 0 0;
        color: #666;
        font-size: 0.95rem;
        line-height: 1.4;
    }
    
    .testimonial-date {
        color: #999;
        font-size: 0.85rem;
        margin-top: 0.3rem;
    }
    
    .testimonial-text {
        color: #2C2C2C;
        font-size: 1rem;
        line-height: 1.7;
        margin: 1rem 0;
        text-align: justify;
    }
    
    .testimonial-text p {
        margin-bottom: 1rem;
    }
    
    .linkedin-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: white !important;
        color: #0077B5 !important;
        padding: 0.6rem 1.2rem;
        border-radius: 25px;
        text-decoration: none !important;
        font-size: 0.9rem;
        font-weight: 600;
        transition: all 0.3s ease;
        margin-top: 1rem;
        border: 2px solid #0077B5;
    }
    
    .linkedin-badge:hover {
        background: #0077B5 !important;
        color: white !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,119,181,0.3);
    }
    
    .linkedin-badge span {
        color: inherit !important;
    }
    
    .linkedin-icon {
        width: 18px;
        height: 18px;
    }
    
    /* İletişim sayfası - buton linkleri */
    .contact-card a {
        border: none !important;
        border-bottom: none !important;
        color: white !important;
    }
    
    /* İletişim formu - section selector */
    section[data-testid="stForm"] {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%) !important;
        padding: 2rem !important;
        border-radius: 20px !important;
        box-shadow: 0 10px 30px rgba(118,75,162,0.4) !important;
        min-height: 450px !important;
    }
    
    section[data-testid="stForm"] h3 {
        color: white !important;
        text-align: center !important;
        margin-bottom: 1.5rem !important;
        margin-top: 0 !important;
    }
    
    section[data-testid="stForm"] label {
        color: white !important;
        font-weight: 500 !important;
    }
    
    section[data-testid="stForm"] input,
    section[data-testid="stForm"] textarea {
        background-color: rgba(255, 255, 255, 0.95) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        color: #2C2C2C !important;
        border-radius: 10px !important;
    }
    
    section[data-testid="stForm"] button {
        background: white !important;
        background-color: white !important;
        color: #764ba2 !important;
        border: none !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        padding: 0.7rem 1.5rem !important;
        border-radius: 25px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
    }
    
    section[data-testid="stForm"] button:hover {
        background: rgba(255, 255, 255, 0.9) !important;
        background-color: rgba(255, 255, 255, 0.9) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 16px rgba(0,0,0,0.3) !important;
    }
    
    div[data-testid="stForm"] {
        border-radius: 20px !important;
    }
</style>
""", unsafe_allow_html=True)




# Sekme anahtarlarını sabitle
sections = ["home", "about", "skills", "projects", "testimonials", "contact"]

# Çeviriler
section_labels = {
    "Türkçe": {
        "home": "🏠 Ana Sayfa",
        "about": "👨‍💼 Hakkımda",
        "skills": "🛠️ Yetenekler",
        "projects": "📊 Projeler",
        "testimonials": "💬 Referanslar",
        "contact": "📞 İletişim"
    },
    "English": {
        "home": "🏠 Home",
        "about": "👨‍💼 About",
        "skills": "🛠️ Skills",
        "projects": "📊 Projects",
        "testimonials": "💬 Testimonials",
        "contact": "📞 Contact"
    }
}


# Sidebar tasarımı
with st.sidebar:
    st.markdown("### 🌐 Dil Seçimi / Language")

    def on_language_change():
        st.session_state.language = st.session_state.language_selector

    language = st.selectbox(
        "Dil / Language",
        ["Türkçe", "English"],
        index=["Türkçe", "English"].index(st.session_state.language),
        key="language_selector",
        on_change=on_language_change
    )

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
        "testimonials_title": "Referanslar",
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
        "testimonials_title": "Testimonials",
        "contact_title": "Contact",
    }
}


# Ana içerik
def show_hero_section():
    import base64
    with open("assets/profile_picture.jpg", "rb") as img_file:
        img_data = base64.b64encode(img_file.read()).decode()
    
    st.markdown(f"""
        <div class="hero-section" style="display: flex; align-items: center; justify-content: space-between; padding: 3rem 4rem;">
            <div style="flex: 1; text-align: left;">
                <h1 class="hero-title" style="text-align: left;">{content[language]["hero_title"]}</h1>
                <p class="hero-subtitle" style="text-align: left; margin-top: 1rem;">{content[language]["hero_subtitle"]}</p>
                <p class="typing-text" style="text-align: left;">{content[language]["typing_text"]}</p>
            </div>
            <div style="flex: 0 0 auto; margin-left: 3rem;">
                <img src="data:image/jpeg;base64,{img_data}" 
                     style="width: 250px; height: 250px; border-radius: 50%; 
                            object-fit: cover; box-shadow: 0 20px 40px rgba(0,0,0,0.3);
                            border: 5px solid white; position: relative; z-index: 2;">
            </div>
        </div>
        """, unsafe_allow_html=True)

    # İstatistik kartları
    stats_labels = {
        "Türkçe": {
            "experience": "Yıl Deneyim",
            "projects": "Proje",
            "awards": "Yarışma Ödülü",
            "technologies": "Teknoloji"
        },
        "English": {
            "experience": "Years Experience",
            "projects": "Projects",
            "awards": "Competition Awards",
            "technologies": "Technologies"
        }
    }
    
    st.markdown(f"""
    <div class="stats-container">
        <div class="stat-card">
            <div class="stat-number">6+</div>
            <div class="stat-label">{stats_labels[language]["experience"]}</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">4+</div>
            <div class="stat-label">{stats_labels[language]["projects"]}</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">2</div>
            <div class="stat-label">{stats_labels[language]["awards"]}</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">10+</div>
            <div class="stat-label">{stats_labels[language]["technologies"]}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def show_about_section():
    st.markdown(f"## {content[language]['about_title']}")

    # Streamlit markdown ile göster
    st.markdown(content[language]["about_text"])

    # CV İndirme Butonu - Streamlit Download Button
    try:
        with open("assets/CV_Eda_Celikeloglu.pdf", "rb") as pdf_file:
            pdf_data = pdf_file.read()
        
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            cv_label = "📄 CV'mi İndir" if language == 'Türkçe' else "📄 Download My CV"
            st.download_button(
                label=cv_label,
                data=pdf_data,
                file_name="CV_Eda_Celikeloglu.pdf",
                mime="application/pdf",
                use_container_width=True
            )
    except FileNotFoundError:
        st.error("CV dosyası bulunamadı!")


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
                <h4 style="color: #667eea; margin-bottom: 1.5rem; font-size: 1.3rem; font-weight: 600;">{category}</h4>
                {"".join([f"<span class='skill-tag'>{skill}</span>" for skill in skills])}
            </div>
            """, unsafe_allow_html=True)

import json
import streamlit as st
import streamlit.components.v1 as components

def show_projects_section():
    st.markdown(f"## {content[language]['projects_title']}")

    # ===== CSS (grid + kart) =====
    st.markdown("""
    <style>
      .proj-card{
        background:#fff;border-radius:14px;box-shadow:0 6px 18px rgba(0,0,0,.08);
        padding:12px 12px 16px;transition:transform .2s ease, box-shadow .2s ease;margin-bottom:18px;
      }
      .proj-card:hover{ transform:translateY(-3px); box-shadow:0 12px 26px rgba(0,0,0,.14); }
      .proj-title{
        font-family:'Poppins',sans-serif;font-weight:600;color:#4B0082;margin:6px 0 10px;text-align:center;
      }
      .proj-thumb{ width:100%; height:190px; object-fit:cover; border-radius:10px; }
    </style>
    """, unsafe_allow_html=True)

    t = (language == "Türkçe")
    lbl_view_details = "📌 Ayrıntılar için tıklayınız" if t else "📌 Click to view details"

    # ===== Projeler =====
    projects = [
        {
            "id":"youtube_ai",
            "title":"🤖 YouTube AI Scraping Agent",
            "title_tr":"🤖 YouTube AI Scraping Agent",
            "title_en":"🤖 YouTube AI Scraping Agent",
            "thumb":"https://raw.githubusercontent.com/EdaCelikeloglu/streamlit_portfolyo/master/assets/youtube_ai_kapak.png",
            "desc_tr":"Bir YouTube bağlantısı üzerinden sanatçı tespiti yapan ve ilgili sanatçının ilk stüdyo albümündeki tüm şarkı sözlerini otomatik olarak analiz eden bir yazılım projesi geliştirdim. Python tabanlı bu sistemde, Genius platformundan veri çekmek için Apify araçlarını kullanırken, albüm bilgilerini belirlemek için yapay zeka modellerinden yararlandım. Süreç boyunca her şarkı için karakter, kelime ve token sayıları hesaplayarak yapılandırılmış veriler oluşturdum. Elde ettiğim verileri, MD5 karma değerleri ve vektör gömmeleri aracılığıyla teknik bir analize dönüştürerek sundum. Proje, özellikle veri kazıma ve dil modellerinin entegrasyonu ile deterministik çıktılar üretmeye odaklanıyor.",
            "desc_en":"I developed a software project that detects artists from a YouTube link and automatically analyzes all lyrics from the artist's first studio album. In this Python-based system, I used Apify tools to scrape data from the Genius platform while leveraging AI models to determine album information. Throughout the process, I calculated character, word, and token counts for each song to create structured data. I transformed the obtained data into technical analysis through MD5 hash values and vector embeddings. The project focuses on producing deterministic outputs through data scraping and language model integration.",
            "pdf_raw":"https://raw.githubusercontent.com/EdaCelikeloglu/streamlit_portfolyo/master/assets/YouTube_AI_Scraping_Agent.pdf",
            "links":[
                {"label_tr":"GitHub","label_en":"GitHub","href":"https://github.com/EdaCelikeloglu/youtube-ai-scraping-agent"}
            ]
        },
        {
            "id":"physical_therapy",
            "title":"� Fizik Tedavi Veri Analizi",
            "title_tr":"� Fizik Tedavi Veri Analizi",
            "title_en":"� Physical Therapy Data Analysis",
            "thumb":"https://raw.githubusercontent.com/EdaCelikeloglu/streamlit_portfolyo/master/assets/Klinik_veri_rehabilitasyon_hatti_kapak.png",
            "desc_tr":"Ham klinik verileri işleyerek analize hazır hale getiren Python tabanlı uçtan uca bir veri işleme hattı geliştirdim. Sistemde; verilerin temizlenmesi, metinsel sürelerin sayısallaştırılması, normalizasyon kurallarının uygulanması ve KNN algoritması ile eksik değerlerin doldurulması gibi kritik aşamaları uyguladım. Fizyoterapi odaklı hazırladığım bu projede, karmaşık sağlık kayıtlarını düzenli bir yapıya kavuşturarak modellemeye uygun veri setleri ve görsel raporlar ürettim. Süreç boyunca kategorik verilerin dönüştürülmesi, özellik mühendisliği ve verilerin anonimleştirilmesi gibi veri bilimi tekniklerini etkin bir şekilde kullandım. Projede yer alan kurallar dizini sayesinde normalizasyon işlemlerini özelleştirilebilir hale getirdim ve hazırladığım boru hattını yerel ortamlarda kolayca çalıştırılabilir şekilde tasarladım. Projenin temel amacı, dağınık haldeki klinik kayıtları standartlaştırılmış ve ölçeklendirilmiş nihai bir tabloya dönüştürmek.",
            "desc_en":"I developed an end-to-end Python-based data processing pipeline that transforms raw clinical data into analysis-ready format. In the system, I implemented critical stages such as data cleaning, numerical conversion of textual durations, application of normalization rules, and filling missing values using the KNN algorithm. In this physiotherapy-focused project, I organized complex health records into a structured format, producing modeling-ready datasets and visual reports. Throughout the process, I effectively utilized data science techniques such as categorical data transformation, feature engineering, and data anonymization. Through the rules directory in the project, I made normalization processes customizable and designed the pipeline to be easily executable in local environments. The main goal of the project is to transform scattered clinical records into a standardized and scaled final table.",
            "pdf_raw":"https://raw.githubusercontent.com/EdaCelikeloglu/streamlit_portfolyo/master/assets/Klinik_veri_rehabilitasyon_hatti.pdf",
            "links":[
                {"label_tr":"GitHub","label_en":"GitHub","href":"https://github.com/EdaCelikeloglu/Physical_Therapy_Data_Analysis_Project"}
            ]
        },
        {
            "id":"datathon",
            "title":"🏆 UP School & Bitexen Women in Datathon 2024",
            "title_tr":"🏆 UP School & Bitexen Women in Datathon 2024",
            "title_en":"🏆 UP School & Bitexen Women in Datathon 2024",
            "thumb":"https://raw.githubusercontent.com/EdaCelikeloglu/streamlit_portfolyo/master/assets/wid_kapak.PNG",
            "desc_tr": """Kadınların iş gücüne katılımı, sağlık, toplumsal cinsiyet rolleri ve siyasi temsiliyetin ücret eşitsizliği üzerindeki etkisini analiz etmek için çoklu doğrusal regresyon modeli oluşturdum.
Toplumsal cinsiyet rollerinin işe yerleşim üzerindeki etkisini incelemek amacıyla lojistik regresyon uyguladım.
Üç kişilik bir ekipte iş birliği içinde çalışarak planlama, ekip çalışması ve zaman yönetimi becerilerimi geliştirdim.
Tüm katılımcılar arasında birincilik elde ettim.""",
            "desc_en": """Built a multiple linear regression model to analyze the influence of women's labor force participation, health, gender roles, and political representation on wage inequality.
Applied logistic regression to examine how gender roles impact job placement.
Collaborated in a team of three, gaining experience in planning, teamwork, and time management.
Achieved first place among all participants.""",
            "video":"https://www.youtube.com/watch?v=c_L3OH6Hng4",
            "links":[
                {"label_tr":"Sunum (PPTX)","label_en":"Presentation (PPTX)","href":"https://raw.githubusercontent.com/EdaCelikeloglu/streamlit_portfolyo/master/assets/Women%20in%20Datathon%20-%20Mar24.pptx"},
                {"label_tr":"Kaggle Notebook","label_en":"Kaggle Notebook","href":"https://www.kaggle.com/code/edacelikeloglu/1st-place-upschoolxbitexen-datathon-mar24/notebook"}
            ]
        },
        {
            "id":"life_sci",
            "title":"🌍 AI for Life Sciences - Groundwater Prediction",
            "title_tr":"🌍 AI for Life Sciences - Yeraltı Suyu Tahmini",
            "title_en":"🌍 AI for Life Sciences - Groundwater Prediction",
            "thumb":"https://raw.githubusercontent.com/EdaCelikeloglu/streamlit_portfolyo/master/assets/yeralti_kapak.PNG",
            "desc_tr": """Gradient Zero ve Viyana Üniversitesi iş birliğiyle düzenlenen bir yarışmada Taikai platformu üzerinden takım projesine katkıda bulundum.
Yeraltı su seviyesi tahmini: 1930-2021 verileri ve dışsal değişkenlerle 2022-2024 tahminleri; SMAPE ile değerlendirildi.
GRACE serileri için dışsal değişkenler (hava, yağış, kar erimesi, yüzey sıcaklığı) belirlendi.
Python (TensorFlow, Keras, scikit-learn, xarray) ile modelleme yapıldı; sunum videosu ve kaynak kod sağlandı.""",
            "desc_en": """Participated in a competition organized by Gradient Zero with the University of Vienna on Taikai.
Groundwater level prediction for Austria (2022-2024) using 1930-2021 history and exogenous variables (SMAPE for accuracy).
Identified GRACE external drivers: weather, precipitation, snowmelt, temperature.
Modeling with Python (TensorFlow, Keras, scikit-learn, xarray); delivered source code and a presentation video.""",
            "video":"https://www.youtube.com/watch?v=UTqxLyytgKM",
            "links":[
                {"label_tr":"Sunum (PPTX)","label_en":"Presentation (PPTX)","href":"https://raw.githubusercontent.com/EdaCelikeloglu/streamlit_portfolyo/master/assets/AI_for_Life_Sciences_Presentation.pptx"},
                {"label_tr":"GitHub","label_en":"GitHub","href":"https://github.com/dilaracankaya/AI_4_Life_Sciences_Hackathon2_Task2"}
            ]
        },
        {
            "id":"sahibinden",
            "title":"🏠 Housing Market & Weather Dynamics in Istanbul",
            "title_tr":"🏠 Konut Piyasası ve Hava Durumu Iliskisi Analizi",
            "title_en":"🏠 Housing Market & Weather Dynamics in Istanbul",
            "thumb":"https://raw.githubusercontent.com/EdaCelikeloglu/streamlit_portfolyo/master/assets/sahibinden_kapak.png",
            "desc_tr":"İstanbul'daki konut piyasası dinamikleri ile hava durumu koşulları arasındaki ilişkiyi açık veri kaynaklarını entegre ederek analiz ettim. Open-Meteo API'si aracılığıyla gerçek zamanlı meteorolojik verileri topladım ve bu verileri satılık dairelerin görüntülenme ve aranma istatistikleriyle birleştirdim. Zaman serisi modellemesi kullanarak sıcaklık, yağış ve diğer hava değişkenlerinin kullanıcı etkileşim eğilimleri üzerindeki etkisini inceledim. Analizde dışsal hava faktörlerinin etkisini ölçmek için SARIMAX modelinden yararlandım ve elde ettiğim bulguları detaylı bir rapor ve görselleştirmeler eşliğinde sundum.",
            "desc_en":"I analyzed the relationship between housing market dynamics and weather conditions in Istanbul by integrating open data sources. Using the Open-Meteo API, I collected real-time meteorological data and combined it with digital metrics on the views and search volumes of apartments listed for sale. Through time series modeling, I examined how changes in temperature, precipitation, and other weather variables influenced user engagement trends. The analysis employed the SARIMAX model to capture the impact of exogenous weather factors, and I presented the key insights through a detailed report and visualization.",
            "links":[]
        },
        {
            "id":"powerbi",
            "title":"📊 Sales Analyses - Power BI Dashboard",
            "title_tr":"📊 Satış Analizleri - Power BI Dashboard",
            "title_en":"📊 Sales Analyses - Power BI Dashboard",
            "thumb":"https://raw.githubusercontent.com/EdaCelikeloglu/streamlit_portfolyo/master/assets/powerbi1.PNG",
            "desc_tr":"Bölgeler ve ürün kategorileri genelinde performans metriklerini görselleştiren etkileşimli bir Power BI dashboard'u.",
            "desc_en":"Interactive Power BI dashboard visualizing performance across regions and product categories.",
            "pdf_raw":"https://raw.githubusercontent.com/EdaCelikeloglu/streamlit_portfolyo/master/assets/Eda_Celikeloglu_Sales_Summaries.pdf",
            "powerbi_link":"https://app.powerbi.com/reportEmbed?reportId=d8b1f2ec-5c17-4864-a9d3-64f415eb5f6e&autoAuth=true&ctid=92e0b030-5e40-4cdd-8ff8-51fa8a4504e2",
            "links":[]
        }
    ]

    # ===== state =====
    if "active_modal" not in st.session_state:
        st.session_state["active_modal"] = None
    if "modal_timestamp" not in st.session_state:
        st.session_state["modal_timestamp"] = 0

    def open_modal(pid):
        import random
        st.session_state["active_modal"] = pid
        st.session_state["modal_id"] = f"{pid}_{random.randint(1000, 9999)}"
        st.rerun()

    # ===== grid =====
    r1c1, r1c2 = st.columns(2)
    for p, col in zip(projects[:2], [r1c1, r1c2]):
        with col:
            st.markdown(f"<div class='proj-card'><div class='proj-title'>{p['title_tr'] if t else p['title_en']}</div>", unsafe_allow_html=True)
            st.image(p["thumb"], use_container_width=True)
            if st.button(lbl_view_details, key=f"open_{p['id']}", use_container_width=True):
                open_modal(p["id"])
            st.markdown("</div>", unsafe_allow_html=True)

    r2c1, r2c2 = st.columns(2)
    for p, col in zip(projects[2:], [r2c1, r2c2]):
        with col:
            st.markdown(f"<div class='proj-card'><div class='proj-title'>{p['title_tr'] if t else p['title_en']}</div>", unsafe_allow_html=True)
            st.image(p["thumb"], use_container_width=True)
            if st.button(lbl_view_details, key=f"open_{p['id']}", use_container_width=True):
                open_modal(p["id"])
            st.markdown("</div>", unsafe_allow_html=True)

    # ===== modal (gerçek popup; parent DOM'a enjekte) =====
    if st.session_state.get("active_modal"):
        p = next(x for x in projects if x["id"] == st.session_state["active_modal"])
        modal_id = st.session_state.get("modal_id", "default")
        inject_modal_top(p, language, modal_id)


def inject_modal_top(p, language: str, modal_id: str):
    """Modalı Streamlit iframenin DIŞINA (parent DOM) ekler; tam ekran overlay + kapat."""
    title = p["title_tr"] if language == "Türkçe" else p["title_en"]
    desc  = p["desc_tr"] if language == "Türkçe" else p["desc_en"]

    # Linkler
    links_html = ""
    if p.get("pdf_raw"):
        links_html += f"<p><a href='{p['pdf_raw']}' target='_blank'>📄 PDF</a></p>"
    if p.get("powerbi_link"):
        links_html += f"<p><a href='{p['powerbi_link']}' target='_blank'>📊 Power BI</a></p>"
    if p.get("links"):
        for L in p["links"]:
            label = L["label_tr"] if language == "Türkçe" else L["label_en"]
            links_html += f"<p><a href='{L['href']}' target='_blank'>🔗 {label}</a></p>"

    # Video
    video_html = ""
    if p.get("video"):
        video_html = f"<div style='margin-top:12px'><iframe width='100%' height='400' src='{p['video'].replace('watch?v=', 'embed/')}' frameborder='0' allowfullscreen></iframe></div>"

    # Modal içerik + stil (parent DOM'a basılacak)
    content_html = f"""
    <style>
      #x-modal-overlay {{ position:fixed; inset:0; background:rgba(0,0,0,.6); z-index:2147483646; }}
      #x-modal-box {{
         position:fixed; top:50%; left:50%; transform:translate(-50%,-50%);
         background:#fff; width:min(900px,90vw); max-height:90vh; overflow:auto;
         border-radius:14px; padding:24px; box-shadow:0 10px 40px rgba(0,0,0,.45);
         z-index:2147483647; font-family: 'Poppins', sans-serif;
      }}
      #x-close {{ position:absolute; right:12px; top:12px; border:none; background:#FF4B4B; color:#fff;
                  border-radius:8px; padding:6px 10px; cursor:pointer; }}
      #x-modal-box h2 {{ margin:0 0 10px 0; }}
      #x-modal-links a {{ text-decoration:none; }}
    </style>
    <div id="x-modal-overlay"></div>
    <div id="x-modal-box">
        <button id="x-close">Kapat</button>
        <h2>{title}</h2>
        <p>{desc}</p>
        <div id="x-modal-links">{links_html}</div>
        {video_html}
    </div>
    """

    # JS ile parent'a ekle/çıkar
    payload = json.dumps(content_html)
    wrapper_id = f"x-modal-wrapper-{modal_id}"
    js = f"""
    <script>
      const doc = window.parent.document;

      // Eski modal varsa temizle
      const old = doc.getElementById('{wrapper_id}');
      if (old) old.remove();

      // Wrapper oluştur ve içeriği bas
      const wrapper = doc.createElement('div');
      wrapper.id = '{wrapper_id}';
      wrapper.innerHTML = {payload};
      doc.body.appendChild(wrapper);

      function closeModal() {{
        const w = doc.getElementById('{wrapper_id}');
        if (w) w.remove();
        // Streamlit'e modal kapatıldığını bildir
        window.parent.postMessage({{
          type: 'streamlit:setComponentValue',
          value: 'closed'
        }}, '*');
      }}

      doc.getElementById('x-close').addEventListener('click', closeModal);
      doc.getElementById('x-modal-overlay').addEventListener('click', closeModal);
      doc.addEventListener('keydown', (e) => {{ if (e.key === 'Escape') closeModal(); }});
    </script>
    """

    # 0 px yüksekliğe göm; görünür olan parent'a eklenen modal olur
    components.html(js, height=0, width=0)


def show_testimonials_section():
    st.markdown(f"## {content[language]['testimonials_title']}")
    
    # Referans verileri
    testimonials_data = {
        "Türkçe": [
            {
                "name": "Güray Ataman",
                "role": "Data Science Team Lead @ sahibinden.com",
                "date": "1 Haziran 2025",
                "text": """Eda Çelikeloğlu worked as a Junior Data Scientist in our team and consistently demonstrated a disciplined and methodical approach to her work. Her strong analytical thinking, determination, and eagerness to learn made a valuable contribution to our projects.

She particularly stood out for her coding skills and problem-solving abilities, delivering effective and results-oriented solutions. Eda was a reliable and collaborative team member who carried out her responsibilities with professionalism and care.

It was a pleasure to work with her. I am confident that she will continue to bring value to any team she joins, and I sincerely wish her continued success in her career.""",
                "linkedin_url": "https://www.linkedin.com/in/gurayataman/",
                "avatar": "https://ui-avatars.com/api/?name=Guray+Ataman&background=667eea&color=fff&size=200"
            },
            {
                "name": "Doğu Sırt",
                "role": "PhD Faculty Lecturer @ Istanbul Technical University, Python, Artificial Intelligence, Data Science, Big Data and Analytics",
                "date": "27 Mayıs 2025",
                "text": """I had the pleasure of teaching Eda during an intensive training program on data science and applied AI. From the very beginning, she stood out with her exceptional curiosity, quick learning abilities, and strong analytical thinking.

Eda consistently demonstrated her ability to turn theoretical knowledge into practical solutions with clarity and precision. Whether it was building machine learning models, analyzing complex datasets, or collaborating on team projects, she approached every challenge with professionalism, creativity, and dedication.

She is exactly the kind of talent that modern companies need—technically strong, eager to learn, and capable of delivering real impact. I highly recommend Eda for any role in data science, AI, or analytics-driven teams. She will be a valuable asset to any organization.""",
                "linkedin_url": "https://www.linkedin.com/in/dogusirt/",
                "avatar": "https://ui-avatars.com/api/?name=Dogu+Sirt&background=764ba2&color=fff&size=200"
            }
        ],
        "English": [
            {
                "name": "Güray Ataman",
                "role": "Data Science Team Lead @ sahibinden.com",
                "date": "June 1, 2025",
                "text": """Eda Çelikeloğlu worked as a Junior Data Scientist in our team and consistently demonstrated a disciplined and methodical approach to her work. Her strong analytical thinking, determination, and eagerness to learn made a valuable contribution to our projects.

She particularly stood out for her coding skills and problem-solving abilities, delivering effective and results-oriented solutions. Eda was a reliable and collaborative team member who carried out her responsibilities with professionalism and care.

It was a pleasure to work with her. I am confident that she will continue to bring value to any team she joins, and I sincerely wish her continued success in her career.""",
                "linkedin_url": "https://www.linkedin.com/in/gurayataman/",
                "avatar": "https://ui-avatars.com/api/?name=Guray+Ataman&background=667eea&color=fff&size=200"
            },
            {
                "name": "Doğu Sırt",
                "role": "PhD Faculty Lecturer @ Istanbul Technical University, Python, Artificial Intelligence, Data Science, Big Data and Analytics",
                "date": "May 27, 2025",
                "text": """I had the pleasure of teaching Eda during an intensive training program on data science and applied AI. From the very beginning, she stood out with her exceptional curiosity, quick learning abilities, and strong analytical thinking.

Eda consistently demonstrated her ability to turn theoretical knowledge into practical solutions with clarity and precision. Whether it was building machine learning models, analyzing complex datasets, or collaborating on team projects, she approached every challenge with professionalism, creativity, and dedication.

She is exactly the kind of talent that modern companies need—technically strong, eager to learn, and capable of delivering real impact. I highly recommend Eda for any role in data science, AI, or analytics-driven teams. She will be a valuable asset to any organization.""",
                "linkedin_url": "https://www.linkedin.com/in/dogusirt/",
                "avatar": "https://ui-avatars.com/api/?name=Dogu+Sirt&background=764ba2&color=fff&size=200"
            }
        ]
    }
    
    testimonials = testimonials_data[language]
    
    # İki referansı yan yana göster
    col1, col2 = st.columns(2)
    
    # Sol kolon - İlk referans (Güray Ataman)
    with col1:
        st.markdown(f"""
        <div class="contact-card" style="min-height: 600px;">
            <div style="text-align: center; margin-bottom: 1rem;">
                <img src="{testimonials[0]['avatar']}" 
                     style="width: 70px; height: 70px; border-radius: 50%; 
                            border: 3px solid white; box-shadow: 0 4px 12px rgba(0,0,0,0.2);">
            </div>
            <h3 style="color: white; text-align: center; margin-bottom: 0.5rem; font-size: 1.3rem;">{testimonials[0]['name']}</h3>
            <p style="color: rgba(255,255,255,0.9); text-align: center; font-size: 0.9rem; margin-bottom: 0.3rem;">
                {testimonials[0]['role']}
            </p>
            <p style="color: rgba(255,255,255,0.7); text-align: center; font-size: 0.8rem; margin-bottom: 1rem;">
                {testimonials[0]['date']}
            </p>
            <hr style="border-color: rgba(255,255,255,0.3); margin: 1rem 0;">
            <p style="color: rgba(255,255,255,0.95); line-height: 1.7; text-align: justify; font-size: 0.95rem;">
                {testimonials[0]['text']}
            </p>
            <div style="text-align: center; margin-top: 1.5rem;">
                <a href="{testimonials[0]['linkedin_url']}" target="_blank" 
                   style="display: inline-block !important; background: white !important; color: #667eea !important; 
                          padding: 0.6rem 1.3rem !important; border-radius: 25px !important; text-decoration: none !important; 
                          font-weight: 600 !important; font-size: 0.9rem !important; box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;">
                    🔗 {'LinkedIn Profilini Görüntüle' if language == 'Türkçe' else 'View LinkedIn Profile'}
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Sağ kolon - İkinci referans (Doğu Sırt)
    with col2:
        st.markdown(f"""
        <div class="contact-card" style="min-height: 600px; background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);">
            <div style="text-align: center; margin-bottom: 1rem;">
                <img src="{testimonials[1]['avatar']}" 
                     style="width: 70px; height: 70px; border-radius: 50%; 
                            border: 3px solid white; box-shadow: 0 4px 12px rgba(0,0,0,0.2);">
            </div>
            <h3 style="color: white; text-align: center; margin-bottom: 0.5rem; font-size: 1.3rem;">{testimonials[1]['name']}</h3>
            <p style="color: rgba(255,255,255,0.9); text-align: center; font-size: 0.9rem; margin-bottom: 0.3rem;">
                {testimonials[1]['role']}
            </p>
            <p style="color: rgba(255,255,255,0.7); text-align: center; font-size: 0.8rem; margin-bottom: 1rem;">
                {testimonials[1]['date']}
            </p>
            <hr style="border-color: rgba(255,255,255,0.3); margin: 1rem 0;">
            <p style="color: rgba(255,255,255,0.95); line-height: 1.7; text-align: justify; font-size: 0.95rem;">
                {testimonials[1]['text']}
            </p>
            <div style="text-align: center; margin-top: 1.5rem;">
                <a href="{testimonials[1]['linkedin_url']}" target="_blank" 
                   style="display: inline-block !important; background: white !important; color: #764ba2 !important; 
                          padding: 0.6rem 1.3rem !important; border-radius: 25px !important; text-decoration: none !important; 
                          font-weight: 600 !important; font-size: 0.9rem !important; box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;">
                    🔗 {'LinkedIn Profilini Görüntüle' if language == 'Türkçe' else 'View LinkedIn Profile'}
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # LinkedIn'e yönlendirme
    if language == "Türkçe":
        st.info("💡 Daha fazla referans ve detay için [LinkedIn profilimi](https://www.linkedin.com/in/eda-celikeloglu) ziyaret edebilirsiniz.")
    else:
        st.info("💡 For more recommendations and details, visit my [LinkedIn profile](https://www.linkedin.com/in/eda-celikeloglu).")


def show_contact_section():
    st.markdown(f"## {content[language]['contact_title']}")

    # İletişim bilgileri ve mesaj formu yan yana
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if language == "Türkçe":
            st.markdown("""
            <div class="contact-card">
                <h3 style="color:white; margin-bottom: 1rem;">İletişime Geçelim! 🚀</h3>
                <p style="opacity: 0.9;">Projeleriniz, veri bilimi üzerine fikir alışverişi veya iş birliği fırsatları için benimle iletişime geçebilirsiniz.</p>
                <p style="opacity: 0.9;">Aşağıdaki kanallardan ulaşabilirsiniz 👇</p>
                <br>
                <div style="display: flex; flex-direction: column; gap: 0.8rem;">
                    <div style="display: block; background: rgba(255,255,255,0.2); color: white; 
                              padding: 0.7rem 1.3rem; border-radius: 25px; 
                              font-weight: 600; font-size: 0.95rem; box-shadow: 0 4px 12px rgba(0,0,0,0.2);
                              text-align: center; border: none;">
                        📧 edacelikeloglu@gmail.com
                    </div>
                    <a href="https://www.linkedin.com/in/eda-celikeloglu" target="_blank" 
                       style="display: block !important; background: white !important; color: #667eea !important; 
                              padding: 0.7rem 1.3rem !important; border-radius: 25px !important; text-decoration: none !important; 
                              font-weight: 600 !important; font-size: 0.95rem !important; box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
                              text-align: center !important; border: none !important;">
                        💼 LinkedIn
                    </a>
                    <a href="https://github.com/EdaCelikeloglu" target="_blank" 
                       style="display: block !important; background: white !important; color: #667eea !important; 
                              padding: 0.7rem 1.3rem !important; border-radius: 25px !important; text-decoration: none !important; 
                              font-weight: 600 !important; font-size: 0.95rem !important; box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
                              text-align: center !important; border: none !important;">
                        🐱 GitHub
                    </a>
                    <a href="https://www.kaggle.com/edacelikeloglu" target="_blank" 
                       style="display: block !important; background: white !important; color: #667eea !important; 
                              padding: 0.7rem 1.3rem !important; border-radius: 25px !important; text-decoration: none !important; 
                              font-weight: 600 !important; font-size: 0.95rem !important; box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
                              text-align: center !important; border: none !important;">
                        🦆 Kaggle
                    </a>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="contact-card">
                <h3 style="color:white; margin-bottom: 1rem;">Let's Get in Touch! 🚀</h3>
                <p style="opacity: 0.9;">Feel free to reach out for projects, data science discussions, or collaboration opportunities.</p>
                <p style="opacity: 0.9;">You can contact me via the links below �</p>
                <br>
                <div style="display: flex; flex-direction: column; gap: 0.8rem;">
                    <div style="display: block; background: rgba(255,255,255,0.2); color: white; 
                              padding: 0.7rem 1.3rem; border-radius: 25px; 
                              font-weight: 600; font-size: 0.95rem; box-shadow: 0 4px 12px rgba(0,0,0,0.2);
                              text-align: center; border: none;">
                        📧 edacelikeloglu@gmail.com
                    </div>
                    <a href="https://www.linkedin.com/in/eda-celikeloglu" target="_blank" 
                       style="display: block !important; background: white !important; color: #667eea !important; 
                              padding: 0.7rem 1.3rem !important; border-radius: 25px !important; text-decoration: none !important; 
                              font-weight: 600 !important; font-size: 0.95rem !important; box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
                              text-align: center !important; border: none !important;">
                        💼 LinkedIn
                    </a>
                    <a href="https://github.com/EdaCelikeloglu" target="_blank" 
                       style="display: block !important; background: white !important; color: #667eea !important; 
                              padding: 0.7rem 1.3rem !important; border-radius: 25px !important; text-decoration: none !important; 
                              font-weight: 600 !important; font-size: 0.95rem !important; box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
                              text-align: center !important; border: none !important;">
                        🐱 GitHub
                    </a>
                    <a href="https://www.kaggle.com/edacelikeloglu" target="_blank" 
                       style="display: block !important; background: white !important; color: #667eea !important; 
                              padding: 0.7rem 1.3rem !important; border-radius: 25px !important; text-decoration: none !important; 
                              font-weight: 600 !important; font-size: 0.95rem !important; box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
                              text-align: center !important; border: none !important;">
                        🦆 Kaggle
                    </a>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        # Mesaj gönderme formu - inline CSS ile
        if language == "Türkçe":
            form_title = "💌 Ya da Mesaj Gönder"
            name_label = "İsminiz"
            email_label = "E-posta Adresiniz"
            message_label = "Mesajınız"
            submit_label = "📤 Gönder"
            success_msg = "Mesajınız başarıyla gönderildi! Teşekkür ederim 🙏"
            warning_msg = "Lütfen tüm alanları doldurun."
            subject_prefix = "Yeni mesaj:"
        else:
            form_title = "💌 Send a Message"
            name_label = "Your Name"
            email_label = "Your Email"
            message_label = "Message"
            submit_label = "📤 Send"
            success_msg = "Your message has been sent successfully! Thank you 🙏"
            warning_msg = "Please fill in all fields."
            subject_prefix = "New message:"
        
        with st.form("contact_form"):
            # Başlık - direkt HTML
            st.markdown(f"""
            <h3 style="color: white; text-align: center; margin-bottom: 1.5rem; margin-top: 0;">{form_title}</h3>
            """, unsafe_allow_html=True)
            name = st.text_input(name_label, key="name_input")
            email = st.text_input(email_label, key="email_input")
            message = st.text_area(message_label, height=150, key="message_input")

            submitted = st.form_submit_button(submit_label, use_container_width=True)

            if submitted:
                if name and email and message:
                    msg = MIMEMultipart()
                    msg["From"] = SENDER_EMAIL
                    msg["To"] = RECEIVER_EMAIL
                    msg["Subject"] = f"{subject_prefix} {name}"
                    msg["Reply-To"] = email
                    msg.attach(MIMEText(f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}", "plain"))

                    try:
                        server = smtplib.SMTP("smtp.gmail.com", 587)
                        server.starttls()
                        server.login(SENDER_EMAIL, EMAIL_PASSWORD)
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
elif selected_section == "testimonials":
    show_testimonials_section()
elif selected_section == "contact":
    show_contact_section()


# Footer
st.markdown(
    """
    <div style="position: fixed; bottom: 0; left: 0; width: 100%; 
                background: rgba(255, 255, 255, 0.95); 
                text-align: center; padding: 0.8rem 0; 
                color: #666; font-size: 0.9rem;
                border-top: 1px solid #eee;
                z-index: 999;
                backdrop-filter: blur(10px);">
        <p style="margin: 0;">© 2026 Eda Çelikeloğlu | Made with ❤️ and Streamlit</p>
    </div>
    """,
    unsafe_allow_html=True
)





