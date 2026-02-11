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
# Aapki active key maine yahan set kar di hai
API_KEY = "AIzaSyBCnOvFT835gjOzBntnKRhFf-jqJIEaP0c"
genai.configure(api_key=API_KEY)

# Session State (Taki scan ke baad data gayab na ho)
if 'v_data' not in st.session_state:
    st.session_state.v_data = {
        'v_no': "", 'reg_date': "", 'owner': "", 'father': "",
        'address': "", 'maker': "", 'model': "", 'chassis': "",
        'engine': "", 'rto': "", 'ins_co': "", 'ins_pol': "", 'ins_exp': ""
    }

IST = pytz.timezone('Asia/Kolkata')
current_time = datetime.datetime.now(IST).strftime("%d-%m-%Y %I:%M %p")

st.set_page_config(page_title="ELITE VEHICLE DESK", page_icon="⭐", layout="wide")
st.title("⭐ ELITE VEHICLE DESK")

# --- AI MAGIC SCANNER ---
st.markdown("### 🤖 AI Magic Scanner")
uploaded_file = st.file_uploader("Upload Virtual RC Image", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    if st.button("✨ Scan & Auto-Fill"):
        with st.spinner("AI is reading the document..."):
            try:
                img = Image.open(uploaded_file)
                # FIX: Using the most stable model name for Free Tier API
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = """Extract details from this RC image. Format:
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
                INS_POL: Policy Number
                INS_EXP: Insurance Valid UpTo"""
                
                response = model.generate_content([prompt, img])
                lines = response.text.split('\n')
                
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
                
                st.success("Details Extracted!")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}. Please ensure API key is active.")

st.divider()

# --- FORM SECTION ---
col1, col2 = st.columns(2)
with col1:
    v_no = st.text_input("Vehicle Number", value=st.session_state.v_data['v_no']).upper()
    owner_name = st.text_input("Owner Name", value=st.session_state.v_data['owner']).upper()
    son_dougher = st.text_input("Son/Daughter/Wife Of", value=st.session_state.v_data['father']).upper()
    address = st.text_area("Full Address", value=st.session_state.v_data['address'])
    chassis_no = st.text_input("Chassis Number", value=st.session_state.v_data['chassis']).upper()

with col2:
    v_maker = st.text_input("Vehicle Maker", value=st.session_state.v_data['maker']).upper()
    v_model = st.text_input("Vehicle Model", value=st.session_state.v_data['model']).upper()
    reg_date = st.text_input("Registration Date", value=st.session_state.v_data['reg_date'])
    reg_auth = st.text_input("RTO Authority", value=st.session_state.v_data['rto']).upper()
    engine_no = st.text_input("Engine Number", value=st.session_state.v_data['engine']).upper()

st.divider()

# Finance & Extra Fields
c3, c4 = st.columns(2)
with c3:
    mobile_no = st.text_input("Mobile Number") # Manual entry as you requested
    ins_company = st.text_input("Insurance Company", value=st.session_state.v_data['ins_co']).upper()
with c4:
    hypo = st.text_input("Hypothecation").upper()
    ins_expire = st.text_input("Insurance Expiry", value=st.session_state.v_data['ins_exp'])

# --- PDF GENERATOR (Aapka original logic) ---
if st.button("Generate Final Elite Report"):
    if not v_no:
        st.error("Vehicle Number is required!")
    else:
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        
        # Design & Header
        c.setFillColor(colors.HexColor("#0f4c75")); c.rect(0, 750, 600, 100, fill=1)
        c.setFillColor(colors.white); c.setFont("Helvetica-Bold", 24)
        c.drawCentredString(300, 795, "ELITE VEHICLE DESK")
        
        # Details Drawing logic...
        c.setFillColor(colors.black); c.setFont("Helvetica", 10)
        y = 720
        c.drawString(50, y, f"REPORT DATE: {current_time}"); y -= 30
        
        # QR Code for Address
        qr_data = f"Owner: {owner_name}\nAddress: {address}"
        qr = qrcode.make(qr_data); qr.save("temp_qr.png")
        c.drawImage("temp_qr.png", 450, 50, width=100, height=100)
        
        c.save()
        st.success("PDF Generated!")
        st.download_button("📥 Download PDF", buffer.getvalue(), f"Elite_{v_no}.pdf")
