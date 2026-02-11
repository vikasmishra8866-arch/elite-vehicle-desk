import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# --- API SETUP ---
API_KEY = "AIzaSyBCnOvFT835gjOzBntnKRhFf-jqJIEaP0c"

# FORCE STABLE VERSION: Ye line 404 error khatam kar degi
genai.configure(api_key=API_KEY)

# --- APP UI ---
st.set_page_config(page_title="ELITE VEHICLE DESK", layout="wide")
st.title("⭐ ELITE VEHICLE DESK")

uploaded_file = st.file_uploader("Upload Virtual RC Image", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    if st.button("✨ Scan & Auto-Fill"):
        with st.spinner("AI is reading (Stable Mode)..."):
            try:
                img = Image.open(uploaded_file)
                
                # FIX: Beta version ki jagah seedha stable model path use kar rahe hain
                model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')
                
                prompt = "Extract vehicle number, owner name, chassis, engine and address from this RC. Return in simple text."
                
                # API Call
                response = model.generate_content([prompt, img])
                
                if response:
                    st.success("Data Extracted!")
                    st.text_area("Extracted Details:", value=response.text, height=200)
                
            except Exception as e:
                st.error(f"Error: {e}")
                st.info("Solution: Apne Streamlit dashboard mein 'Reboot App' par click karein taaki nayi library install ho jaye.")

# --- Baki ka form aur PDF logic niche... ---
