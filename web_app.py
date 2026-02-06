import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.utils import simpleSplit # Address wrap karne ke liye
import datetime
import io
import pytz 
import qrcode 

# --- INDIAN TIME SETTING ---
IST = pytz.timezone('Asia/Kolkata')
current_time = datetime.datetime.now(IST).strftime("%d-%m-%Y %I:%M %p")

# Page Setup
st.set_page_config(page_title="ELITE VEHICLE DESK", page_icon="⭐")

# --- UI DESIGN ---
st.title("⭐ ELITE VEHICLE DESK")
st.write(f"📅 Date: {current_time}")

# --- INPUT SECTION ---
st.markdown("### 📝 Enter Vehicle Information")
col1, col2 = st.columns(2)

with col1:
    v_no = st.text_input("Vehicle Number").upper()
    reg_date = st.text_input("Registration Date")
    owner_name = st.text_input("Owner Name").upper()
    address = st.text_area("Full Address")
    mobile_no = st.text_input("Mobile No")

with col2:
    v_maker = st.text_input("Vehicle Maker").upper()
    v_model = st.text_input("Vehicle Model").upper()
    chassis_no = st.text_input("Chassis Number").upper()
    engine_no = st.text_input("Engine Number").upper()
    hypo = st.text_input("Hypothecation").upper()
    reg_auth = st.text_input("Registration Authority (RTO)").upper()

st.markdown("---")
st.markdown("### 🛡️ Insurance Details")
ins_col1, ins_col2 = st.columns(2)
with ins_col1:
    ins_company = st.text_input("Insurance Company").upper()
    ins_policy = st.text_input("Policy Number").upper()
with ins_col2:
    ins_expire = st.text_input("Expiry Date")

# --- PDF GENERATOR ---
if st.button("Generate Final Elite Report"):
    if not v_no or not owner_name:
        st.error("Please fill required details!")
    else:
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        
        # --- HEADER ---
        c.setFillColor(colors.HexColor("#0f4c75"))
        c.rect(0, 750, 600, 100, fill=1)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 26)
        c.drawCentredString(300, 795, "ELITE VEHICLE DESK")
        c.setFont("Helvetica-Oblique", 11)
        c.drawCentredString(300, 778, "Premium Vehicle Information & Documentation Services")
        
        # --- BODY ---
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, 730, f"REPORT GENERATED ON: {current_time}")
        c.line(50, 720, 540, 720)

        # Single Heading Layout
        y = 700
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "VEHICLE DETAILS:")
        c.line(50, y-5, 160, y-5)
        y -= 25

        def draw_row(label, value, y_pos):
            c.setFont("Helvetica-Bold", 10)
            c.drawString(60, y_pos, f"{label}:")
            c.setFont("Helvetica", 10)
            
            # Address Wrap Logic
            if label == "ADDRESS":
                lines = simpleSplit(str(value).upper(), "Helvetica", 10, 330)
                for line in lines:
                    c.drawString(200, y_pos, line)
                    y_pos -= 15
                return y_pos - 5
            else:
                c.drawString(200, y_pos, str(value).upper() if value else "N/A")
                return y_pos - 20

        # Ordered Details
        y = draw_row("VEHICLE NO", v_no, y)
        y = draw_row("REG. DATE", reg_date, y)
        y = draw_row("OWNER NAME", owner_name, y)
        y = draw_row("ADDRESS", address, y)
        y = draw_row("MOBILE NO", mobile_no, y)
        y = draw_row("VEHICLE MAKER", v_maker, y)
        y = draw_row("VEHICLE MODEL", v_model, y)
        y = draw_row("CHASSIS NO", chassis_no, y)
        y = draw_row("ENGINE NO", engine_no, y)
        y = draw_row("HYPOTHECATION", hypo, y)
        y = draw_row("REG. AUTHORITY", reg_auth, y) # Shifted here

        # --- INSURANCE ---
        y -= 15
        c.setFillColor(colors.HexColor("#f2f2f2"))
        c.rect(50, y, 490, 20, fill=1)
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(300, y+6, "INSURANCE INFORMATION")
        
        y -= 30
        y = draw_row("COMPANY NAME", ins_company, y)
        y = draw_row("POLICY NO", ins_policy, y)
        y = draw_row("EXPIRY DATE", ins_expire, y)

        # --- QR CODE ---
        qr_data = f"Vehicle: {v_no}\nOwner: {owner_name}\nChassis: {chassis_no}\nVerify: https://parivahan.gov.in/"
        qr = qrcode.make(qr_data)
        qr.save("temp_qr.png")
        c.drawImage("temp_qr.png", 450, 140, width=80, height=80)
        c.setFont("Helvetica-Oblique", 7)
        c.drawString(455, 130, "Scan for Verification")

        # --- FOOTER ---
        c.line(50, 110, 540, 110)
        c.setFont("Helvetica-Bold", 12)
        c.drawRightString(540, 90, "Authorized Signatory")
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, 90, "ELITE VEHICLE DESK")
        
        # New Professional Disclaimer
        c.setFont("Helvetica", 8)
        c.drawString(50, 70, "DECLARATION: This document is a digital record generated for informational purposes only.")
        c.drawString(50, 60, "The data presented is subject to verification with the original Vahan Registry/mParivahan database.")

        c.save()
        st.success("Premium Report Fixed & Generated!")
        st.download_button("📥 Download Final PDF", buffer.getvalue(), f"Elite_Report_{v_no}.pdf", "application/pdf")
