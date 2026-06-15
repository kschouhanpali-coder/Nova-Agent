import streamlit as st

from config import init_session_state
from styles import inject_custom_css
from views import render_home, render_hub, render_chat, render_settings, render_sidebar

# --- Page Config ---
st.set_page_config(
    page_title="NovaAgent Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Initialize State ---
init_session_state()

# --- Inject Theme CSS ---
inject_custom_css(st.session_state.view)

# --- Sidebar (hidden on Home) ---
if st.session_state.view != 'Home':
    render_sidebar()

# --- Route to Active View ---
view = st.session_state.view

if view == 'Home':
    render_home()
elif view == 'Hub':
    render_hub()
elif view == 'Settings':
    render_settings()
elif view == 'Chat':
    render_chat()
