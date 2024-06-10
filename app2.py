from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Configures genai library with the API key from the environment variable
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize the GenerativeModel
model = genai.GenerativeModel('gemini-pro-vision')

def get_gemini_response(input_text, image_data, prompt):
    response = model.generate_content([input_text, image_data[0], prompt])
    return response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Set page title and header
st.set_page_config(page_title="MultiLanguage Invoice Extractor")
st.title("MultiLanguage Invoice Extractor")

# Text input for user prompt
input_text = st.text_area("Enter your query or prompt:", key="input")

# File uploader for invoice image
uploaded_file = st.file_uploader("Upload the invoice image (JPG, JPEG, PNG):", type=["jpg", "jpeg", "png"])

# Display the uploaded image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

# Analyze button
submit = st.button("Analyze Invoice")

# Input prompt for the AI model
input_prompt = """You are an expert in understanding invoices. 
We will upload an image of an invoice, and you will have to answer any questions based on the uploaded invoice."""

# If submit button is clicked
if submit:
    # Check if input and image are provided
    if input_text and uploaded_file:
        image_data = input_image_setup(uploaded_file)
        # Perform analysis and display response
        with st.spinner("Analyzing..."):
            response = get_gemini_response(input_text, image_data, input_prompt)
        st.success("Analysis complete!")
        st.subheader("Response:")
        st.write(response)
    else:
        st.error("Please provide both a query/prompt and upload an invoice image.")
