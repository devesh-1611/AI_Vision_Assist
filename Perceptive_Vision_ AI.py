import streamlit as st
from PIL import Image, ImageEnhance
import pyttsx3
import os
import pytesseract  

# Set Tesseract OCR path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Initialize Text-to-Speech engine
engine = pyttsx3.init()

# Streamlit App Styling
st.markdown(
    """
    <style>
     .main-title {
        font-size: 48px;
         font-weight: bold;
         text-align: center;
         color: #0662f6;
         margin-top: -20px;
     }
    .subtitle {
        font-size: 18px;
        color: #555;
        text-align: center;
        margin-bottom: 20px;
    }
    .feature-header {
        font-size: 24px;
        color: #333;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-title">👁️ Perceptive Vision AI 👁️</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI for Scene Understanding, Text Extraction & Speech for the Visually Impaired 🗣️</div>', unsafe_allow_html=True)

# Sidebar Information
st.sidebar.title("ℹ️ About")
st.sidebar.markdown(
    """
    📌 **Features**
    - 🔍 **Describe Scene**: Get AI insights about the image, including objects and suggestions.
    - 📝 **Extract Text**: Extract visible text using OCR.
    - 🔊 **Text-to-Speech**: Hear the extracted text aloud.

    💡 **How it helps**:
    Assists visually impaired users by providing scene descriptions, text extraction, and speech.
    """
)

# Functions for Functionality
def extract_text_from_image(image):
    """Extract text from an image using OCR."""
    try:
        # Enhance image for better OCR
        image = image.convert("L")  # Convert to grayscale
        image = ImageEnhance.Contrast(image).enhance(2.0)  # Improve contrast
        text = pytesseract.image_to_string(image)
        if not text.strip():
            return "No text detected in the image."
        return text
    except Exception as e:
        st.error(f"Error extracting text: {e}")
        return "Error during OCR."

def text_to_speech(text):
    """Convert text to speech using pyttsx3."""
    try:
        if not text.strip():
            st.warning("No text to convert to speech.")
            return
        engine.say(text)
        engine.runAndWait()
        st.success("✅ Text-to-Speech Conversion Completed!")
    except Exception as e:
        st.error(f"Text-to-Speech Error: {e}")

# File Upload Section
st.markdown("<h3 class='feature-header'>📤 Upload an Image</h3>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Drag and drop or browse an image (JPG, JPEG, PNG)", type=["jpg", "jpeg", "png"])
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

# Feature Buttons
st.markdown("<h3 class='feature-header'>⚙️ Features</h3>", unsafe_allow_html=True)
col1, col2 = st.columns(2)

ocr_button = col1.button("📝 Extract Text")
tts_button = col2.button("🔊 Text-to-Speech")

# Process Features
if uploaded_file:
    if ocr_button:
        with st.spinner("Extracting text from the image..."):
            extracted_text = extract_text_from_image(image)
            st.markdown("<h3 class='feature-header'>📝 Extracted Text</h3>", unsafe_allow_html=True)
            st.text_area("Extracted Text", extracted_text, height=150)

    if tts_button:
        with st.spinner("Converting text to speech..."):
            extracted_text = extract_text_from_image(image)
            text_to_speech(extracted_text)

# Footer
st.markdown(
    """
    <hr>
    <footer style="text-align:center;">
        <p>Powered by <strong>Tesseract OCR</strong> | Built with ❤️ using Streamlit</p>
    </footer>
    """,
    unsafe_allow_html=True,
)

