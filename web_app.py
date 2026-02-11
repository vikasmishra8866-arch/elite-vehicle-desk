import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# --- API CONFIG ---
API_KEY = "AIzaSyBCnOvFT835gjOzBntnKRhFf-jqJIEaP0c"

# FIX: Forcefully using the stable version to avoid 404 v1beta error
os.environ["GOOGLE_GENERATIVE_AI_NETWORK_ENDPOINT"] = "generativelanguage.googleapis.com"
genai.configure(api_key=API_KEY)

# --- MODEL INITIALIZATION ---
# Yahan hum 'models/gemini-1.5-flash' ka poora path use karenge
model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')

st.title("⭐ ELITE VEHICLE DESK")

uploaded_file = st.file_uploader("Upload Virtual RC Image", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    if st.button("✨ Scan & Auto-Fill"):
        with st.spinner("AI is reading the document..."):
            try:
                img = Image.open(uploaded_file)
                
                # Prompt for extraction
                prompt = "Extract vehicle details from this RC. Return as text."
                
                # Stable call
                response = model.generate_content([prompt, img])
                
                if response.text:
                    st.success("Data Extracted!")
                    st.write(response.text)
                else:
                    st.error("AI couldn't read the text. Try a clearer image.")
                    
            except Exception as e:
                # Agar ab bhi error aaye toh hum model badal kar check karenge
                st.error(f"Technical Error: {e}")
                st.info("Try refreshing the page once.")
