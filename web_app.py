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

# --- GEMINI AI SETUP ---
API_KEY = "AIzaSyCodTmsjFLl_MFgahtATwfWmhuAI-dIxzs"
genai.configure(api_key=API_KEY)

# --- INDIAN TIME SETTING ---
IST = pytz.timezone('Asia/Kolkata')
current_time = datetime.datetime.now(IST).strftime("%d-%m-%Y %I:%M %p")

st.set_page_config(page_title="ELITE VEHICLE DESK", page_icon="⭐")

st.title("⭐ ELITE VEHICLE DESK")
st.write(f"📅 Report Date: {current_time}")

# --- NEW: AI MAGIC SCANNER SECTION ---
st.markdown("---")
st.markdown("### 🤖 AI Magic Scanner (Auto-Fill)")
uploaded_file = st.file_uploader("Upload Vehicle Document (RC/Insurance Photo) for Auto-Fill", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    if st.button("✨ Scan & Auto-Fill Details"):
        with st.spinner("AI is reading the document..."):
            try:
                img = Image.open(uploaded_file)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Prompt to extract details
                prompt = """
                Extract the following vehicle details from this image. 
                Return the data in this exact format:
                Vehicle Number: [value]
                Registration Date: [value]
                Owner Name: [value]
                Father Name: [value]
                Address: [value]
                Maker: [value]
                Model: [value]
                Chassis Number: [value]
                Engine Number: [value]
                RTO: [value]
                """
                
                response = model.generate_content([prompt, img])
                lines = response.text.split('\n')
                
                # Dictionary to store extracted data
                extracted_data = {}
                for line in lines:
                    if ":" in line:
                        key, val = line.split(":", 1)
                        extracted_data[key.strip()] = val.strip()

                # Updating Session State for Auto-Fill
                st.session_state['v_no'] = extracted_data.get('Vehicle Number', "")
                st.session_state['reg_date'] = extracted_data.get('Registration Date', "")
                st.session_state['owner'] = extracted_data.get('Owner Name', "")
                st.session_state['father'] = extracted_data.get('Father Name', "")
                st.session_state['address'] = extracted_data.get('Address', "")
                st.session_state['maker'] = extracted_data.get('Maker', "")
                st.session_state['model'] = extracted_data.get('Model', "")
                st.session_state['chassis'] = extracted_data.get('Chassis Number', "")
                st.session_state['engine'] = extracted_data.get('Engine Number', "")
                st.session_state['rto'] = extracted_data.get('RTO', "")
                
                st.success("Details Extracted Successfully! Check the boxes below.")
            except Exception as e:
                st.error(f"AI could not read the image: {e}")

st.markdown("---")

# --- INPUT SECTION (Linked with AI Session State) ---
st.markdown("### 📝 Vehicle & Owner Details")
col1, col2 = st.columns(2)
with col1:
    v_no = st.text_input("Vehicle Number", value=st.session_state.get('v_no', "")).upper()
    reg_date = st.text_input("Registration Date", value=st.session_state.get('reg_date', ""))
    owner_name = st.text_input("Owner Name", value=st.session_state.get('owner', "")).upper()
    son_dougher = st.text_input("Son/Daughter/Wife Of", value=st.session_state.get('father', "")).upper() 
    address = st.text_area("Full Address", value=st.session_state.get('address', ""))
with col2:
    v_maker = st.text_input("Vehicle Maker", value=st.session_state.get('maker', "")).upper()
    v_model = st.text_input("Vehicle Model", value=st.session_state.get('model', "")).upper()
    chassis_no = st.text_input("Chassis Number", value=st.session_state.get('chassis', "")).upper()
    engine_no = st.text_input("Engine Number", value=st.session_state.get('engine', "")).upper()

st.markdown("### 🏦 Financing & Authority")
c3, c4 = st.columns(2)
with c3:
    hypo = st.text_input("Hypothecation").upper()
    mobile_no = st.text_input("Mobile No")
with c4:
    reg_auth = st.text_input("Registration Authority (RTO)", value=st.session_state.get('rto', "")).upper()

st.markdown("### 🛡️ Insurance Status")
ins1, ins2 = st.columns(2)
with ins1:
    ins_company = st.text_input("Insurance Company").upper()
    ins_policy = st.text_input("Policy Number").upper()
with ins2:
    ins_expire = st.text_input("Expiry Date")

# --- PDF GENERATOR (SAME AS ORIGINAL) ---
if st.button("Generate Final Elite Report"):
    if not v_no or not owner_name:
        st.error("Please fill required details!")
    else:
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        
        # --- WATERMARK ---
        c.saveState()
        c.setFont("Helvetica-Bold", 60)
        c.setStrokeColor(colors.lightgrey)
        c.setFillColor(colors.lightgrey, alpha=0.1)
        c.translate(300, 400)
        c.rotate(45)
        c.drawCentredString(0, 0, "ELITE VEHICLE DESK")
        c.restoreState()
        
        # --- HEADER ---
        c.setFillColor(colors.HexColor("#0f4c75"))
        c.rect(0, 750, 600, 100, fill=1)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 26)
        c.drawCentredString(300, 795, "ELITE VEHICLE DESK")
        c.setFont("Helvetica-Bold", 12) 
        c.drawCentredString(300, 775, "Official Vehicle Verification & Insurance Report")
        
        # --- BODY ---
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, 730, f"REPORT GENERATED ON: {current_time}")
        c.line(50, 720, 540, 720)

        y = 690
        def draw_row(label, value, y_pos):
            c.setFont("Helvetica-Bold", 10)
            c.drawString(60, y_pos, f"{label}:")
            c.setFont("Helvetica", 10)
            
            if label == "ADDRESS":
                maxWidth = 320 
                text_lines = simpleSplit(str(value).upper(), "Helvetica", 10, maxWidth)
                for line in text_lines:
                    c.drawString(200, y_pos, line)
                    y_pos -= 15 
                return y_pos - 5 
            else:
                c.drawString(200, y_pos, str(value).upper() if value else "N/A")
                return y_pos - 20

        # SECTION: VEHICLE
        c.setFillColor(colors.HexColor("#0f4c75"))
        c.rect(50, y, 490, 20, fill=1)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(60, y+5, "VEHICLE INFORMATION")
        y -= 25

        c.setFillColor(colors.black)
        
        # --- SIDE-BY-SIDE VEHICLE & MOBILE NO ---
        c.setFont("Helvetica-Bold", 10)
        c.drawString(60, y, "VEHICLE NO:")
        c.setFont("Helvetica", 10)
        c.drawString(200, y, v_no)
        
        c.setFont("Helvetica-Bold", 10)
        c.drawString(360, y, "MOBILE NO:")
        c.setFont("Helvetica", 10)
        c.drawString(450, y, mobile_no if mobile_no else "N/A")
        y -= 20

        y = draw_row("REG. DATE", reg_date, y)
        y = draw_row("OWNER NAME", owner_name, y)
        y = draw_row("SON/DAUGHTER/WIFE OF", son_dougher, y) 
        y = draw_row("ADDRESS", address, y) 
        
        y = draw_row("VEHICLE MAKER", v_maker, y)
        y = draw_row("VEHICLE MODEL", v_model, y)
        y = draw_row("CHASSIS NO", chassis_no, y)
        y = draw_row("ENGINE NO", engine_no, y)
        y = draw_row("HYPOTHECATION", hypo, y)
        y = draw_row("REG. AUTHORITY", reg_auth, y)

        # SECTION: INSURANCE
        y -= 10
        c.setFillColor(colors.HexColor("#0f4c75"))
        c.rect(50, y, 490, 20, fill=1)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(60, y+5, "INSURANCE DETAILS")
        y -= 25

        c.setFillColor(colors.black)
        y = draw_row("COMPANY NAME", ins_company, y)
        y = draw_row("POLICY NO", ins_policy, y)
        y = draw_row("EXPIRY DATE", ins_expire, y)

        # --- QR CODE CONTENT ---
        qr_content = (
            f"ELITE VEHICLE DESK REPORT\n"
            f"--------------------------\n"
            f"Vehicle No: {v_no}\n"
            f"Owner Name: {owner_name}\n"
            f"S/D/W Of: {son_dougher}\n"
            f"Chassis No: {chassis_no}\n"
            f"Engine No: {engine_no}\n\n"
            f"Verify on mParivahan:\n"
            f"https://parivahan.gov.in/parivahan/"
        )
        qr = qrcode.make(qr_content)
        qr.save("temp_qr.png")
        c.drawImage("temp_qr.png", 450, 100, width=85, height=85)
        c.setFont("Helvetica-Bold", 7)
        c.drawString(455, 90, "Scan for Full Details")
        
        # FOOTER
        c.line(50, 80, 540, 80)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(50, 65, "ELITE VEHICLE DESK")
        c.drawRightString(540, 65, "Authorized Signatory")
        
        c.setFont("Helvetica-Oblique", 8)
        c.drawString(50, 45, "NOTE: This document is an electronically generated summary for quick verification.")
        c.drawString(50, 35, "Final status should be confirmed with official mParivahan/RTO government portals.")

        c.save()
        st.success("Report Generated!")
        st.download_button("📥 Download Official PDF", buffer.getvalue(), f"Elite_Report_{v_no}.pdf", "application/pdf")
