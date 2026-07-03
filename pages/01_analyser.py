import streamlit as st
import os
from google import genai

# Configure your page layout
st.set_page_config(page_title="Endometriosis Forum Thread Insights", layout="centered")

st.title("Forum Thread Summarizer & Analyzer")
st.write(
    "Reddit holds some of the deepest peer discussions on women's health conditions like endometriosis. "
    "Copy an entire comment section or thread, paste it below, and let AI structure the patient insights."
    "Note : All user-related information will be filtered out to maintain privacy."
)

# 1. Setup the Gemini Client
try:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
    api_key_loaded = True
except Exception as e:
    api_key_loaded = False
    st.error("Missing Gemini API Key. Please configure your environment variables.")

# 2. Creating the Frontend Layout using Streamlit
if api_key_loaded:
    user_pasted_data = st.text_area(
        label="Paste raw forum thread or comments here:",
        height=300,
        placeholder="Ctrl+A and Ctrl+C on a Reddit page, then paste it here..."
)

    # Create an interactive action button
    if st.button("Generate Structured Summary", type="primary"):
        if not user_pasted_data.strip():
            st.warning("Please paste some text before clicking the button!")
        else:
            # Show a clean loading spinner while the text is processing
            with st.spinner("Analyzing discussion nodes and filtering out system text noise..."):
                
                prompt = f"""
                You are an advanced text processing assistant specializing in healthcare discussions. 
                Analyze the following raw forum comment text copy-pasted from a discussion thread.
                
                Tasks:
                1. Filter out all website UI noise, timestamps, usernames, and system text. But do not generate any filtered content as the response.
                2. Summarize the content in 5 ONLY short bullet points 
                (maximum 10 words per bullet). Focus strictly on extracted keywords.

                Raw Text Data:
                ---
                {user_pasted_data}
                ---
                """
                
                try:
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt,
                    )
                    st.markdown(response.text)
                except Exception as e:
                    if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                        st.error("🔄 System is currently busy (Rate Limit Reached). Please wait 60 seconds before trying another thread!")
                    else:
                        st.error(f"An unexpected error occurred: {e}")