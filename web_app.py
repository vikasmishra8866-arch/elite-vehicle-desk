import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- API SETUP ---
API_KEY = "AIzaSyBCnOvFT835gjOzBntnKRhFf-jqJIEaP0c"
genai.configure(api_key=API_KEY)

st.title("⭐ ELITE VEHICLE DESK")

# --- FILE UPLOADER ---
uploaded_file = st.file_uploader("Upload Virtual RC Image", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    if st.button("✨ Scan & Auto-Fill"):
        with st.spinner("AI is analyzing (Stable Mode)..."):
            try:
                img = Image.open(uploaded_file)
                
                # FINAL FIX: Yahan 'models/' prefix lagana zaroori hai 404 hatane ke liye
                model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')
                
                # API Call - Bina version specify kiye (Stable default)
                response = model.generate_content(["Extract details from this RC.", img])
                
                if response.text:
                    st.success("Details Extracted Successfully!")
                    st.write(response.text)
                
            except Exception as e:
                # Agar ab bhi error aaye toh seedha error message print hoga
                st.error(f"Technical Detail: {e}")
                st.info("Solution: 2 minute baad refresh karke try karein.")
