"""
AI Allergen Detector
Streamlit Dashboard for Multilingual Food Label Analysis powered by Sarvam AI.
Designed for Food Technology & Biochemical Engineering Applications.
"""

import os
import io
import time
from PIL import Image
import streamlit as st
from dotenv import load_dotenv

# Load local environment variables
load_dotenv()

from backend.allergen_engine import AllergenDetectorEngine, ALLERGEN_DATABASE
from backend.sarvam_client import SarvamService
from sample_labels.sample_data import SAMPLE_PRODUCTS

# Streamlit Page Config
st.set_page_config(
    page_title="AI Allergen Detector | Sarvam AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.3rem;
        font-weight: 800;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #475569;
        margin-bottom: 1.2rem;
    }
    .status-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .danger-box {
        background-color: #FEF2F2;
        border-left: 6px solid #DC2626;
        padding: 16px;
        border-radius: 8px;
        margin-bottom: 16px;
    }
    .caution-box {
        background-color: #FFFBEB;
        border-left: 6px solid #D97706;
        padding: 16px;
        border-radius: 8px;
        margin-bottom: 16px;
    }
    .safe-box {
        background-color: #F0FDF4;
        border-left: 6px solid #16A34A;
        padding: 16px;
        border-radius: 8px;
        margin-bottom: 16px;
    }
    .bio-card {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 14px;
        margin-bottom: 10px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding-top: 10px;
        padding-bottom: 10px;
        border-radius: 6px;
    }
