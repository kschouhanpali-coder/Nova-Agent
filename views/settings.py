import streamlit as st
import os
from dotenv import load_dotenv

from config import AGENT_MAPPING
from utils import save_env_var, save_key_to_env


def render_settings():
    """Render the Settings/Configuration view."""
    st.markdown("<h1 style='margin-bottom: 2rem;' class='text-gradient'>System Configuration</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="glass-card" style="border-left: 4px solid #00d2ff; --agent-color: #00d2ff;">
        <h2 style="margin-top:0;">Gemini Neural Engine</h2>
        <p style="color:#a1a1aa; font-size:1.1rem; margin-bottom:1.5rem;">Provide your Google Gemini API key to authenticate the generative models. You can save it permanently to the .env file.</p>
    </div>
    """, unsafe_allow_html=True)
    
    new_key = st.text_input("Gemini API Key", value=st.session_state.gemini_key, type="password", placeholder="AIzaSy...")
    if new_key != st.session_state.gemini_key:
        st.session_state.gemini_key = new_key
        
    if st.button("Save Gemini Key to .env"):
        save_key_to_env(new_key)
        load_dotenv(override=True)
        st.session_state.gemini_key = os.getenv('GEMINI_API_KEY', '')
        st.success("Gemini API Key saved permanently to .env file!")
    
    st.markdown("---")
    
    st.markdown("""
    <div class="glass-card" style="border-left: 4px solid #22c55e; --agent-color: #22c55e;">
        <h2 style="margin-top:0;">Groq Fallback Engine</h2>
        <p style="color:#a1a1aa; font-size:1.1rem; margin-bottom:0.5rem;">Free fallback provider. When Gemini quota is exhausted, the system automatically uses Groq (Llama 3).</p>
        <p style="color:#22c55e; font-size:0.9rem;">Get a free key at <a href="https://console.groq.com/keys" style="color:#22c55e;" target="_blank">console.groq.com/keys</a></p>
    </div>
    """, unsafe_allow_html=True)
    
    new_groq_key = st.text_input("Groq API Key", value=st.session_state.groq_key, type="password", placeholder="gsk_...")
    if new_groq_key != st.session_state.groq_key:
        st.session_state.groq_key = new_groq_key
        
    if st.button("Save Groq Key to .env"):
        save_env_var("GROQ_API_KEY", new_groq_key)
        load_dotenv(override=True)
        st.session_state.groq_key = os.getenv('GROQ_API_KEY', '')
        st.success("Groq API Key saved permanently to .env file!")
