# pages/01_analyser.py
import streamlit as st
from services.llm_analyser import analyze_forum_thread

st.set_page_config(page_title="Forum Thread Insights", layout="centered")
st.title("Forum Thread Summarizer & Analyzer")

# 1. Manage API Key securely
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    st.error("Missing Gemini API Key.")
    st.stop()

# 2. UI Elements
user_pasted_data = st.text_area(
    label="Paste raw forum thread or comments here:",
    height=300,
    placeholder="Ctrl+A and Ctrl+C on a Reddit page, then paste it here..."
)

if st.button("Generate Structured Summary", type="primary"):
    if not user_pasted_data.strip():
        st.warning("Please paste some text before clicking the button!")
    else:
        with st.spinner("Analyzing discussion nodes and filtering text noise..."):
            # Trigger the backend logic
            structured_analysis = analyze_forum_thread(user_pasted_data, api_key)
            
            # Render the final output neatly
            st.success("Analysis Complete!")
            st.markdown(structured_analysis)