</style>
""", unsafe_allow_html=True)


# --- SIDEBAR CONFIGURATION ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/shield.png", width=64)
    st.title("Settings & Profile")

    st.subheader("1. 🔑 Sarvam AI API")
    env_key = os.getenv("SARVAM_API_KEY", "")
    api_key_input = st.text_input(
        "Enter Sarvam API Key:",
        value=env_key,
        type="password",
        help="Get your key at https://dashboard.sarvam.ai"
    )

    is_live_api = st.toggle("Enable Live Sarvam Cloud APIs", value=bool(api_key_input.strip()))
    sarvam = SarvamService(api_key=api_key_input if is_live_api else None)

    if sarvam.is_configured() and is_live_api:
        st.success("🟢 Sarvam API: Active & Connected")
    else:
        st.info("ℹ️ Local Engine / Demo Mode Active (Enter Sarvam API Key for cloud OCR & TTS)")

    st.markdown("---")
    st.subheader("2. 🌐 Output Language")
    language_choice = st.selectbox(
        "Select Audio & Explanation Language:",
        options=["English", "हिन्दी (Hindi)", "বাংলা (Bengali)"],
        index=0
    )
    lang_code_map = {
        "English": "en",
        "हिन्दी (Hindi)": "hi",
        "বাংলা (Bengali)": "bn"
    }
    target_lang = lang_code_map[language_choice]

    st.markdown("---")
    st.subheader("3. 🩺 Your Allergy Profile")
    st.caption("Select ingredients and allergens you must strictly avoid:")

    allergen_options = {
        "peanuts": "🥜 Peanuts / Groundnuts (मूंगफली / চিনাবাদাম)",
        "milk": "🥛 Milk & Dairy (Lactose / Casein / Whey)",
        "gluten": "🌾 Gluten & Wheat (Maida / Suji / Atta / Celiac)",
        "tree_nuts": "🌰 Tree Nuts (Cashew / Almond / Pista / Walnut)",
        "soy": "🌱 Soy & Soya Lecithin (INS 322)",
        "egg": "🥚 Egg (Albumin / Lysozyme INS 1105)",
        "mustard": "🌿 Mustard (Sarson / Rai / সর্ষে)",
        "sesame": "🧂 Sesame (Til / তিল)",
        "seafood": "🦐 Fish & Shellfish (Prawns / Crab / মাছ)",
        "sulfites": "🍷 Sulfites & Sulphur Dioxide (INS 220-228)"
    }

    selected_allergen_keys = st.multiselect(
        "Known Allergens:",
        options=list(allergen_options.keys()),
        default=["peanuts", "gluten"],
        format_func=lambda k: allergen_options[k]
    )

    custom_allergen = st.text_input(
        "Additional Custom Allergies / Sensitivity:",
        placeholder="e.g. Chickpea, Fenugreek, MSG, Strawberry",
        help="Separate multiple items with commas"
    )

    st.markdown("---")
    st.caption("🎓 **Food Tech & Biochemical Engineering Project**\n*Multilingual Indic Food Label Parser with FSSAI Compliance & Clinical Epitope Mapping.*")


# --- MAIN HEADER ---
st.markdown('<div class="main-title">🛡️ AI Allergen Detector</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">'
    'Multilingual Food Safety, Biochemical Epitope Screener & Nutritional Health Analysis powered by <b>Sarvam AI</b>.'
    ' Supports packaging labels in <b>English</b>, <b>हिन्दी (Hindi)</b>, and <b>বাংলা (Bengali)</b>.'
    '</div>',
    unsafe_allow_html=True
)

# --- STEP 1: INPUT PRODUCT LABEL ---
st.markdown("### 📸 1. Input Food Product Label")

tab_upload, tab_camera, tab_samples = st.tabs([
    "📁 Upload Image",
    "📷 Take Photo (Camera)",
    "🧪 Preset Multilingual Samples"
])

uploaded_image = None
label_text_to_process = ""
selected_sample_title = ""

with tab_upload:
    file_upload = st.file_uploader(
        "Upload a picture of any food packaging or ingredient list (JPG, PNG):",
        type=["jpg", "jpeg", "png", "webp"]
    )
    if file_upload:
        uploaded_image = Image.open(file_upload)
        # Use live Sarvam Doc-AI if available
        if is_live_api and sarvam.is_configured():
            with st.spinner("🤖 Sarvam Document AI is digitizing the multilingual food label..."):
                file_bytes = file_upload.getvalue()
                ocr_result = sarvam.digitise_document(file_bytes, file_name=file_upload.name)
                if ocr_result["success"]:
                    label_text_to_process = ocr_result["text"]
                else:
                    st.warning(f"Sarvam Doc-AI Notice: {ocr_result.get('error')}. You can review or edit the text below.")
        else:
            # Fallback or manual entry prompt
            st.info("Tip: Enter or paste the extracted text below, or enable Live Sarvam API in sidebar for automated Cloud OCR.")
            label_text_to_process = st.text_area(
                "Extracted or Label Text:",
                value="",
                placeholder="Paste or edit the ingredient text from the image here..."
            )

with tab_camera:
    camera_file = st.camera_input("Capture picture of food packaging directly:")
    if camera_file:
        uploaded_image = Image.open(camera_file)
        if is_live_api and sarvam.is_configured():
            with st.spinner("🤖 Sarvam Document AI is digitizing your captured food label..."):
                file_bytes = camera_file.getvalue()
                ocr_result = sarvam.digitise_document(file_bytes, file_name="camera_label.jpg")
                if ocr_result["success"]:
                    label_text_to_process = ocr_result["text"]
                else:
                    st.warning(f"Doc-AI notice: {ocr_result.get('error')}")

with tab_samples:
    st.caption("Select a pre-loaded authentic multilingual product label to test immediately:")
    sample_col1, sample_col2 = st.columns([1, 2])
    
    with sample_col1:
        sample_choice = st.radio(
            "Select Preset Product:",
            options=[p["title"] for p in SAMPLE_PRODUCTS],
            index=0
        )
    
    chosen_product = next(p for p in SAMPLE_PRODUCTS if p["title"] == sample_choice)
    selected_sample_title = chosen_product["title"]
    
    with sample_col2:
        st.markdown(f"**{chosen_product['title']}**")
        st.markdown(f"*{chosen_product['subtitle']}*")
        st.caption(f"Languages: {chosen_product['primary_language']}")
        
        # Load sample image if exists
        sample_img_path = os.path.join(
            os.path.dirname(__file__), "sample_labels", f"{chosen_product['id']}.jpg"
        )
        if os.path.exists(sample_img_path):
            sample_img = Image.open(sample_img_path)
            st.image(sample_img, caption="Synthetic Label Replica for OCR Testing", width=380)
            if not uploaded_image:
                uploaded_image = sample_img
        
        if not label_text_to_process or tab_samples:
            label_text_to_process = chosen_product["label_text"]


# --- DISPLAY SELECTED IMAGE & TEXT PREVIEW ---
if uploaded_image or label_text_to_process:
    st.markdown("---")
    st.markdown("### 🔍 2. Food Label Inspection & Extracted Text")
    
    col_img, col_txt = st.columns([1, 2])
    with col_img:
        if uploaded_image:
            st.image(uploaded_image, caption="Uploaded Food Label", use_container_width=True)
        else:
            st.info("No image file loaded. Working from text.")

    with col_txt:
        st.markdown("**Scanned Ingredients & Allergen Declaration:**")
        editable_text = st.text_area(
            "Text to analyze (you may adjust or add Indic terms):",
            value=label_text_to_process,
            height=200
        )
        label_text_to_process = editable_text

    # --- EXECUTE BIOCHEMICAL & ALLERGEN ANALYSIS ---
    analyze_btn = st.button("🚀 Analyze Food Safety & Health Impact", type="primary", use_container_width=True)
    
    if analyze_btn or label_text_to_process:
        analysis = AllergenDetectorEngine.analyze_label(
            extracted_text=label_text_to_process,
            user_allergens=selected_allergen_keys,
            custom_allergen_input=custom_allergen
        )

        st.markdown("---")
        st.markdown("## 📊 3. Allergen Safety Verdict")

        # --- SAFETY STATUS BANNER ---
        status = analysis["safety_status"]
        if status == "DANGER":
            st.markdown(f"""
            <div class="danger-box">
                <h2 style="color: #991B1B; margin-top:0;">{analysis['verdict_title']}</h2>
                <h4 style="color: #B91C1C;">⛔ DO NOT CONSUME THIS PRODUCT!</h4>
                <p style="font-size: 1.05rem; color: #7F1D1D; margin-bottom: 0;">
                    <b>{analysis['summaries'][target_lang]}</b>
                </p>
            </div>
            """, unsafe_allow_html=True)
        elif status == "CAUTION":
            st.markdown(f"""
            <div class="caution-box">
                <h2 style="color: #92400E; margin-top:0;">{analysis['verdict_title']}</h2>
                <h4 style="color: #B45309;">⚠️ ADVISORY / TRACE ALLERGEN WARNING</h4>
                <p style="font-size: 1.05rem; color: #78350F; margin-bottom: 0;">
                    <b>{analysis['summaries'][target_lang]}</b>
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="safe-box">
                <h2 style="color: #166534; margin-top:0;">{analysis['verdict_title']}</h2>
                <h4 style="color: #15803D;">✅ NO DETECTED ALLERGENS MATCHING YOUR PROFILE</h4>
                <p style="font-size: 1.05rem; color: #14532D; margin-bottom: 0;">
                    <b>{analysis['summaries'][target_lang]}</b>
                </p>
            </div>
            """, unsafe_allow_html=True)

        # --- VOICE ALERT VIA SARVAM BULBUL TTS ---
        st.markdown("#### 🔊 Spoken Safety Alert (Sarvam Bulbul TTS)")
        spoken_text = analysis["summaries"][target_lang]
        
        audio_cols = st.columns([3, 1])
        with audio_cols[0]:
            st.caption(f"Spoken Announcement in {language_choice}: *\"{spoken_text}\"*")
        
        # Check if user requested voice synthesis
        if is_live_api and sarvam.is_configured():
            with st.spinner("Generating Indic voice alert via Sarvam Bulbul TTS..."):
                audio_bytes = sarvam.generate_speech_alert(spoken_text, lang=target_lang)
                if audio_bytes:
                    st.audio(audio_bytes, format="audio/wav")
                else:
                    st.caption("ℹ️ Cloud TTS audio synthesis completed or limit reached.")
        else:
            st.info("💡 Connect your Sarvam API Key to hear real-time Indian accent voice warnings in English, Hindi, or Bengali!")

        # --- DETECTED ALLERGENS BREAKDOWN ---
        st.markdown("### 🔬 Biochemical Allergen Breakdown")
        col_direct, col_advisory = st.columns(2)

        with col_direct:
            st.markdown("#### 🚨 Direct Allergenic Ingredients Detected")
            if analysis["detected_direct_allergens"]:
                for item in analysis["detected_direct_allergens"]:
                    st.error(
                        f"**{item['name']}**\n\n"
                        f"- **Matched Words:** `{', '.join(item['matched_tokens'])}`\n"
                        f"- **Biochemical Epitope / Storage Protein:** {item['bio_protein']}\n"
                        f"- **Anaphylaxis Severity Risk:** `{item['anaphylaxis_risk']}`\n"
                        f"- **Clinical Context:** {item['clinical_note']}"
                    )
            else:
                st.success("None of your specified allergens were detected as direct ingredients.")

        with col_advisory:
            st.markdown("#### ⚠️ Cross-Contamination / Advisory Traces")
            if analysis["detected_advisory_allergens"]:
                for item in analysis["detected_advisory_allergens"]:
                    st.warning(
                        f"**{item['name']}** (Facility / Advisory Trace)\n\n"
                        f"- **Found Advisory Tokens:** `{', '.join(item['matched_tokens'])}`\n"
                        f"- **Risk Mechanism:** Shared processing machinery or packaging lines."
                    )
            else:
                st.info("No cross-contamination warnings found for your specified allergens.")

        # --- GOOD & BAD BIOCHEMICAL EFFECTS ---
        st.markdown("---")
        st.markdown("## 🧪 4. Food Science & Biochemical Health Effects")
        st.caption("Comprehensive analysis of nutritional benefits, metabolic risks, and additives for this food product.")

        col_good, col_bad = st.columns(2)

        with col_good:
            st.markdown("### 🟢 Positive Biochemical Effects")
            if analysis["good_effects"]:
                for item in analysis["good_effects"]:
                    st.markdown(f"""
                    <div class="bio-card" style="border-left: 4px solid #10B981;">
                        <h4 style="color: #065F46; margin-bottom: 4px;">✨ {item['factor']}</h4>
                        <p style="color: #1F2937; font-size: 0.95rem; margin-bottom: 0;">
                            <b>Biochemical Mechanism:</b> {item['biochemical_mechanism']}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No prominent functional or whole-food biochemical markers identified on this label.")

        with col_bad:
            st.markdown("### 🔴 Adverse Biochemical Effects & Metabolic Risks")
            if analysis["bad_effects"]:
                for item in analysis["bad_effects"]:
                    st.markdown(f"""
                    <div class="bio-card" style="border-left: 4px solid #EF4444;">
                        <h4 style="color: #991B1B; margin-bottom: 4px;">⚠️ {item['factor']}</h4>
                        <p style="color: #1F2937; font-size: 0.95rem; margin-bottom: 0;">
                            <b>Biochemical Mechanism:</b> {item['biochemical_mechanism']}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.success("No high-risk additives, trans fats, or extreme glycemic triggers identified.")

        # --- FOOD ADDITIVES & INS DATABASE SCREENER ---
        st.markdown("---")
        st.markdown("### 🏷️ 5. Food Additives & INS Chemical Screener")
        if analysis["additives_profile"]:
            st.caption(f"Detected {len(analysis['additives_profile'])} regulated INS/E-numbers on product label:")
            for add in analysis["additives_profile"]:
                with st.expander(f"📌 {add['name']} — [{add['class']}] ({add['risk_level']})"):
                    st.write(f"**Biochemical & Physiological Effect:** {add['biochemical_effect']}")
                    st.write(f"**Safety Classification:** `{add['risk_level']}`")
        else:
            st.info("No standard INS or E-number codes were detected on this label.")

        # --- NOVA ULTRA-PROCESSED FOOD CLASSIFICATION ---
        st.markdown("---")
        st.markdown("### 🏭 6. NOVA Food Processing Classification")
        nova = analysis["nova"]
        score = nova["score"]
        
        cols_nova = st.columns([1, 3])
        with cols_nova[0]:
            if score == 4:
                st.error(f"### {nova['title']}")
            elif score == 3:
                st.warning(f"### {nova['title']}")
            else:
                st.success(f"### {nova['title']}")
        with cols_nova[1]:
            st.markdown(f"**Biochemical Processing Context:** {nova['explanation']}")
            st.progress(score / 4.0)

        # --- OPTIONAL DEEP LLM ANALYSIS (SARVAM CHAT 105B) ---
        if is_live_api and sarvam.is_configured():
            st.markdown("---")
            st.markdown("### 🤖 7. Sarvam-105B Advanced Biochemical Consultation")
            with st.expander("Click to generate full Indic LLM Food Science Report"):
                with st.spinner("Sarvam-105B is generating detailed clinical consultation..."):
                    llm_result = sarvam.chat_analyze_biochemistry(
                        label_text=label_text_to_process,
                        user_allergens=[ALLERGEN_DATABASE[k]["display_name"] for k in selected_allergen_keys if k in ALLERGEN_DATABASE],
                        target_lang=target_lang
                    )
                    if llm_result["success"]:
                        st.markdown(llm_result["response"])
                    else:
                        st.error(llm_result["response"])

# --- FOOTER ---
st.markdown("---")
st.markdown(
    "<center><small>AI Allergen Detector | Developed for Food Tech & Biochemical Engineering | Powered by Sarvam AI</small></center>",
    unsafe_allow_html=True
)
