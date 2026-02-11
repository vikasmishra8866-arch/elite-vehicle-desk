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

# --- BINDING YOUR ACTIVE KEY ---
API_KEY = "AIzaSyBCnOvFT835gjOzBntnKRhFf-jqJIEaP0c"
genai.configure(api_key=API_KEY)

# Session State to store values
if 'v_data' not in st.session_state:
    st.session_state.v_data = {
        'v_no': "", 'reg_date': "", 'owner': "", 'father': "",
        'address': "", 'maker': "", 'model': "", 'chassis': "",
        'engine': "", 'rto': "", 'ins_co': "", 'ins_pol': "", 'ins_exp': ""
    }

IST = pytz.timezone('Asia/Kolkata')
current_time = datetime.datetime.now(IST).strftime("%d-%m-%Y %I:%M %p")

st.set_page_config(page_title="ELITE VEHICLE DESK", page_icon="⭐")
st.title("⭐ ELITE VEHICLE DESK")

# --- AI MAGIC SCANNER ---
st.markdown("### 🤖 AI Magic Scanner (Auto-Fill)")
uploaded_file = st.file_uploader("Upload Virtual RC Photo", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    if st.button("✨ Scan & Auto-Fill Details"):
        with st.spinner("AI is analyzing your document..."):
            try:
                img = Image.open(uploaded_file)
                
                # IMPORTANT: Hum latest stable model use kar rahe hain
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = """
                Extract vehicle details from this Virtual RC image. 
                Do NOT extract Mobile Number. Format exactly:
                VNO: [Vehicle Number]
                DATE: [Registration Date]
                NAME: [Owner Name]
                SDW: [Father/Husband Name]
                ADDR: [Full Address]
                MAKER: [Maker Name]
                MODEL: [Model Name]
                CHASSIS: [Chassis No]
                ENGINE: [Engine No]
                RTO: [Registering Authority]
                INS_CO: [Insurance Company]
                INS_POL: [Policy Number]
                INS_EXP: [Insurance Expiry]
                """
                
                response = model.generate_content([prompt, img])
                
                # Data Parsing logic
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
                
                st.success("Scan Complete! Review details below.")
                st.rerun()
                
            except Exception as e:
                st.error(f"Error: {e}")
                st.info("Since you just enabled the API, it might take 2-3 minutes to sync globally. Please try again in a moment.")

st.markdown("---")

# --- UI FORM ---
st.markdown("### 📝 Vehicle & Owner Details")
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

st.markdown("### 🛡️ Insurance & Finance")
c3, c4 = st.columns(2)
with c3:
    mobile_no = st.text_input("Mobile No") 
    ins_company = st.text_input("Insurance Company", value=st.session_state.v_data['ins_co']).upper()
with c4:
    hypo = st.text_input("Hypothecation").upper()
    ins_expire = st.text_input("Expiry Date", value=st.session_state.v_data['ins_exp'])

# --- PDF Logic below... ---
