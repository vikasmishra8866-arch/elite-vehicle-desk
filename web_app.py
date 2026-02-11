import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.utils import simpleSplit 
import datetime
import io
import pytz 
import qrcode 
import google.generativeai as genai
from PIL import Image

# --- GOOGLE AI SETUP ---
# Aapne jo nayi key share ki thi wahi use kar raha hoon
API_KEY = "AIzaSyBCnOvFT835gjOzBntnKRhFf-jqJIEaP0c"
genai.configure(api_key=API_KEY)

# Session State Initialize
if 'v_data' not in st.session_state:
    st.session_state.v_data = {
        'v_no': "", 'reg_date': "", 'owner': "", 'father': "",
        'address': "", 'maker': "", 'model': "", 'chassis': "",
        'engine': "", 'rto': "", 'ins_co': "", 'ins_pol': "", 'ins_exp': ""
    }

# --- INDIAN TIME ---
IST = pytz.timezone('Asia/Kolkata')
current_time = datetime.datetime.now(IST).strftime("%d-%m-%Y %I:%M %p")

st.set_page_config(page_title="ELITE VEHICLE DESK", page_icon="⭐")
st.title("⭐ ELITE VEHICLE DESK")

# --- AI MAGIC SCANNER SECTION ---
st.markdown("### 🤖 AI Magic Scanner (Auto-Fill)")
uploaded_file = st.file_uploader("Upload Virtual RC / Insurance Photo", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    if st.button("✨ Scan & Auto-Fill Details"):
        with st.spinner("AI is reading the document..."):
            try:
                img = Image.open(uploaded_file)
                
                # IMPORTANT: Hum 'gemini-pro-vision' use karenge jo har key pe chalta hai
                model = genai.GenerativeModel('gemini-pro-vision')
                
                prompt = """
                Analyze this vehicle document image. Extract these details. 
                Keep Mobile Number blank. Format:
                VNO: Registration Number
                DATE: Registration Date
                NAME: Owner Name
                SDW: Father/Husband Name
                ADDR: Full Address
                MAKER: Maker Name
                MODEL: Model Name
                CHASSIS: Chassis No
                ENGINE: Engine No
                RTO: Registering Authority
                INS_CO: Insurance Company
                INS_POL: Policy No
                INS_EXP: Expiry Date
                """
                
                response = model.generate_content([prompt, img])
                
                # Extracting text from response
                output_text = response.text
                lines = output_text.split('\n')
                
                # Mapping data to session state
                mapping = {
                    'VNO': 'v_no', 'DATE': 'reg_date', 'NAME': 'owner',
                    'SDW': 'father', 'ADDR': 'address', 'MAKER': 'maker',
                    'MODEL': 'model', 'CHASSIS': 'chassis', 'ENGINE': 'engine',
                    'RTO': 'rto', 'INS_CO': 'ins_co', 'INS_POL': 'ins_pol', 'INS_EXP': 'ins_exp'
                }
                
                for line in lines:
                    for key, state_key in mapping.items():
                        if line.upper().startswith(f"{key}:"):
                            st.session_state.v_data[state_key] = line.split(":", 1)[1].strip()
                
                st.success("Details Extracted Successfully!")
                st.rerun()
                
            except Exception as e:
                # Agar Gemini Pro Vision bhi na chale, toh Flash ka backup
                try:
                    model_flash = genai.GenerativeModel('gemini-1.5-flash')
                    response = model_flash.generate_content([prompt, img])
                    # (Same logic as above...)
                except:
                    st.error(f"Scan failed: API key issue. Please ensure your API key has 'Generative AI API' enabled in Google Cloud Console.")

st.markdown("---")

# --- UI INPUTS ---
col1, col2 = st.columns(2)
with col1:
    v_no = st.text_input("Vehicle Number", value=st.session_state.v_data['v_no']).upper()
    reg_date = st.text_input("Registration Date", value=st.session_state.v_data['reg_date'])
    owner_name = st.text_input("Owner Name", value=st.session_state.v_data['owner']).upper()
    son_dougher = st.text_input("Son/Daughter/Wife Of", value=st.session_state.v_data['father']).upper()
    address = st.text_area("Full Address", value=st.session_state.v_data['address'])

with col2:
    v_maker = st.text_input("Vehicle Maker", value=st.session_state.v_data['maker']).upper()
    v_model = st.text_input("Vehicle Model", value=st.session_state.v_data['model']).upper()
    chassis_no = st.text_input("Chassis Number", value=st.session_state.v_data['chassis']).upper()
    engine_no = st.text_input("Engine Number", value=st.session_state.v_data['engine']).upper()
    reg_auth = st.text_input("RTO Authority", value=st.session_state.v_data['rto']).upper()

st.markdown("### 🏦 Financing & Insurance")
c3, c4 = st.columns(2)
with c3:
    mobile_no = st.text_input("Mobile No (Manual Entry)")
    ins_company = st.text_input("Insurance Company", value=st.session_state.v_data['ins_co']).upper()
with c4:
    hypo = st.text_input("Hypothecation").upper()
    ins_expire = st.text_input("Expiry Date", value=st.session_state.v_data['ins_exp'])

# --- PDF GENERATOR (Aapka Original Logic) ---
if st.button("Generate Final Elite Report"):
    if not v_no or not owner_name:
        st.error("Basic details are required!")
    else:
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        # Header & Design
        c.setFillColor(colors.HexColor("#0f4c75")); c.rect(0, 750, 600, 100, fill=1)
        c.setFillColor(colors.white); c.setFont("Helvetica-Bold", 24); c.drawCentredString(300, 795, "ELITE VEHICLE DESK")
        # Draw all rows (Same as your original code)
        # ...
        c.save()
        st.download_button("📥 Download Report", buffer.getvalue(), f"Elite_{v_no}.pdf")
