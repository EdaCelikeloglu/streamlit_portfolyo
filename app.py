import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
import streamlit.components.v1 as components
import json
import base64
import random


# .env dosyasını yükle
load_dotenv()

# Ortam değişkenlerinden değerleri al
SENDER_EMAIL = os.getenv("EMAIL_USER")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Sayfa konfigürasyonu
st.set_page_config(
    page_title="Eda Çelikeloğlu - Data Scientist & Mathematician",
    page_icon="assets/favicon.png",
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
        background: linear-gradient(180deg, #7b8ff5 0%, #8b5fb8 100%);
    }

    /* Ana içerik alanının üst boşluğunu azalt - daha güçlü seçiciler */
    div[data-testid="stAppViewContainer"] > section.main > div.block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
    }
    
    div[data-testid="stAppViewContainer"] > section.main {
        padding-top: 0rem !important;
    }
    
    .main > div {
        padding-top: 0rem !important;
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
        background-color: rgba(255, 255, 255, 0.05);
        padding: 0;
        border-radius: 10px;
        margin-top: -1rem;
    }
    
    /* Radio button labels - navigation items */
    [data-testid="stSidebar"] .stRadio label {
        background: transparent;
        padding: 0.1rem 0.8rem;
        border-radius: 0;
        margin: 0;
        transition: all 0.2s ease;
        cursor: pointer;
        border-left: 3px solid transparent;
    }
    
    [data-testid="stSidebar"] .stRadio label:first-child {
        border-top-left-radius: 10px;
        border-top-right-radius: 10px;
    }
    
    [data-testid="stSidebar"] .stRadio label:last-child {
        border-bottom-left-radius: 10px;
        border-bottom-right-radius: 10px;
    }
    
    [data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(102,126,234,0.15);
        border-left-color: #667eea;
    }
    
    /* Selected radio button */
    [data-testid="stSidebar"] .stRadio label[data-checked="true"] {
        background: linear-gradient(90deg, rgba(102,126,234,0.2) 0%, rgba(118,75,162,0.1) 100%);
        border-left-color: #667eea;
        border-left-width: 4px;
    }
    
    [data-testid="stSidebar"] .stRadio label[data-checked="true"] p {
        color: #667eea !important;
        font-weight: 600;
    }

    [data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.3) !important;
    }

    .hero-section {
        background: linear-gradient(135deg, #7b8ff5 0%, #8b5fb8 100%);
        padding: 2rem 2rem;
        border-radius: 25px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        margin-top: 0;
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
        background: linear-gradient(135deg, #7b8ff5 0%, #8b5fb8 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        box-shadow: 0 10px 30px rgba(102,126,234,0.4);
        margin-bottom: 2rem;
    }

    .contact-form-card {
        background: linear-gradient(135deg, #8b5fb8 0%, #7b8ff5 100%);
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
        border: 2px solid white !important;
        padding: 15px 35px !important;
        border-radius: 30px !important;
        font-weight: 700 !important;
        font-size: 1.15rem !important;
        box-shadow: 0 10px 30px rgba(102,126,234,0.5), 0 0 20px rgba(102,126,234,0.3) !important;
        transition: all 0.3s ease !important;
        font-family: 'Poppins', sans-serif !important;
        animation: pulse-glow 2s ease-in-out infinite !important;
    }

    @keyframes pulse-glow {
        0%, 100% {
            box-shadow: 0 10px 30px rgba(102,126,234,0.5), 0 0 20px rgba(102,126,234,0.3);
        }
        50% {
            box-shadow: 0 10px 30px rgba(102,126,234,0.7), 0 0 30px rgba(102,126,234,0.5);
        }
    }

    .stDownloadButton > button:hover {
        transform: translateY(-3px) scale(1.05) !important;
        box-shadow: 0 15px 40px rgba(102,126,234,0.7), 0 0 35px rgba(102,126,234,0.6) !important;
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%) !important;
        border-color: rgba(255,255,255,0.9) !important;
    }

    .stDownloadButton > button:active {
        transform: translateY(-1px) scale(1.02) !important;
        box-shadow: 0 8px 25px rgba(102,126,234,0.6) !important;
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



# Dil seçimi - Sağ üst köşe
col1, col2, col3 = st.columns([6, 1, 1])
with col3:
    def on_language_change():
        st.session_state.language = st.session_state.language_selector
    
    language_option = st.selectbox(
        "",
        ["TR", "EN"],
        index=0 if st.session_state.language == "Türkçe" else 1,
        key="language_selector",
        on_change=on_language_change,
        label_visibility="collapsed"
    )
    
    if language_option == "TR":
        st.session_state.language = "Türkçe"
    else:
        st.session_state.language = "English"

# Sekme anahtarlarını sabitle
sections = ["home", "skills", "awards", "projects", "testimonials", "certificates", "contact"]
# Çeviriler
section_labels = {
    "Türkçe": {
        "home": "🏠 Ana Sayfa",
        "about": "👨‍💼 Hakkımda",
        "skills": "🛠️ Yetenekler",
        "projects": "📊 Projeler",
        "awards": "🏆 Ödüller",
        "certificates": "📜 Sertifikalar",
        "testimonials": "💬 Referanslar",
        "contact": "📞 İletişim"
    },
    "English": {
        "home": "🏠 Home",
        "about": "👨‍💼 About",
        "skills": "🛠️ Skills",
        "projects": "📊 Projects",
        "awards": "🏆 Awards",
        "certificates": "📜 Certificates",
        "testimonials": "💬 Testimonials",
        "contact": "📞 Contact"
    }
}


# Sidebar tasarımı
with st.sidebar:
    # Logo en üstte
    st.markdown("""
    <div style="text-align: center; padding: 0.5rem 0 1rem 0;">
        <img src="data:image/png;base64,{}" style="width: 100px; height: 100px; border-radius: 50%; 
             box-shadow: 0 4px 15px rgba(255,255,255,0.3); border: 3px solid white;">
    </div>
    """.format(__import__('base64').b64encode(open("assets/favicon.png", "rb").read()).decode()), unsafe_allow_html=True)
    
    labels = [section_labels[st.session_state.language][s] for s in sections]
    current_label = section_labels[st.session_state.language][st.session_state.selected_section]

    def on_section_change():
        reverse_map = {v: k for k, v in section_labels[st.session_state.language].items()}
        st.session_state.selected_section = reverse_map[st.session_state.nav_selector]

    selected_label = st.radio(
        "",
        labels,
        index=labels.index(current_label),
        key="nav_selector",
        on_change=on_section_change
    )
    
    # CV İndirme Butonu
    st.markdown("<br>", unsafe_allow_html=True)
    try:
        with open("assets/Eda_Celikeloglu_CV.pdf", "rb") as pdf_file:
            pdf_data = pdf_file.read()
        
        cv_label = "📄 CV'mi İndir" if st.session_state.language == 'Türkçe' else "📄 Download My CV"
        st.download_button(
            label=cv_label,
            data=pdf_data,
            file_name="Eda_Celikeloglu_CV.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    except FileNotFoundError:
        pass
    
    # Hareketli İstatistik Baloncukları
    bubble_data = {
        "Türkçe": [
            {"number": "2", "label": "Ödül"},
            {"number": "8+", "label": "Proje"},
            {"number": "10+", "label": "Teknoloji"}
        ],
        "English": [
            {"number": "2", "label": "Awards"},
            {"number": "8+", "label": "Projects"},
            {"number": "10+", "label": "Technologies"}
        ]
    }
    
    bubbles = bubble_data[st.session_state.language]
    
    st.markdown(f"""
    <style>
    .bubble-container {{
        position: relative;
        height: 450px;
        overflow: hidden;
        pointer-events: none;
        margin: 1rem 0;
    }}
    .bubble {{
        position: absolute;
        bottom: 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 50px;
        padding: 1rem 1.5rem;
        font-size: 1rem;
        font-weight: 700;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        animation: float-up 12s infinite ease-in-out;
        opacity: 0;
        white-space: nowrap;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
    }}
    .bubble-number {{
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }}
    .bubble-label {{
        font-size: 0.95rem;
        font-weight: 500;
    }}
    .bubble:nth-child(1) {{
        left: 5%;
        animation-delay: 0s;
        animation-duration: 18s;
    }}
    .bubble:nth-child(2) {{
        left: 55%;
        animation-delay: 5s;
        animation-duration: 18s;
    }}
    .bubble:nth-child(3) {{
        left: 25%;
        animation-delay: 10s;
        animation-duration: 18s;
    }}
    @keyframes float-up {{
        0% {{
            bottom: 0;
            opacity: 0;
            transform: translateX(0) scale(0.8);
        }}
        15% {{
            opacity: 1;
        }}
        75% {{
            opacity: 1;
        }}
        100% {{
            bottom: 370px;
            opacity: 0;
            transform: translateX(20px) scale(1);
        }}
    }}
    
    /* Mobil responsive tasarım */
    @media (max-width: 768px) {{
        /* Column'ları mobilde alt alta diz */
        [data-testid="column"] {{
            width: 100% !important;
            flex: 0 0 100% !important;
            max-width: 100% !important;
            padding: 0 0.5rem !important;
            margin-bottom: 1rem !important;
        }}
        
        /* Hero section mobil düzeni */
        .hero-section {{
            flex-direction: column !important;
            padding: 1.5rem 1rem !important;
            text-align: center !important;
        }}
        
        .hero-section > div:first-child {{
            text-align: center !important;
            margin-bottom: 1.5rem !important;
        }}
        
        .hero-section > div:last-child {{
            margin-left: 0 !important;
            margin-bottom: 1rem !important;
        }}
        
        .hero-section img {{
            width: 180px !important;
            height: 180px !important;
        }}
        
        .hero-section h1 {{
            font-size: 1.8rem !important;
            text-align: center !important;
        }}
        
        .hero-section h2 {{
            font-size: 1.2rem !important;
            text-align: center !important;
        }}
        
        .hero-section p {{
            text-align: center !important;
            font-size: 0.95rem !important;
        }}
        
        .hero-title {{
            text-align: center !important;
        }}
        
        .hero-subtitle {{
            text-align: center !important;
        }}
        
        .typing-text {{
            text-align: center !important;
        }}
        
        .contact-card {{
            height: auto !important;
            min-height: auto !important;
            padding: 1.5rem !important;
            margin-bottom: 1rem !important;
            overflow: hidden !important;
            word-wrap: break-word !important;
        }}
        
        .contact-card p {{
            font-size: 0.9rem !important;
            line-height: 1.6 !important;
            word-wrap: break-word !important;
            overflow-wrap: break-word !important;
        }}
        
        .contact-card h3 {{
            font-size: 1.1rem !important;
            word-wrap: break-word !important;
        }}
        
        .contact-card img {{
            width: 60px !important;
            height: 60px !important;
        }}
        
        [data-testid="stForm"] {{
            height: auto !important;
            padding: 1.5rem !important;
        }}
    }}
    </style>
    <div class="bubble-container">
        <div class="bubble">
            <div class="bubble-number">{bubbles[0]['number']}</div>
            <div class="bubble-label">{bubbles[0]['label']}</div>
        </div>
        <div class="bubble">
            <div class="bubble-number">{bubbles[1]['number']}</div>
            <div class="bubble-label">{bubbles[1]['label']}</div>
        </div>
        <div class="bubble">
            <div class="bubble-number">{bubbles[2]['number']}</div>
            <div class="bubble-label">{bubbles[2]['label']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Kısa değişkenler
language = st.session_state.language
selected_section = st.session_state.selected_section


# İçerik sözlüğü
content = {
    "Türkçe": {
        "hero_title": "Eda Çelikeloğlu",
        "hero_subtitle": "Veri Bilimci | Veri Analisti | Matematikçi",
        "typing_text": "Verilerle hikayeler anlatıyorum...",
        "about_text": """
        <div style="
            color:#2b2b2b !important;
            line-height:1.85;
            font-size:1.05rem;
            text-align:justify;
            font-family:'Poppins', sans-serif;
        ">
            <p>
                Matematik altyapısına sahip bir veri analizi ve veri bilimi profesyoneliyim. Altı yıllık matematik öğretmenliği deneyimimin ardından veri ve teknolojiye olan ilgimi kariyerime taşıyarak bu alana geçiş yaptım. Gerçek problemler üzerinde çalışarak analitik düşünme gücümü veri odaklı karar üretme becerisiyle birleştirdim. Karmaşık veri yapılarını anlaşılır, ölçülebilir ve uygulanabilir çıktılara dönüştürmek temel motivasyonumu oluşturuyor.
            </p>

            <p>
                Sahibinden.com'da Junior Data Scientist olarak gerçekleştirdiğim staj süresince dijital etkileşim metrikleri ile dışsal değişkenler arasındaki ilişkileri analiz ettim ve zaman serisi yaklaşımlarıyla tahminleme çalışmaları yürüttüm. Veriyi yalnızca incelemekle kalmayıp, sonuçları iş birimleri için anlamlı içgörülere dönüştürmeye odaklandım. YenidenBiz Derneği'nde gönüllü veri analisti olarak, kadınların iş gücüne katılımını destekleyen projelerde veri analizi ve raporlama çalışmalarına katkı sunuyorum.
            </p>

            <p><strong>🎓 Eğitim:</strong> Marmara Üniversitesi, Matematik Bölümü, 2010-2014</p>

            <p><strong>💼 Deneyim:</strong></p>
            <ul style="margin-top:0.4rem; padding-left:1.4rem;">
                <li>Sahibinden.com, Junior Data Scientist, 2025</li>
                <li>YenidenBiz Derneği, Gönüllü Veri Analisti, 2025-Halen</li>
            </ul>

            <p><strong>📍 Konum:</strong> Maltepe, İstanbul</p>
        </div>
        """
    },
    "English": {
        "hero_title": "Eda Çelikeloğlu",
        "hero_subtitle": "Data Scientist | Data Analyst | Mathematician",
        "typing_text": "I tell stories with data...",
        "about_text": """
        <div style="
            color:#2b2b2b !important;
            line-height:1.85;
            font-size:1.05rem;
            text-align:justify;
            font-family:'Poppins', sans-serif;
        ">
            <p>
                I am a data analytics and data science professional with a strong academic background in mathematics. After six years of experience as a mathematics teacher, I transitioned my career toward data and technology, where I have been applying my analytical mindset to real world problems and data driven decision making. I am motivated by turning complex datasets into clear, measurable, and applicable outcomes that create real impact.
            </p>

            <p>
                During my internship at Sahibinden.com as a Junior Data Scientist, I analyzed the relationship between digital engagement metrics and external variables, conducting forecasting studies using time series approaches. I focused not only on analyzing the data but also on transforming results into actionable insights for business stakeholders. As a Volunteer Data Analyst at YenidenBiz Association, I contribute to projects that support women returning to the workforce by providing data analysis and reporting that enable evidence based program evaluation.
            </p>

            <p><strong>🎓 Education:</strong> Marmara University, BSc in Mathematics, 2010-2014</p>

            <p><strong>💼 Experience:</strong></p>
            <ul style="margin-top:0.4rem; padding-left:1.4rem;">
                <li>Sahibinden.com, Junior Data Scientist, 2025</li>
                <li>YenidenBiz Association, Volunteer Data Analyst, 2025-Present</li>
            </ul>

            <p><strong>📍 Location:</strong> Maltepe, Istanbul</p>
        </div>
        """
    }
}


# Ana içerik
def show_hero_section():
    
    with open("assets/profile_picture.jpg", "rb") as img_file:
        img_data = base64.b64encode(img_file.read()).decode()
    
    st.markdown(f"""
        <div class="hero-section" style="display: flex; align-items: center; justify-content: space-between; padding: 2rem 4rem; margin-top: 0;">
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
    
    # Hakkımda bölümünü ekle
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(content[language]["about_text"], unsafe_allow_html=True)
    



def show_skills_section():
    skills_data = {
        "Türkçe": {
            "Programlama": ["Python", "SQL"],
            "Veri Bilimi": ["Pandas", "NumPy", "Scikit-learn", "XGBoost", "LightGBM", "TensorFlow", "Keras", "xarray"],
            "Görselleştirme": ["Matplotlib", "Seaborn", "Plotly", "Power BI", "Tableau", "Streamlit"],
            "Analiz": ["EDA", "Feature Engineering", "Time Series", "SARIMAX", "Regression", "Classification", "KNN"],
            "Araçlar": ["Jupyter", "PyCharm", "VS Code", "GitHub", "Excel", "Apify"]
        },
        "English": {
            "Programming": ["Python", "SQL"],
            "Data Science": ["Pandas", "NumPy", "Scikit-learn", "XGBoost", "LightGBM", "TensorFlow", "Keras", "xarray"],
            "Visualization": ["Matplotlib", "Seaborn", "Plotly", "Power BI", "Tableau", "Streamlit"],
            "Analysis": ["EDA", "Feature Engineering", "Time Series", "SARIMAX", "Regression", "Classification", "KNN"],
            "Tools": ["Jupyter", "PyCharm", "VS Code", "GitHub", "Excel", "Apify"]
        }
    }
    
    # CSS stilleri
    st.markdown("""
    <style>
    .skill-card-compact {
        background: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(255,255,255,0.95) 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(102,126,234,0.15);
        transition: all 0.3s ease;
        border: 2px solid transparent;
        height: 100%;
        min-height: 200px;
        display: flex;
        flex-direction: column;
    }
    .skill-card-compact:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(102,126,234,0.25);
        border-color: rgba(102,126,234,0.4);
    }
    .skill-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #667eea;
        margin-bottom: 1rem;
        text-align: center;
    }
    .skill-tags-container {
        text-align: center;
        flex-grow: 1;
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        align-content: flex-start;
    }
    .skill-tag-compact {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.4rem 0.9rem;
        border-radius: 15px;
        margin: 0.3rem;
        font-size: 0.85rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    .skill-tag-compact:hover {
        transform: scale(1.08);
        box-shadow: 0 3px 12px rgba(102,126,234,0.4);
    }
    </style>
    """, unsafe_allow_html=True)

    categories = list(skills_data[language].items())
    
    # İlk satır: 3 sütun
    col1, col2, col3 = st.columns(3)
    
    with col1:
        category, skills = categories[0]
        skills_html = "".join([f"<span class='skill-tag-compact'>{skill}</span>" for skill in skills])
        st.markdown(f"""
        <div class="skill-card-compact">
            <div class="skill-title">{category}</div>
            <div class="skill-tags-container">{skills_html}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        category, skills = categories[1]
        skills_html = "".join([f"<span class='skill-tag-compact'>{skill}</span>" for skill in skills])
        st.markdown(f"""
        <div class="skill-card-compact">
            <div class="skill-title">{category}</div>
            <div class="skill-tags-container">{skills_html}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        category, skills = categories[2]
        skills_html = "".join([f"<span class='skill-tag-compact'>{skill}</span>" for skill in skills])
        st.markdown(f"""
        <div class="skill-card-compact">
            <div class="skill-title">{category}</div>
            <div class="skill-tags-container">{skills_html}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # İkinci satır: 3 sütun (ilk 2 dolu, son boş)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        category, skills = categories[3]
        skills_html = "".join([f"<span class='skill-tag-compact'>{skill}</span>" for skill in skills])
        st.markdown(f"""
        <div class="skill-card-compact">
            <div class="skill-title">{category}</div>
            <div class="skill-tags-container">{skills_html}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        category, skills = categories[4]
        skills_html = "".join([f"<span class='skill-tag-compact'>{skill}</span>" for skill in skills])
        st.markdown(f"""
        <div class="skill-card-compact">
            <div class="skill-title">{category}</div>
            <div class="skill-tags-container">{skills_html}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.empty()
    
    st.markdown('</div>', unsafe_allow_html=True)



# ===== Projeler (Global) =====
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
        "id":"churninator",
        "title":"💳 Churninator - Müşteri Kaybı Tahmini",
        "title_tr":"💳 Churninator - Müşteri Kaybı Tahmini",
        "title_en":"💳 Churninator - Customer Churn Prediction",
        "thumb":"https://raw.githubusercontent.com/EdaCelikeloglu/streamlit_portfolyo/master/assets/Churninator_kapak.png",
        "desc_tr":"İstanbul Kodluyor Projesi kapsamında Churninator adlı bir Veri Bilimi bitirme projesi geliştirdim. Projenin temel amacı, kredi kartı müşterilerinin bankadan ayrılma olasılıklarını gelişmiş veri analizi yöntemleriyle tahmin etmek. Uyguladığım model %92 recall oranına ulaşarak yüksek bir başarı sergiledi. Tamamen Python diliyle geliştirdiğim bu yazılım; veri setleri, yapılandırma dosyaları ve analiz kodlarını içeren kapsamlı bir yapıdan oluşuyor. Proje, finansal hizmetler alanında müşteri kaybını önlemek isteyen profesyonellere yönelik teknik bir çözüm sunuyor.",
        "desc_en":"I developed a Data Science capstone project called Churninator as part of the Istanbul Kodluyor Project. The main goal of the project is to predict the likelihood of credit card customers leaving the bank using advanced data analysis methods. The model I implemented achieved a high success rate with 92% recall. This software, developed entirely in Python, consists of a comprehensive structure including datasets, configuration files, and analysis codes. The project offers a technical solution for professionals in the financial services sector who want to prevent customer churn.",
        "pdf_raw":"https://raw.githubusercontent.com/EdaCelikeloglu/streamlit_portfolyo/master/assets/Churninator.pdf",
        "links":[
            {"label_tr":"GitHub","label_en":"GitHub","href":"https://github.com/EdaCelikeloglu/Churninator"}
        ]
    },
    {
        "id":"nasa_plotly",
        "title":"🌌 NASA Uzay Hava Verileri - Plotly Görselleştirme",
        "title_tr":"🌌 NASA Uzay Hava Verileri - Plotly Görselleştirme",
        "title_en":"🌌 NASA Space Weather Data - Plotly Visualization",
        "thumb":"https://raw.githubusercontent.com/EdaCelikeloglu/streamlit_portfolyo/master/assets/nasa_kapak_1.png",
        "desc_tr":"Bu projede NASA tarafından paylaşılan uzay hava olaylarını Kaggle üzerinde düzenleyerek kullanılabilir bir veri seti haline getirdim ve bu verilerle Plotly kullanarak interaktif görselleştirmeler oluşturdum. Amacım, farklı uzay hava olaylarının zaman içindeki değişimini incelemek ve kullanıcıya veriyi etkileşimli biçimde keşfetme imkanı sunmaktı. Çalışma boyunca zaman serileri, olay türlerine göre yoğunluklar ve tarih bazlı dağılımlar üzerine odaklandım. Böylece karmaşık ve teknik görünen bir veri yapısını daha okunabilir, karşılaştırılabilir ve analiz edilebilir bir hale dönüştürdüm.",
        "desc_en":"In this project, I organized space weather events shared by NASA on Kaggle into a usable dataset and created interactive visualizations using Plotly. My goal was to examine the changes in different space weather events over time and provide users with the opportunity to explore the data interactively. Throughout the work, I focused on time series, event type densities, and date-based distributions. Thus, I transformed a complex and technical-looking data structure into a more readable, comparable, and analyzable format.",
        "links":[
            {"label_tr":"Kaggle Notebook","label_en":"Kaggle Notebook","href":"https://www.kaggle.com/code/edacelikeloglu/plotly-examples-with-nasa-space-weather-data"}
        ]
    },
    {
        "id":"physical_therapy",
        "title":" 🏥 Fizik Tedavi Veri Analizi",
        "title_tr":" 🏥 Fizik Tedavi Veri Analizi",
        "title_en":" 🏥 Physical Therapy Data Analysis",
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
            "desc_tr": """Gradient Zero ve Viyana Üniversitesi iş birliğiyle düzenlenen bir yarışmada Taikai platformu üzerinden takım projesine katkıda bulundum ve takımımızla birlikte 3. olduk.
Yeraltı su seviyesi tahmini: 1930-2021 verileri ve dışsal değişkenlerle 2022-2024 tahminleri; SMAPE ile değerlendirildi.
GRACE serileri için dışsal değişkenler (hava, yağış, kar erimesi, yüzey sıcaklığı) belirlendi.
Python (TensorFlow, Keras, scikit-learn, xarray) ile modelleme yapıldı; sunum videosu ve kaynak kod sağlandı.""",
            "desc_en": """I participated in a competition organized by Gradient Zero with the University of Vienna on Taikai and achieved 3rd place with my team.
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

def show_projects_section():
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

    # ===== state =====
    if "active_modal" not in st.session_state:
        st.session_state["active_modal"] = None
    if "modal_timestamp" not in st.session_state:
        st.session_state["modal_timestamp"] = 0

    def open_modal(pid):
        
        st.session_state["active_modal"] = pid
        st.session_state["modal_id"] = f"{pid}_{random.randint(1000, 9999)}"
        st.rerun()

    # ===== grid =====
    # Ödül projelerini hariç tut
    filtered_projects = [p for p in projects if p["id"] not in ["datathon", "life_sci"]]
    
    # Projeleri 2'şer 2'şer satırlara böl
    cols_per_row = 2
    for i in range(0, len(filtered_projects), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            if i + j < len(filtered_projects):
                p = filtered_projects[i + j]
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


def show_awards_section():
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
    
    # Sadece ödül projelerini göster
    award_projects = [p for p in projects if p["id"] in ["datathon", "life_sci"]]
    
    def open_modal(pid):
        
        st.session_state["active_modal"] = pid
        st.session_state["modal_id"] = f"{pid}_{random.randint(1000, 9999)}"
        st.rerun()
    
    # Grid layout
    cols_per_row = 2
    for i in range(0, len(award_projects), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            if i + j < len(award_projects):
                p = award_projects[i + j]
                with col:
                    st.markdown(f"<div class='proj-card'><div class='proj-title'>{p['title_tr'] if t else p['title_en']}</div>", unsafe_allow_html=True)
                    st.image(p["thumb"], use_container_width=True)
                    if st.button(lbl_view_details, key=f"award_open_{p['id']}", use_container_width=True):
                        open_modal(p["id"])
                    st.markdown("</div>", unsafe_allow_html=True)
    
    # Modal
    if st.session_state.get("active_modal"):
        p = next((x for x in projects if x["id"] == st.session_state["active_modal"]), None)
        if p:
            modal_id = st.session_state.get("modal_id", "default")
            inject_modal_top(p, language, modal_id)


def show_testimonials_section():
    # Referans verileri
    testimonials_data = {
        "Türkçe": [
            {
                "name": "Güray Ataman",
                "role": "Data Science Team Lead<br>@ sahibinden.com",
                "date": "1 Haziran 2025",
                "text": """Eda Çelikeloğlu worked as a Junior Data Scientist in our team and consistently demonstrated a disciplined and methodical approach to her work. Her strong analytical thinking, determination, and eagerness to learn made a valuable contribution to our projects.

She particularly stood out for her coding skills and problem-solving abilities, delivering effective and results-oriented solutions. Eda was a reliable and collaborative team member who carried out her responsibilities with professionalism and care.

It was a pleasure to work with her. I am confident that she will continue to bring value to any team she joins, and I sincerely wish her continued success in her career.<br><br><br><br><br><br><br>""",
                "linkedin_url": "https://www.linkedin.com/in/gurayataman/",
                "avatar": "https://ui-avatars.com/api/?name=Guray+Ataman&background=667eea&color=fff&size=200"
            },
            {
                "name": "Doğu Sırt",
                "role": "PhD Faculty Lecturer @ Istanbul Technical University<br>Python, AI, Data Science, Big Data and Analytics",
                "date": "27 Mayıs 2025",
                "text": """I had the pleasure of teaching Eda during an intensive training program on data science and applied AI. From the very beginning, she stood out with her exceptional curiosity, quick learning abilities, and strong analytical thinking.

Eda consistently demonstrated her ability to turn theoretical knowledge into practical solutions with clarity and precision. Whether it was building machine learning models, analyzing complex datasets, or collaborating on team projects, she approached every challenge with professionalism, creativity, and dedication.

She is exactly the kind of talent that modern companies need—technically strong, eager to learn, and capable of delivering real impact. I highly recommend Eda for any role in data science, AI, or analytics-driven teams. She will be a valuable asset to any organization.<br><br><br><br>""",
                "linkedin_url": "https://www.linkedin.com/in/dogusirt/",
                "avatar": "https://ui-avatars.com/api/?name=Dogu+Sirt&background=764ba2&color=fff&size=200"
            },
            {
                "name": "Eda Başkan",
                "role": "Business Development and Resource Management Director<br>@ YenidenBiz Association",
                "date": "23 Şubat 2026",
                "text": """I have had the pleasure of working with Eda Çelikeloglu through our data driven initiatives at the YenidenBiz Association. Eda quickly adapted to our data analysis processes and consistently added value with her strong analytical thinking and solution oriented mindset.

As a Volunteer Data Analyst, she actively contributed to projects supporting women's return to the workforce, delivering meaningful insights from data. She also played an important role in the migration of our database infrastructure to the Google Apps environment, demonstrating strong ownership, technical curiosity, and a proactive approach.

Eda's solid mathematical background enables her to contribute effectively to data driven decision making. She is also a collaborative team player, eager to learn, and highly responsible in her work.

I strongly believe Eda will create significant value in data analytics and data science roles.""",
                "linkedin_url": "https://www.linkedin.com/in/edabaskan/",
                "avatar": "https://ui-avatars.com/api/?name=Eda+Baskan&background=8b5fb8&color=fff&size=200"
            }
        ],
        "English": [
            {
                "name": "Güray Ataman",
                "role": "Data Science Team Lead<br>@ sahibinden.com",
                "date": "June 1, 2025",
                "text": """Eda Çelikeloğlu worked as a Junior Data Scientist in our team and consistently demonstrated a disciplined and methodical approach to her work. Her strong analytical thinking, determination, and eagerness to learn made a valuable contribution to our projects.

She particularly stood out for her coding skills and problem-solving abilities, delivering effective and results-oriented solutions. Eda was a reliable and collaborative team member who carried out her responsibilities with professionalism and care.

It was a pleasure to work with her. I am confident that she will continue to bring value to any team she joins, and I sincerely wish her continued success in her career.<br><br><br><br><br><br><br>""",
                "linkedin_url": "https://www.linkedin.com/in/gurayataman/",
                "avatar": "https://ui-avatars.com/api/?name=Guray+Ataman&background=667eea&color=fff&size=200"
            },
            {
                "name": "Doğu Sırt",
                "role": "PhD Faculty Lecturer @ Istanbul Technical University<br>Python, AI, Data Science, Big Data and Analytics",
                "date": "May 27, 2025",
                "text": """I had the pleasure of teaching Eda during an intensive training program on data science and applied AI. From the very beginning, she stood out with her exceptional curiosity, quick learning abilities, and strong analytical thinking.

Eda consistently demonstrated her ability to turn theoretical knowledge into practical solutions with clarity and precision. Whether it was building machine learning models, analyzing complex datasets, or collaborating on team projects, she approached every challenge with professionalism, creativity, and dedication.

She is exactly the kind of talent that modern companies need—technically strong, eager to learn, and capable of delivering real impact. I highly recommend Eda for any role in data science, AI, or analytics-driven teams. She will be a valuable asset to any organization.<br><br><br><br>""",
                "linkedin_url": "https://www.linkedin.com/in/dogusirt/",
                "avatar": "https://ui-avatars.com/api/?name=Dogu+Sirt&background=764ba2&color=fff&size=200"
            },
            {
                "name": "Eda Başkan",
                "role": "Business Development and Resource Management Director<br>@ YenidenBiz Association",
                "date": "Feb 23, 2026",
                "text": """I have had the pleasure of working with Eda Çelikeloglu through our data driven initiatives at the YenidenBiz Association. Eda quickly adapted to our data analysis processes and consistently added value with her strong analytical thinking and solution oriented mindset.

As a Volunteer Data Analyst, she actively contributed to projects supporting women's return to the workforce, delivering meaningful insights from data. She also played an important role in the migration of our database infrastructure to the Google Apps environment, demonstrating strong ownership, technical curiosity, and a proactive approach.

Eda's solid mathematical background enables her to contribute effectively to data driven decision making. She is also a collaborative team player, eager to learn, and highly responsible in her work.

I strongly believe Eda will create significant value in data analytics and data science roles.""",
                "linkedin_url": "https://www.linkedin.com/in/edabaskan/",
                "avatar": "https://ui-avatars.com/api/?name=Eda+Baskan&background=8b5fb8&color=fff&size=200"
            }
        ]
    }
    
    testimonials = testimonials_data[language]
    
    # Üç referansı yan yana göster
    col1, col2, col3 = st.columns(3)
    
    # Sol kolon - İlk referans (Güray Ataman)
    with col1:
        st.markdown(f"""
        <div class="contact-card" style="height: 1100px; display: flex; flex-direction: column;">
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
            <div style="flex-grow: 1;">
                <p style="color: rgba(255,255,255,0.95); line-height: 1.7; text-align: justify; font-size: 0.95rem;">
                    {testimonials[0]['text']}
                </p>
            </div>
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
    
    # Orta kolon - İkinci referans (Doğu Sırt)
    with col2:
        st.markdown(f"""
        <div class="contact-card" style="height: 1100px; background: linear-gradient(135deg, #8b5fb8 0%, #7b8ff5 100%); display: flex; flex-direction: column;">
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
            <div style="flex-grow: 1;">
                <p style="color: rgba(255,255,255,0.95); line-height: 1.7; text-align: justify; font-size: 0.95rem;">
                    {testimonials[1]['text']}
                </p>
            </div>
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
    
    # Sağ kolon - Üçüncü referans (Eda Başkan)
    with col3:
        st.markdown(f"""
        <div class="contact-card" style="height: 1100px; display: flex; flex-direction: column;">
            <div style="text-align: center; margin-bottom: 1rem;">
                <img src="{testimonials[2]['avatar']}" 
                     style="width: 70px; height: 70px; border-radius: 50%; 
                            border: 3px solid white; box-shadow: 0 4px 12px rgba(0,0,0,0.2);">
            </div>
            <h3 style="color: white; text-align: center; margin-bottom: 0.5rem; font-size: 1.3rem;">{testimonials[2]['name']}</h3>
            <p style="color: rgba(255,255,255,0.9); text-align: center; font-size: 0.9rem; margin-bottom: 0.3rem;">
                {testimonials[2]['role']}
            </p>
            <p style="color: rgba(255,255,255,0.7); text-align: center; font-size: 0.8rem; margin-bottom: 1rem;">
                {testimonials[2]['date']}
            </p>
            <hr style="border-color: rgba(255,255,255,0.3); margin: 1rem 0;">
            <div style="flex-grow: 1;">
                <p style="color: rgba(255,255,255,0.95); line-height: 1.7; text-align: justify; font-size: 0.95rem;">
                    {testimonials[2]['text']}
                </p>
            </div>
            <div style="text-align: center; margin-top: 1.5rem;">
                <a href="{testimonials[2]['linkedin_url']}" target="_blank" 
                   style="display: inline-block !important; background: white !important; color: #8b5fb8 !important; 
                          padding: 0.6rem 1.3rem !important; border-radius: 25px !important; text-decoration: none !important; 
                          font-weight: 600 !important; font-size: 0.9rem !important; box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;">
                    🔗 {'LinkedIn Profilini Görüntüle' if language == 'Türkçe' else 'View LinkedIn Profile'}
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)


def open_certificate_modal(cert, modal_id):
    file_path = cert["file"]
    thumb_path = cert.get("thumb")

    if not os.path.exists(file_path):
        st.error("Dosya bulunamadı." if language == "Türkçe" else "File not found.")
        return

    ext = os.path.splitext(file_path)[1].lower()

    if ext in [".jpg", ".jpeg", ".png", ".webp"]:
        mime_type = "image/jpeg" if ext in [".jpg", ".jpeg"] else f"image/{ext.replace('.', '')}"
        with open(file_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        content_html = f"""
        <div style="text-align:center;">
            <img src="data:{mime_type};base64,{encoded}" style="max-width:100%; max-height:75vh; border-radius:12px; box-shadow:0 10px 30px rgba(0,0,0,0.25);">
        </div>
        """
    elif ext == ".pdf":
        if thumb_path and os.path.exists(thumb_path):
            with open(thumb_path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode()
            content_html = f"""
            <div style="text-align:center;">
                <img src="data:image/png;base64,{encoded}" style="max-width:100%; max-height:75vh; border-radius:12px; box-shadow:0 10px 30px rgba(0,0,0,0.25);">
            </div>
            """
        else:
            st.error("Önizleme görseli bulunamadı." if language == "Türkçe" else "Preview image not found.")
            return
    else:
        st.error("Desteklenmeyen dosya türü." if language == "Türkçe" else "Unsupported file type.")
        return

    title = cert["name"]

    modal_html = f"""
    <style>
      #cert-modal-overlay {{
        position: fixed;
        inset: 0;
        background: rgba(0,0,0,0.65);
        z-index: 2147483646;
      }}
      #cert-modal-box {{
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: white;
        width: min(1100px, 92vw);
        max-height: 92vh;
        overflow: auto;
        border-radius: 18px;
        padding: 24px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.35);
        z-index: 2147483647;
        font-family: 'Poppins', sans-serif;
      }}
      #cert-close-btn {{
        position: absolute;
        right: 16px;
        top: 16px;
        border: none;
        background: #FF4B4B;
        color: white;
        border-radius: 10px;
        padding: 8px 12px;
        cursor: pointer;
        font-weight: 600;
      }}
      #cert-modal-title {{
        margin: 0 0 18px 0;
        color: #4B0082;
        font-size: 1.4rem;
        font-weight: 600;
        padding-right: 70px;
      }}
    </style>
    <div id="cert-modal-overlay"></div>
    <div id="cert-modal-box">
        <button id="cert-close-btn">Kapat</button>
        <h2 id="cert-modal-title">{title}</h2>
        {content_html}
    </div>
    """

    payload = json.dumps(modal_html)
    wrapper_id = f"cert-modal-wrapper-{modal_id}"

    js = f"""
    <script>
      const doc = window.parent.document;

      const old = doc.getElementById('{wrapper_id}');
      if (old) old.remove();

      const wrapper = doc.createElement('div');
      wrapper.id = '{wrapper_id}';
      wrapper.innerHTML = {payload};
      doc.body.appendChild(wrapper);

      function closeModal() {{
        const w = doc.getElementById('{wrapper_id}');
        if (w) w.remove();
      }}

      doc.getElementById('cert-close-btn').addEventListener('click', closeModal);
      doc.getElementById('cert-modal-overlay').addEventListener('click', closeModal);
      doc.addEventListener('keydown', (e) => {{
        if (e.key === 'Escape') closeModal();
      }});
    </script>
    """

    components.html(js, height=0, width=0)


def show_certificates_section():
    certificates_data = {
        "Türkçe": {
            "categories": {
                "Öne Çıkanlar": [
                    {
                        "name": "Veri Bilimi, İstanbul Kodluyor",
                        "file": "assets/sertifikalar/featured-certificates/Eda Çelikeloğlu-Veri Bilimi-istanbulkodluyor.jpg",
                        "thumb": "assets/sertifikalar/featured-certificates/Eda Çelikeloğlu-Veri Bilimi-istanbulkodluyor.jpg"
                    },
                    {
                        "name": "Veri Mühendisliği, İBB",
                        "file": "assets/sertifikalar/featured-certificates/Eda Çelikeloğlu-Veri-Mühendisliği-ibb.jpg",
                        "thumb": "assets/sertifikalar/featured-certificates/Eda Çelikeloğlu-Veri-Mühendisliği-ibb.jpg"
                    }
                ],
                "Cisco Badges": [
                    {
                        "name": "Data Analytics Essentials Badge",
                        "file": "assets/sertifikalar/cisco-badges/Data_Analytics_Essentials_Badge20240522-8-ky8doy_cisco.pdf",
                        "thumb": "assets/sertifikalar/thumbnails/data_analytics_essentials_badge20240522-8-ky8doy_cisco.png"
                    },
                    {
                        "name": "Introduction to Data Science Badge",
                        "file": "assets/sertifikalar/cisco-badges/Introduction_to_Data_Science_Badge20240519-8-szt9p7_cisco.pdf",
                        "thumb": "assets/sertifikalar/thumbnails/introduction_to_data_science_badge20240519-8-szt9p7_cisco.png"
                    }
                ],
                "Geleceği Yazanlar": [
                    {
                        "name": "Derin Öğrenme 201",
                        "file": "assets/sertifikalar/gelecegi-yazanlar/Eda Çelikeloğlu-Derin Öğrenme201.pdf",
                        "thumb": "assets/sertifikalar/thumbnails/eda-celikeloglu-derin-ogrenme201.png"
                    },
                    {
                        "name": "Derin Öğrenme 301",
                        "file": "assets/sertifikalar/gelecegi-yazanlar/Eda Çelikeloğlu-Derin Öğrenme301.pdf",
                        "thumb": "assets/sertifikalar/thumbnails/eda-celikeloglu-derin-ogrenme301.png"
                    },
                    {
                        "name": "Derin Öğrenme 401",
                        "file": "assets/sertifikalar/gelecegi-yazanlar/Eda Çelikeloğlu-Derin Öğrenme401.pdf",
                        "thumb": "assets/sertifikalar/thumbnails/eda-celikeloglu-derin-ogrenme401.png"
                    },
                    {
                        "name": "Derin Öğrenme 501",
                        "file": "assets/sertifikalar/gelecegi-yazanlar/Eda Çelikeloğlu-Derin Öğrenme501.pdf",
                        "thumb": "assets/sertifikalar/thumbnails/eda-celikeloglu-derin-ogrenme501.png"
                    },
                    {
                        "name": "Makine Öğrenmesi 101",
                        "file": "assets/sertifikalar/gelecegi-yazanlar/Eda Çelikeloğlu-Makine Öğrenmesi101.pdf",
                        "thumb": "assets/sertifikalar/thumbnails/eda-celikeloglu-makine-ogrenmesi101.png"
                    },
                    {
                        "name": "Python 101",
                        "file": "assets/sertifikalar/gelecegi-yazanlar/Eda Çelikeloğlu-Python101.pdf",
                        "thumb": "assets/sertifikalar/thumbnails/eda-celikeloglu-python101.png"
                    },
                    {
                        "name": "Python 201",
                        "file": "assets/sertifikalar/gelecegi-yazanlar/Eda Çelikeloğlu-Python201.pdf",
                        "thumb": "assets/sertifikalar/thumbnails/eda-celikeloglu-python201.png"
                    },
                    {
                        "name": "Python 301",
                        "file": "assets/sertifikalar/gelecegi-yazanlar/Eda Çelikeloğlu-Python301.pdf",
                        "thumb": "assets/sertifikalar/thumbnails/eda-celikeloglu-python301.png"
                    },
                    {
                        "name": "Python 401",
                        "file": "assets/sertifikalar/gelecegi-yazanlar/Eda Çelikeloğlu-Python401.pdf",
                        "thumb": "assets/sertifikalar/thumbnails/eda-celikeloglu-python401.png"
                    },
                    {
                        "name": "Veri Bilimi ve Yapay Zekaya Giriş 101",
                        "file": "assets/sertifikalar/gelecegi-yazanlar/Eda Çelikeloğlu-Veri Bilimi ve Yapay Zekaya Giriş101.pdf",
                        "thumb": "assets/sertifikalar/thumbnails/eda-celikeloglu-veri-bilimi-ve-yapay-zekaya-giris101.png"
                    },
                    {
                        "name": "Veri Manipülasyonu 101",
                        "file": "assets/sertifikalar/gelecegi-yazanlar/Eda Çelikeloğlu-Veri Manipülasyonu101.pdf",
                        "thumb": "assets/sertifikalar/thumbnails/eda-celikeloglu-veri-manipulasyonu101.png"
                    },
                    {
                        "name": "Veri Manipülasyonu 201",
                        "file": "assets/sertifikalar/gelecegi-yazanlar/Eda Çelikeloğlu-Veri Manipülasyonu201.pdf",
                        "thumb": "assets/sertifikalar/thumbnails/eda-celikeloglu-veri-manipulasyonu201.png"
                    }
                ],
                "Miuul": [
                    {
                        "name": "CRM Analytics",
                        "file": "assets/sertifikalar/miuul-certificates/Eda Çelikeloğlu - CRM Analytics.pdf",
                        "thumb": "assets/sertifikalar/thumbnails/eda-celikeloglu-crm-analytics.png"
                    },
                    {
                        "name": "Feature Engineering",
                        "file": "assets/sertifikalar/miuul-certificates/Eda Çelikeloğlu - Feature Engineering.pdf",
                        "thumb": "assets/sertifikalar/thumbnails/eda-celikeloglu-feature-engineering.png"
                    },
                    {
                        "name": "Linear Algebra for Data Science",
                        "file": "assets/sertifikalar/miuul-certificates/Eda Çelikeloğlu - Linear Algebra for Data Science and.pdf",
                        "thumb": "assets/sertifikalar/thumbnails/eda-celikeloglu-linear-algebra-for-data-science-and.png"
                    },
                    {
                        "name": "Machine Learning",
                        "file": "assets/sertifikalar/miuul-certificates/Eda Çelikeloğlu - Machine Learning.pdf",
                        "thumb": "assets/sertifikalar/thumbnails/eda-celikeloglu-machine-learning.png"
                    },
                    {
                        "name": "Python Programming 101",
                        "file": "assets/sertifikalar/miuul-certificates/Eda Çelikeloğlu - Python Programming 101.pdf",
                        "thumb": "assets/sertifikalar/thumbnails/eda-celikeloglu-python-programming-101.png"
                    },
                    {
                        "name": "Querying MS SQL",
                        "file": "assets/sertifikalar/miuul-certificates/Eda Çelikeloğlu - Querying MS SQL.pdf",
                        "thumb": "assets/sertifikalar/thumbnails/eda-celikeloglu-querying-ms-sql.png"
                    },
                    {
                        "name": "Time Series",
                        "file": "assets/sertifikalar/miuul-certificates/Eda Çelikeloğlu - Time Series.pdf",
                        "thumb": "assets/sertifikalar/thumbnails/eda-celikeloglu-time-series.png"
                    }
                ],
                "Diğer": [
                    {
                        "name": "BT İş Analisti Sertifikası",
                        "file": "assets/sertifikalar/others/BT_Is_Analisti_Sertifika_teedo.pdf",
                        "thumb": "assets/sertifikalar/thumbnails/bt_is_analisti_sertifika_teedo.png"
                    },
                    {
                        "name": "Veri Bilimi",
                        "file": "assets/sertifikalar/others/Eda_Celikeloglu-Veri_Bilimi-ecodation.pdf",
                        "thumb": "assets/sertifikalar/thumbnails/eda-celikeloglu-veri-bilimi-ecodation.png"
                    },
                    {
                        "name": "EF SET Certificate English B1",
                        "file": "assets/sertifikalar/others/EF SET Certificate_english_b1.pdf",
                        "thumb": "assets/sertifikalar/thumbnails/ef-set-certificate_english_b1.png"
                    },
                    {
                        "name": "Uygulamalı Microsoft Power BI",
                        "file": "assets/sertifikalar/others/Uygulamali_Microsoft_Power_BI_Sertifika_btk.pdf",
                        "thumb": "assets/sertifikalar/thumbnails/uygulamali_microsoft_power_bi_sertifika_btk.png"
                    }
                ]
            }
        },
        "English": {
            "categories": {
                "Featured": [
                    {
                        "name": "Data Science, Istanbul Kodluyor",
                        "file": "assets/sertifikalar/featured-certificates/Eda Çelikeloğlu-Veri Bilimi-istanbulkodluyor.jpg",
                        "thumb": "assets/sertifikalar/featured-certificates/Eda Çelikeloğlu-Veri Bilimi-istanbulkodluyor.jpg"
                    },
                    {
                        "name": "Data Engineering, IBB",
                        "file": "assets/sertifikalar/featured-certificates/Eda Çelikeloğlu-Veri-Mühendisliği-ibb.jpg",
                        "thumb": "assets/sertifikalar/featured-certificates/Eda Çelikeloğlu-Veri-Mühendisliği-ibb.jpg"
                    }
                ],
                "Cisco Badges": [
                    {
                        "name": "Data Analytics Essentials Badge",
                        "file": "assets/sertifikalar/cisco-badges/Data_Analytics_Essentials_Badge20240522-8-ky8doy_cisco.pdf",
                        "thumb": "assets/sertifikalar/thumbnails/data_analytics_essentials_badge20240522-8-ky8doy_cisco.png"
                    },
                    {
                        "name": "Introduction to Data Science Badge",
                        "file": "assets/sertifikalar/cisco-badges/Introduction_to_Data_Science_Badge20240519-8-szt9p7_cisco.pdf",
                        "thumb": "assets/sertifikalar/thumbnails/introduction_to_data_science_badge20240519-8-szt9p7_cisco.png"
                    }
                ],
                "Geleceği Yazanlar": [
                    {
                        "name": "Deep Learning 201",
                        "file": "assets/sertifikalar/gelecegi-yazanlar/Eda Çelikeloğlu-Derin Öğrenme201.pdf",
                        "thumb": "assets/sertifikalar/thumbnails/eda-celikeloglu-derin-ogrenme201.png"
                    },
                    {
                        "name": "Deep Learning 301",
                        "file": "assets/sertifikalar/gelecegi-yazanlar/Eda Çelikeloğlu-Derin Öğrenme301.pdf",
                        "thumb": "assets/sertifikalar/thumbnails/eda-celikeloglu-derin-ogrenme301.png"
                    },
                    {
                        "name": "Deep Learning 401",
                        "file": "assets/sertifikalar/gelecegi-yazanlar/Eda Çelikeloğlu-Derin Öğrenme401.pdf",
                        "thumb": "assets/sertifikalar/thumbnails/eda-celikeloglu-derin-ogrenme401.png"
                    },
                    {
                        "name": "Deep Learning 501",
                        "file": "assets/sertifikalar/gelecegi-yazanlar/Eda Çelikeloğlu-Derin Öğrenme501.pdf",
                        "thumb": "assets/sertifikalar/thumbnails/eda-celikeloglu-derin-ogrenme501.png"
                    },
                    {
                        "name": "Machine Learning 101",
                        "file": "assets/sertifikalar/gelecegi-yazanlar/Eda Çelikeloğlu-Makine Öğrenmesi101.pdf",
                        "thumb": "assets/sertifikalar/thumbnails/eda-celikeloglu-makine-ogrenmesi101.png"
                    },
                    {
                        "name": "Python 101",
                        "file": "assets/sertifikalar/gelecegi-yazanlar/Eda Çelikeloğlu-Python101.pdf",
                        "thumb": "assets/sertifikalar/thumbnails/eda-celikeloglu-python101.png"
                    },
                    {
                        "name": "Python 201",
                        "file": "assets/sertifikalar/gelecegi-yazanlar/Eda Çelikeloğlu-Python201.pdf",
                        "thumb": "assets/sertifikalar/thumbnails/eda-celikeloglu-python201.png"
                    },
                    {
                        "name": "Python 301",
                        "file": "assets/sertifikalar/gelecegi-yazanlar/Eda Çelikeloğlu-Python301.pdf",
                        "thumb": "assets/sertifikalar/thumbnails/eda-celikeloglu-python301.png"
                    },
                    {
                        "name": "Python 401",
                        "file": "assets/sertifikalar/gelecegi-yazanlar/Eda Çelikeloğlu-Python401.pdf",
                        "thumb": "assets/sertifikalar/thumbnails/eda-celikeloglu-python401.png"
                    },
                    {
                        "name": "Introduction to Data Science and AI 101",
                        "file": "assets/sertifikalar/gelecegi-yazanlar/Eda Çelikeloğlu-Veri Bilimi ve Yapay Zekaya Giriş101.pdf",
                        "thumb": "assets/sertifikalar/thumbnails/eda-celikeloglu-veri-bilimi-ve-yapay-zekaya-giris101.png"
                    },
                    {
                        "name": "Data Manipulation 101",
                        "file": "assets/sertifikalar/gelecegi-yazanlar/Eda Çelikeloğlu-Veri Manipülasyonu101.pdf",
                        "thumb": "assets/sertifikalar/thumbnails/eda-celikeloglu-veri-manipulasyonu101.png"
                    },
                    {
                        "name": "Data Manipulation 201",
                        "file": "assets/sertifikalar/gelecegi-yazanlar/Eda Çelikeloğlu-Veri Manipülasyonu201.pdf",
                        "thumb": "assets/sertifikalar/thumbnails/eda-celikeloglu-veri-manipulasyonu201.png"
                    }
                ],
                "Miuul": [
                    {
                        "name": "CRM Analytics",
                        "file": "assets/sertifikalar/miuul-certificates/Eda Çelikeloğlu - CRM Analytics.pdf",
                        "thumb": "assets/sertifikalar/thumbnails/eda-celikeloglu-crm-analytics.png"
                    },
                    {
                        "name": "Feature Engineering",
                        "file": "assets/sertifikalar/miuul-certificates/Eda Çelikeloğlu - Feature Engineering.pdf",
                        "thumb": "assets/sertifikalar/thumbnails/eda-celikeloglu-feature-engineering.png"
                    },
                    {
                        "name": "Linear Algebra for Data Science",
                        "file": "assets/sertifikalar/miuul-certificates/Eda Çelikeloğlu - Linear Algebra for Data Science and.pdf",
                        "thumb": "assets/sertifikalar/thumbnails/eda-celikeloglu-linear-algebra-for-data-science-and.png"
                    },
                    {
                        "name": "Machine Learning",
                        "file": "assets/sertifikalar/miuul-certificates/Eda Çelikeloğlu - Machine Learning.pdf",
                        "thumb": "assets/sertifikalar/thumbnails/eda-celikeloglu-machine-learning.png"
                    },
                    {
                        "name": "Python Programming 101",
                        "file": "assets/sertifikalar/miuul-certificates/Eda Çelikeloğlu - Python Programming 101.pdf",
                        "thumb": "assets/sertifikalar/thumbnails/eda-celikeloglu-python-programming-101.png"
                    },
                    {
                        "name": "Querying MS SQL",
                        "file": "assets/sertifikalar/miuul-certificates/Eda Çelikeloğlu - Querying MS SQL.pdf",
                        "thumb": "assets/sertifikalar/thumbnails/eda-celikeloglu-querying-ms-sql.png"
                    },
                    {
                        "name": "Time Series",
                        "file": "assets/sertifikalar/miuul-certificates/Eda Çelikeloğlu - Time Series.pdf",
                        "thumb": "assets/sertifikalar/thumbnails/eda-celikeloglu-time-series.png"
                    }
                ],
                "Others": [
                    {
                        "name": "Business Analyst Certificate",
                        "file": "assets/sertifikalar/others/BT_Is_Analisti_Sertifika_teedo.pdf",
                        "thumb": "assets/sertifikalar/thumbnails/bt_is_analisti_sertifika_teedo.png"
                    },
                    {
                        "name": "Data Science",
                        "file": "assets/sertifikalar/others/Eda Çelikeloğlu-Veri Bilimi-ecodation.pdf",
                        "thumb": "assets/sertifikalar/thumbnails/eda-celikeloglu-veri-bilimi-ecodation.png"
                    },
                    {
                        "name": "EF SET Certificate English B1",
                        "file": "assets/sertifikalar/others/EF SET Certificate_english_b1.pdf",
                        "thumb": "assets/sertifikalar/thumbnails/ef-set-certificate_english_b1.png"
                    },
                    {
                        "name": "Applied Microsoft Power BI",
                        "file": "assets/sertifikalar/others/Uygulamali_Microsoft_Power_BI_Sertifika_btk.pdf",
                        "thumb": "assets/sertifikalar/thumbnails/uygulamali_microsoft_power_bi_sertifika_btk.png"
                    }
                ]
            }
        }
    }

    if "active_certificate" not in st.session_state:
        st.session_state.active_certificate = None
    if "certificate_modal_id" not in st.session_state:
        st.session_state.certificate_modal_id = None

    data = certificates_data[language]

    st.markdown("""
    <style>
    .cert-category-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #667eea;
        margin: 1rem 0 0.8rem 0;
    }

    .cert-thumb-wrap:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 26px rgba(102,126,234,0.16);
    }

    div[data-testid="stButton"] > button[kind="secondary"] {
        border-radius: 12px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    for category, certs in data["categories"].items():
        st.markdown(f"<div class='cert-category-title'>{category}</div>", unsafe_allow_html=True)

        cols_per_row = 4
        for i in range(0, len(certs), cols_per_row):
            cols = st.columns(cols_per_row)

            for j, col in enumerate(cols):
                if i + j < len(certs):
                    cert = certs[i + j]
                    with col:
                        preview_path = cert.get("thumb")

                        if preview_path and os.path.exists(preview_path):
                            st.image(preview_path, use_container_width=True)
                        else:
                            st.markdown("""
                            <div style="
                                height: 180px;
                                display:flex;
                                align-items:center;
                                justify-content:center;
                                background: linear-gradient(135deg, #eef2ff 0%, #f7ecff 100%);
                                border-radius: 12px;
                                color: #667eea;
                                font-weight: 700;
                                text-align:center;
                                padding: 1rem;
                            ">
                                CERTIFICATE
                            </div>
                            """, unsafe_allow_html=True)

                        if st.button(
                                f"👁️ {cert['name']}",
                                key=f"cert_open_{category}_{i + j}",
                                use_container_width=True
                        ):
                            st.session_state.active_certificate = cert
                            st.session_state.certificate_modal_id = f"cert_{random.randint(1000, 9999)}"
                            st.rerun()


    if st.session_state.active_certificate:
        open_certificate_modal(
            st.session_state.active_certificate,
            st.session_state.certificate_modal_id
        )


def show_contact_section():
    # Column'ları yukarıdan hizalamak için CSS
    st.markdown("""
    <style>
    [data-testid="column"] {
        display: flex !important;
        flex-direction: column !important;
        align-items: stretch !important;
        vertical-align: top !important;
    }
    [data-testid="stForm"] {
        background: linear-gradient(135deg, #7b8ff5 0%, #8b5fb8 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        height: 550px;
        display: flex;
        flex-direction: column;
        margin-top: 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # İletişim bilgileri ve mesaj formu yan yana
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if language == "Türkçe":
            st.markdown("""
            <div class="contact-card" style="height: 550px;">
                <h3 style="color:white; margin-bottom: 1rem; text-align: center;">İletişime Geçelim! 🚀</h3>
                <p style="opacity: 0.9;">Projeleriniz, veri bilimi üzerine fikir alışverişi veya iş birliği fırsatları için benimle iletişime geçebilirsiniz.</p>
                <p style="opacity: 0.9;">Aşağıdaki kanallardan ulaşabilirsiniz 👇</p>
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
                        🦆 Kaggle <br><br><br><br>
                    </a>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="contact-card" style="height: 550px;">
                <h3 style="color:white; margin-bottom: 1rem; text-align: center;">Let's Get in Touch! 🚀</h3>
                <p style="opacity: 0.9;">Feel free to reach out for projects, data science discussions, or collaboration opportunities.</p>
                <p style="opacity: 0.9;">You can contact me via the links below 👇</p>
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
            form_title = "Ya da Mesaj Gönder 💌"
            name_label = "İsminiz"
            email_label = "E-posta Adresiniz"
            message_label = "Mesajınız"
            submit_label = "📤 Gönder"
            success_msg = "Mesajınız başarıyla gönderildi! Teşekkür ederim 🙏"
            warning_msg = "Lütfen tüm alanları doldurun."
            subject_prefix = "Yeni mesaj:"
        else:
            form_title = "Send a Message 💌"
            name_label = "Your Name"
            email_label = "Your Email"
            message_label = "Message"
            submit_label = "📤 Send"
            success_msg = "Your message has been sent successfully! Thank you 🙏"
            warning_msg = "Please fill in all fields."
            subject_prefix = "New message:"
        
        with st.form("contact_form"):
            # Başlık
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
elif selected_section == "skills":
    show_skills_section()
elif selected_section == "projects":
    show_projects_section()
elif selected_section == "awards":
    show_awards_section()
elif selected_section == "testimonials":
    show_testimonials_section()
elif selected_section == "certificates":
    show_certificates_section()
elif selected_section == "contact":
    show_contact_section()

# Footer
st.markdown(
    """
    <div style="position: fixed; bottom: 0; left: 0; width: 100%; 
                background: linear-gradient(135deg, #f5f7fa 0%, #e8eaf6 50%, #f3e5f5 100%); 
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





