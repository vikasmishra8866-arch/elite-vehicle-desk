import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.utils import simpleSplit 
import datetime
import io
import pytz 
import qrcode 

# --- INDIAN TIME SETTING ---
IST = pytz.timezone('Asia/Kolkata')
current_time = datetime.datetime.now(IST).strftime("%d-%m-%Y %I:%M %p")

st.set_page_config(page_title="ELITE VEHICLE DESK", page_icon="⭐")

st.title("⭐ ELITE VEHICLE DESK")
st.write(f"📅 Report Date: {current_time}")

# --- INPUT SECTION ---
st.markdown("### 📝 Vehicle & Owner Details")
col1, col2 = st.columns(2)
with col1:
    v_no = st.text_input("Vehicle Number").upper()
    reg_date = st.text_input("Registration Date")
    owner_name = st.text_input("Owner Name").upper()
    address = st.text_area("Full Address")
with col2:
    v_maker = st.text_input("Vehicle Maker").upper()
    v_model = st.text_input("Vehicle Model").upper()
    chassis_no = st.text_input("Chassis Number").upper()
    engine_no = st.text_input("Engine Number").upper()

st.markdown("### 🏦 Financing & Authority")
c3, c4 = st.columns(2)
with c3:
    hypo = st.text_input("Hypothecation").upper()
    mobile_no = st.text_input("Mobile No")
with c4:
    reg_auth = st.text_input("Registration Authority (RTO)").upper()

st.markdown("### 🛡️ Insurance Status")
ins1, ins2 = st.columns(2)
with ins1:
    ins_company = st.text_input("Insurance Company").upper()
    ins_policy = st.text_input("Policy Number").upper()
with ins_2:
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
        c.setFont("Helvetica-Oblique", 12)
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
                lines = simpleSplit(str(value).upper(), "Helvetica", 10, 320)
                for line in lines:
                    c.drawString(200, y_pos, line)
                    y_pos -= 15
                return y_pos - 5
            else:
                c.drawString(200, y_pos, str(value).upper() if value else "N/A")
                return y_pos - 20

        # VEHICLE DATA SECTION
        c.setFillColor(colors.HexColor("#eef2f3"))
        c.rect(50, y, 490, 20, fill=1)
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(60, y+5, "VEHICLE INFORMATION")
        y -= 25

        y = draw_row("VEHICLE NO", v_no, y)
        y = draw_row("REG. DATE", reg_date, y)
        y = draw_row("OWNER NAME", owner_name, y)
        y = draw_row("ADDRESS", address, y)
        y = draw_row("MOBILE NO", mobile_no, y)
        y = draw_row("MAKER/MODEL", f"{v_maker} / {v_model}", y)
        y = draw_row("CHASSIS NO", chassis_no, y)
        y = draw_row("ENGINE NO", engine_no, y)
        y = draw_row("HYPOTHECATION", hypo, y)
        y = draw_row("REG. AUTHORITY", reg_auth, y)

        # INSURANCE SECTION
        y -= 10
        c.setFillColor(colors.HexColor("#eef2f3"))
        c.rect(50, y, 490, 20, fill=1)
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(60, y+5, "INSURANCE DETAILS")
        y -= 25

        y = draw_row("COMPANY NAME", ins_company, y)
        y = draw_row("POLICY NO", ins_policy, y)
        y = draw_row("EXPIRY DATE", ins_expire, y)

        # QR CODE & FOOTER
        qr_data = f"Vehicle: {v_no}\nOwner: {owner_name}\nVerify: https://parivahan.gov.in/"
        qr = qrcode.make(qr_data)
        qr.save("temp_qr.png")
        c.drawImage("temp_qr.png", 450, 150, width=80, height=80)
        
        c.line(50, 110, 540, 110)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(50, 95, "ELITE VEHICLE DESK")
        c.drawRightString(540, 95, "Authorized Signatory")
        
        c.setFont("Helvetica", 8)
        c.drawString(50, 75, "IMPORTANT: This is a digital report generated for informational purposes.")
        c.drawString(50, 65, "The data is subject to verification with original Vahan Registry/mParivahan records.")

        c.save()
        st.success("Premium Report Fixed!")
        st.download_button("📥 Download Official PDF", buffer.getvalue(), f"Elite_Report_{v_no}.pdf", "application/pdf")
