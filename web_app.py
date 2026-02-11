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

# --- GEMINI AI SETUP (With Your New Key) ---
API_KEY = "AIzaSyBCnOvFT835gjOzBntnKRhFf-jqJIEaP0c"
genai.configure(api_key=API_KEY)

# Session State Initialize (Taki data boxes mein tika rahe)
if 'v_data' not in st.session_state:
    st.session_state.v_data = {
        'v_no': "", 'reg_date': "", 'owner': "", 'father': "",
        'address': "", 'maker': "", 'model': "", 'chassis': "",
        'engine': "", 'rto': "", 'ins_co': "", 'ins_pol': "", 'ins_exp': ""
    }

# --- INDIAN TIME SETTING ---
IST = pytz.timezone('Asia/Kolkata')
current_time = datetime.datetime.now(IST).strftime("%d-%m-%Y %I:%M %p")

st.set_page_config(page_title="ELITE VEHICLE DESK", page_icon="⭐")

st.title("⭐ ELITE VEHICLE DESK")
st.write(f"📅 Report Date: {current_time}")

# --- AI MAGIC SCANNER SECTION ---
st.markdown("---")
st.markdown("### 🤖 AI Magic Scanner (Auto-Fill)")
uploaded_file = st.file_uploader("Upload Virtual RC / Insurance Photo", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    if st.button("✨ Scan & Auto-Fill Details"):
        with st.spinner("AI is reading the document..."):
            try:
                img = Image.open(uploaded_file)
                # Using the stable flash model
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = """
                Extract vehicle details from this image. DO NOT extract Mobile Number. 
                Format the response EXACTLY like this:
                VNO: [Registration Number]
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
                INS_POL: [Insurance Policy No]
                INS_EXP: [Insurance Valid UpTo]
                """
                
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
                
                st.success("Details Extracted! Review them below.")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}. If this is a 404, please wait 2 minutes for the new key to activate.")

st.markdown("---")

# --- INPUT SECTION (Linked with AI Session State) ---
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

st.markdown("### 🏦 Financing & Authority")
c3, c4 = st.columns(2)
with c3:
    hypo = st.text_input("Hypothecation").upper()
    mobile_no = st.text_input("Mobile No") # Manual entry
with c4:
    reg_auth = st.text_input("Registration Authority (RTO)", value=st.session_state.v_data['rto']).upper()

st.markdown("### 🛡️ Insurance Status")
ins1, ins2 = st.columns(2)
with ins1:
    ins_company = st.text_input("Insurance Company", value=st.session_state.v_data['ins_co']).upper()
    ins_policy = st.text_input("Policy Number", value=st.session_state.v_data['ins_pol']).upper()
with ins2:
    ins_expire = st.text_input("Expiry Date", value=st.session_state.v_data['ins_exp'])

# --- PDF GENERATOR (Original Logic) ---
if st.button("Generate Final Elite Report"):
    if not v_no or not owner_name:
        st.error("Please fill required details!")
    else:
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        
        # Watermark
        c.saveState()
        c.setFont("Helvetica-Bold", 60); c.setStrokeColor(colors.lightgrey)
        c.setFillColor(colors.lightgrey, alpha=0.1); c.translate(300, 400)
        c.rotate(45); c.drawCentredString(0, 0, "ELITE VEHICLE DESK"); c.restoreState()
        
        # Header
        c.setFillColor(colors.HexColor("#0f4c75")); c.rect(0, 750, 600, 100, fill=1)
        c.setFillColor(colors.white); c.setFont("Helvetica-Bold", 26)
        c.drawCentredString(300, 795, "ELITE VEHICLE DESK")
        c.setFont("Helvetica-Bold", 12); c.drawCentredString(300, 775, "Official Vehicle Verification & Insurance Report")
        
        c.setFillColor(colors.black); c.setFont("Helvetica-Bold", 10)
        c.drawString(50, 730, f"REPORT GENERATED ON: {current_time}"); c.line(50, 720, 540, 720)

        y = 690
        def draw_row(label, value, y_pos):
            c.setFont("Helvetica-Bold", 10); c.drawString(60, y_pos, f"{label}:")
            c.setFont("Helvetica", 10)
            if label == "ADDRESS":
                maxWidth = 320 
                text_lines = simpleSplit(str(value).upper(), "Helvetica", 10, maxWidth)
                for line in text_lines:
                    c.drawString(200, y_pos, line); y_pos -= 15 
                return y_pos - 5 
            else:
                c.drawString(200, y_pos, str(value).upper() if value else "N/A")
                return y_pos - 20

        # Section: Vehicle
        c.setFillColor(colors.HexColor("#0f4c75")); c.rect(50, y, 490, 20, fill=1)
        c.setFillColor(colors.white); c.setFont("Helvetica-Bold", 11); c.drawString(60, y+5, "VEHICLE INFORMATION"); y -= 25
        c.setFillColor(colors.black)
        
        c.setFont("Helvetica-Bold", 10); c.drawString(60, y, "VEHICLE NO:"); c.setFont("Helvetica", 10); c.drawString(200, y, v_no)
        c.setFont("Helvetica-Bold", 10); c.drawString(360, y, "MOBILE NO:"); c.setFont("Helvetica", 10); c.drawString(450, y, mobile_no if mobile_no else "N/A")
        y -= 20

        y = draw_row("REG. DATE", reg_date, y)
        y = draw_row("OWNER NAME", owner_name, y)
        y = draw_row("S/D/W OF", son_dougher, y)
        y = draw_row("ADDRESS", address, y)
        y = draw_row("VEHICLE MAKER", v_maker, y)
        y = draw_row("VEHICLE MODEL", v_model, y)
        y = draw_row("CHASSIS NO", chassis_no, y)
        y = draw_row("ENGINE NO", engine_no, y)
        y = draw_row("HYPOTHECATION", hypo, y)
        y = draw_row("REG. AUTHORITY", reg_auth, y)

        # Section: Insurance
        y -= 10; c.setFillColor(colors.HexColor("#0f4c75")); c.rect(50, y, 490, 20, fill=1)
        c.setFillColor(colors.white); c.drawString(60, y+5, "INSURANCE DETAILS"); y -= 25
        c.setFillColor(colors.black)
        y = draw_row("COMPANY NAME", ins_company, y)
        y = draw_row("POLICY NO", ins_policy, y)
        y = draw_row("EXPIRY DATE", ins_expire, y)

        # QR Code
        qr_content = f"Vehicle No: {v_no}\nOwner: {owner_name}\nChassis: {chassis_no}"
        qr = qrcode.make(qr_content); qr.save("temp_qr.png")
        c.drawImage("temp_qr.png", 450, 100, width=85, height=85)
        c.setFont("Helvetica-Bold", 7); c.drawString(455, 90, "Scan for Full Details")
        
        c.line(50, 80, 540, 80)
        c.setFont("Helvetica-Bold", 11); c.drawString(50, 65, "ELITE VEHICLE DESK"); c.drawRightString(540, 65, "Authorized Signatory")
        
        c.save()
        st.success("Report Generated!")
        st.download_button("📥 Download Official PDF", buffer.getvalue(), f"Elite_Report_{v_no}.pdf", "application/pdf")
