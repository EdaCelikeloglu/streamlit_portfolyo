import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
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
            "id":"datathon",
            "title":"🏆 UP School & Bitexen Women in Datathon 2024",
            "title_tr":"🏆 UP School & Bitexen Women in Datathon 2024",
            "title_en":"🏆 UP School & Bitexen Women in Datathon 2024",
            "thumb":"https://raw.githubusercontent.com/EdaCelikeloglu/streamlit_portfolyo/master/assets/wid_kapak.PNG",
            "desc_tr": """Kadınların iş gücüne katılımı, sağlık, toplumsal cinsiyet rolleri ve siyasi temsiliyetin ücret eşitsizliği üzerindeki etkisini analiz etmek için çoklu doğrusal regresyon modeli oluşturdum.
Toplumsal cinsiyet rollerinin işe yerleşim üzerindeki etkisini incelemek amacıyla lojistik regresyon uyguladım.
Üç kişilik bir ekipte iş birliği içinde çalışarak planlama, ekip çalışması ve zaman yönetimi becerilerimi geliştirdim.
Tüm katılımcılar arasında birincilik elde ettim.""",
            "desc_en": """Built a multiple linear regression model to analyze the influence of women’s labor force participation, health, gender roles, and political representation on wage inequality.
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
            "desc_tr":"İstanbul’daki konut piyasası dinamikleri ile hava durumu koşulları arasındaki ilişkiyi açık veri kaynaklarını entegre ederek analiz ettim. Open-Meteo API’si aracılığıyla gerçek zamanlı meteorolojik verileri topladım ve bu verileri satılık dairelerin görüntülenme ve aranma istatistikleriyle birleştirdim. Zaman serisi modellemesi kullanarak sıcaklık, yağış ve diğer hava değişkenlerinin kullanıcı etkileşim eğilimleri üzerindeki etkisini inceledim. Analizde dışsal hava faktörlerinin etkisini ölçmek için SARIMAX modelinden yararlandım ve elde ettiğim bulguları detaylı bir rapor ve görselleştirmeler eşliğinde sundum.",
            "desc_en":"I analyzed the relationship between housing market dynamics and weather conditions in Istanbul by integrating open data sources. Using the Open-Meteo API, I collected real-time meteorological data and combined it with digital metrics on the views and search volumes of apartments listed for sale. Through time series modeling, I examined how changes in temperature, precipitation, and other weather variables influenced user engagement trends. The analysis employed the SARIMAX model to capture the impact of exogenous weather factors, and I presented the key insights through a detailed report and visualization.",
            "links":[]
        },
        {
            "id":"powerbi",
            "title":"📊 Sales Analyses - Power BI Dashboard",
            "title_tr":"📊 Satış Analizleri - Power BI Dashboard",
            "title_en":"📊 Sales Analyses - Power BI Dashboard",
            "thumb":"https://raw.githubusercontent.com/EdaCelikeloglu/streamlit_portfolyo/master/assets/powerbi1.PNG",
            "desc_tr":"Bölgeler ve ürün kategorileri genelinde performans metriklerini görselleştiren etkileşimli bir Power BI dashboard’u.",
            "desc_en":"Interactive Power BI dashboard visualizing performance across regions and product categories.",
            "pdf_raw":"https://raw.githubusercontent.com/EdaCelikeloglu/streamlit_portfolyo/master/assets/Eda_Celikeloglu_Sales_Summaries.pdf",
            "powerbi_link":"https://app.powerbi.com/reportEmbed?reportId=d8b1f2ec-5c17-4864-a9d3-64f415eb5f6e&autoAuth=true&ctid=92e0b030-5e40-4cdd-8ff8-51fa8a4504e2",
            "links":[]
        }
    ]

    # ===== state =====
    if "active_modal" not in st.session_state:
        st.session_state["active_modal"] = None

    def open_modal(pid):
        st.session_state["active_modal"] = pid
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
        inject_modal_top(p, language)


def inject_modal_top(p, language: str):
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

    # Modal içerik + stil (parent DOM’a basılacak)
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
    js = f"""
    <script>
      const doc = window.parent.document;

      // Eski modal varsa temizle
      const old = doc.getElementById('x-modal-wrapper');
      if (old) old.remove();

      // Wrapper oluştur ve içeriği bas
      const wrapper = doc.createElement('div');
      wrapper.id = 'x-modal-wrapper';
      wrapper.innerHTML = {payload};
      doc.body.appendChild(wrapper);

      function closeModal() {{
        const w = doc.getElementById('x-modal-wrapper');
        if (w) w.remove();
      }}

      doc.getElementById('x-close').addEventListener('click', closeModal);
      doc.getElementById('x-modal-overlay').addEventListener('click', closeModal);
      doc.addEventListener('keydown', (e) => {{ if (e.key === 'Escape') closeModal(); }});
    </script>
    """

    # 0 px yüksekliğe göm; görünür olan parent’a eklenen modal olur
    components.html(js, height=0, width=0)


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