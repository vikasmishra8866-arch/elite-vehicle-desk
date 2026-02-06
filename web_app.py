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
    mobile_no = st.text_input("Mobile No") 
    reg_date = st.text_input("Registration Date")
    owner_name = st.text_input("Owner Name").upper()
    son_dougher = st.text_input("Son/Daughter/Wife Of").upper()
    address = st.text_area("Full Address")
with col2:
    v_maker = st.text_input("Vehicle Maker").upper()
    v_model = st.text_input("Vehicle Model").upper()
    chassis_no = st.text_input("Chassis Number").upper()
    engine_no = st.text_input("Engine Number").upper()
    hypo = st.text_input("Hypothecation").upper()
    reg_auth = st.text_input("Registration Authority (RTO)").upper()

st.markdown("### 🛡️ Insurance Status")
ins1, ins2 = st.columns(2)
with ins1:
    ins_company = st.text_input("Insurance Company").upper()
    ins_policy = st.text_input("Policy Number").upper()
with ins2:
    ins_expire = st.text_input("Expiry Date")

# --- PDF GENERATOR ---
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

        # Modified draw_row to handle side-by-side Mobile No
        def draw_row(label, value, y_pos, extra_label=None, extra_value=None):
            c.setFont("Helvetica-Bold", 10)
            c.drawString(60, y_pos, f"{label}:")
            c.setFont("Helvetica", 10)
            c.drawString(180, y_pos, str(value).upper() if value else "N/A")
            
            # Agar extra field (Mobile No) dena hai toh:
            if extra_label and extra_value:
                c.setFont("Helvetica-Bold", 10)
                c.drawString(350, y_pos, f"{extra_label}:")
                c.setFont("Helvetica", 10)
                c.drawString(450, y_pos, str(extra_value).upper() if extra_value else "N/A")
            
            return y_pos - 20

        # SECTION: VEHICLE
        c.setFillColor(colors.HexColor("#0f4c75"))
        c.rect(50, y, 490, 20, fill=1)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(60, y+5, "VEHICLE INFORMATION")
        y -= 25

        c.setFillColor(colors.black)
        # Yahan Vehicle No aur Mobile No ek saath print honge
        y = draw_row("VEHICLE NO", v_no, y, "MOBILE NO", mobile_no) 
        y = draw_row("REG. DATE", reg_date, y)
        y = draw_row("OWNER NAME", owner_name, y)
        y = draw_row("SON/DAUGHTER/WIFE OF", son_dougher, y)
        
        # Address multi-line fix
        c.setFont("Helvetica-Bold", 10)
        c.drawString(60, y, "ADDRESS:")
        c.setFont("Helvetica", 10)
        maxWidth = 350 
        text_lines = simpleSplit(str(address).upper(), "Helvetica", 10, maxWidth)
        for line in text_lines:
            c.drawString(180, y, line)
            y -= 15
        y -= 5

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

        # --- QR CODE ---
        qr_content = f"Vehicle No: {v_no}\nOwner: {owner_name}\nMobile: {mobile_no}"
        qr = qrcode.make(qr_content)
        qr.save("temp_qr.png")
        c.drawImage("temp_qr.png", 450, 85, width=80, height=80)
        
        # FOOTER
        c.line(50, 75, 540, 75)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(50, 60, "ELITE VEHICLE DESK")
        c.drawRightString(540, 60, "Authorized Signatory")

        c.save()
        st.success("Elite Report Updated with Side-by-Side Layout!")
        st.download_button("📥 Download Official PDF", buffer.getvalue(), f"Elite_Report_{v_no}.pdf", "application/pdf")
