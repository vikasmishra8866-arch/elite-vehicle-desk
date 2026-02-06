import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import datetime
import io
import pytz 
import qrcode # QR Code banane ke liye

# --- INDIAN TIME SETTING ---
IST = pytz.timezone('Asia/Kolkata')
current_time = datetime.datetime.now(IST).strftime("%d-%m-%Y %I:%M %p")

# Page Setup
st.set_page_config(page_title="ELITE VEHICLE DESK", page_icon="⭐")

# --- UI DESIGN ---
st.title("⭐ ELITE VEHICLE DESK")
st.subheader("Official Vehicle Verification & Insurance Record")
st.write(f"📅 Date & Time: {current_time}")

# --- INPUT SECTION ---
st.markdown("### 🚗 Vehicle Registration Details")
col1, col2 = st.columns(2)

with col1:
    v_no = st.text_input("Vehicle Number", placeholder="e.g. GJ-05-XX-1234").upper()
    reg_date = st.text_input("Registration Date", placeholder="DD-MM-YYYY")
    owner_name = st.text_input("Owner Name").upper()
    address = st.text_area("Address")

with col2:
    chassis_no = st.text_input("Chassis Number").upper()
    engine_no = st.text_input("Engine Number").upper()
    v_maker = st.text_input("Vehicle Maker").upper()
    v_model = st.text_input("Vehicle Model").upper()

col3, col4 = st.columns(2)
with col3:
    mobile_no = st.text_input("Registered Mobile No")
with col4:
    hypo = st.text_input("Hypothecation").upper()

# --- INSURANCE SECTION ---
st.markdown("---")
st.markdown("### 🛡️ Insurance & Authority Details")
ins_col1, ins_col2 = st.columns(2)
with ins_col1:
    ins_company = st.text_input("Insurance Company Name").upper()
    ins_policy = st.text_input("Insurance Policy No").upper()
with ins_col2:
    ins_expire = st.text_input("Insurance Expiry Date", placeholder="DD-MM-YYYY")
    reg_auth = st.text_input("Registration Authority").upper()

# --- PDF GENERATOR ---
if st.button("Generate ELITE Vehicle Report"):
    if not v_no or not owner_name:
        st.error("Please enter Vehicle Number and Owner Name!")
    else:
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        
        # --- HEADER DESIGN ---
        c.setFillColor(colors.HexColor("#0f4c75")) # Dark Blue
        c.rect(0, 750, 600, 100, fill=1)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 26)
        c.drawCentredString(300, 795, "ELITE VEHICLE DESK")
        c.setFont("Helvetica-Oblique", 12)
        c.drawCentredString(300, 775, "Official Vehicle Verification & Insurance Report")
        
        # --- BODY ---
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(50, 725, f"REPORT GENERATED ON: {current_time}")
        c.line(50, 715, 540, 715)

        y = 690
        def draw_detail(label, value, y_pos, x_indent=60):
            c.setFont("Helvetica-Bold", 10)
            c.drawString(x_indent, y_pos, f"{label}:")
            c.setFont("Helvetica", 10)
            val_text = str(value) if value else "N/A"
            c.drawString(x_indent + 140, y_pos, val_text)
            return y_pos - 20 # Thodi spacing kam ki for more compact look

        # Two-column layout for details
        start_y = 690
        left_x_indent = 50
        right_x_indent = 300 # Right column ka start

        current_y_left = start_y
        current_y_right = start_y

        # Vehicle Details (Left Column)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(left_x_indent, current_y_left, "VEHICLE DETAILS:")
        current_y_left -= 20
        current_y_left = draw_detail("VEHICLE NO", v_no, current_y_left, left_x_indent)
        current_y_left = draw_detail("REG. DATE", reg_date, current_y_left, left_x_indent)
        current_y_left = draw_detail("OWNER NAME", owner_name, current_y_left, left_x_indent)
        current_y_left = draw_detail("ADDRESS", address, current_y_left, left_x_indent)
        current_y_left = draw_detail("REG. MOBILE", mobile_no, current_y_left, left_x_indent)
        current_y_left = draw_detail("HYPOTHECATION", hypo, current_y_left, left_x_indent)
        
        # Engine/Chassis (Right Column)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(right_x_indent, current_y_right, "TECHNICAL DETAILS:")
        current_y_right -= 20
        current_y_right = draw_detail("CHASSIS NO", chassis_no, current_y_right, right_x_indent)
        current_y_right = draw_detail("ENGINE NO", engine_no, current_y_right, right_x_indent)
        current_y_right = draw_detail("MAKER", v_maker, current_y_right, right_x_indent)
        current_y_right = draw_detail("MODEL", v_model, current_y_right, right_x_indent)

        # Ensure both columns end at roughly the same height, or use max_y
        max_y_after_details = min(current_y_left, current_y_right) - 20
        
        # --- INSURANCE SUB-SECTION ---
        y = max_y_after_details
        c.setFillColor(colors.HexColor("#e0e0e0")) # Light Grey Bar
        c.rect(50, y, 490, 20, fill=1)
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 11)
        c.drawCentredString(300, y+5, "INSURANCE & REGISTRATION AUTHORITY")
        
        y -= 30
        c.setFont("Helvetica-Bold", 10)
        c.drawString(60, y, f"COMPANY NAME:")
        c.setFont("Helvetica", 10)
        c.drawString(200, y, ins_company if ins_company else "N/A")
        
        c.setFont("Helvetica-Bold", 10)
        c.drawString(60, y-20, f"POLICY NO:")
        c.setFont("Helvetica", 10)
        c.drawString(200, y-20, ins_policy if ins_policy else "N/A")
        
        c.setFont("Helvetica-Bold", 10)
        c.drawString(60, y-40, f"EXPIRY DATE:")
        c.setFont("Helvetica", 10)
        c.drawString(200, y-40, ins_expire if ins_expire else "N/A")

        c.setFont("Helvetica-Bold", 10)
        c.drawString(300, y-20, f"REG. AUTHORITY:")
        c.setFont("Helvetica", 10)
        c.drawString(440, y-20, reg_auth if reg_auth else "N/A")
        
        # --- QR CODE GENERATION ---
        qr_data = (
            f"Vehicle No: {v_no}\n"
            f"Reg Date: {reg_date}\n"
            f"Owner: {owner_name}\n"
            f"Chassis No: {chassis_no}\n"
            f"Engine No: {engine_no}\n"
            f"Verify on mParivahan: https://parivahan.gov.in/parivahan/"
        )
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=3, # QR code ka size
            border=2,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
        # QR Code ko PDF mein daalna
        qr_img_path = "temp_qr.png"
        qr_img.save(qr_img_path)
        c.drawImage(qr_img_path, 450, 150, width=80, height=80) # Position adjust karein
        
        c.setFont("Helvetica-Oblique", 7)
        c.drawString(450, 135, "Scan for Details & mParivahan")

        # --- FOOTER ---
        c.line(50, 100, 540, 100)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(50, 80, "ELITE VEHICLE DESK")
        c.drawRightString(540, 80, "Authorized Signatory")
        c.setFont("Helvetica-Oblique", 8)
        c.drawString(50, 60, "* This report is based on information provided by the user.")
        c.drawString(50, 50, "For official verification, please refer to government records.")

        c.save()
        st.success("ELITE Vehicle Report Generated with QR Code!")
        st.download_button("📥 Download Elite PDF Report", buffer.getvalue(), f"Elite_Report_{v_no}.pdf", "application/pdf")
