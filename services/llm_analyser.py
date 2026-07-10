# This file handles RAG processes - chunking, cleaning and API handling.

# services/llm_analyzer.py
from google import genai
import streamlit as st

@st.cache_data(show_spinner=False)
def analyze_forum_thread(raw_text: str, api_key: str) -> str:
    """
    Cleans raw forum text, strips system clutter, and passes it to Gemini.
    Optimized with Streamlit Caching so it won't re-run on accidental clicks.
    """
    # 1. Initialize client
    client = genai.Client(api_key=api_key)
    
    # 2. Frame your strict prompt (The 3 Burdens context)
    system_instruction = (
        "You are an expert health communication analyst separating signal from noise in forums. "
        "Analyze this raw forum thread. Discard usernames, dates, and markdown clutter. "
        "Categorize the insights into 5 bullet points - 20 words each for each following category: 1) Medical Education needs, 2) Self-Advocacy struggles."
    )
    
    # 3. Call the API
    response = client.models.generate_content(
        model="gemini-2.5-flash", # efficient for processing long raw threads
        contents=f"{system_instruction}\n\nRaw Text:\n{raw_text}"
    )
    
    return response.text