import streamlit as st
import os
import re
import math
import string
import base64
from typing import Optional, List, Dict
from dotenv import load_dotenv
import textwrap

# Load environment variables from .env file
load_dotenv(override=True)

st.set_page_config(
    page_title="NovaAgent Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- State Management ---
if 'view' not in st.session_state:
    st.session_state.view = 'Home'
if 'active_agent' not in st.session_state:
    st.session_state.active_agent = 'planner'

# --- Agent Mapping & Setup ---
AGENT_MAPPING = {
    "planner": {
        "name": "Sam Altman",
        "role": "CEO & Co-Founder, OpenAI",
        "color": "#00d2ff",
        "skill_file": "SKILL.md",
        "rag_file": "SAM_ALTMAN_RAG_MASTER.md",
        "description": "Embody Sam Altman, CEO of OpenAI — architect of ChatGPT, GPT-4, and the modern AGI race. Leverage his expertise in hyper-growth scaling, geopolitical AI alignment, and venture funding to steer groundbreaking technical initiatives, manage complex GPU compute infrastructure, and navigate global AI safety regulations.",
        "capabilities": ["AGI Strategy", "Product Scaling", "Venture & Fundraising", "AI Policy", "Org Design", "AI Economics", "Future of Work"],
        "status": "Online",
        "latency": "14ms"
    },
    "oracle": {
        "name": "Demis Hassabis",
        "role": "CEO & Co-Founder, Google DeepMind",
        "color": "#a855f7",
        "skill_file": "SKILL-2-2.md",
        "rag_file": "DEMIS_HASSABIS_RAG_MASTER.md",
        "description": "Embody Demis Hassabis, CEO of Google DeepMind — neuroscientist, chess prodigy, game designer, and 2024 Chemistry Nobel laureate. Harness deep reinforcement learning, AlphaFold systems biology, and neuroscience-inspired AI models to solve complex scientific challenges, advance materials science, and pioneer next-generation general intelligence.",
        "capabilities": ["Reinforcement Learning", "Protein Biology", "Neuroscience-Inspired AI", "Scientific AI Applications", "AGI Research Strategy", "Multimodal AI", "Game AI"],
        "status": "Online",
        "latency": "18ms"
    },
    "medic": {
        "name": "Dario Amodei",
        "role": "CEO & Co-Founder, Anthropic",
        "color": "#22c55e",
        "skill_file": "SKILL-3-2.md",
        "rag_file": "DARIO_AMODEI_RAG_MASTER.md",
        "description": "Embody Dario Amodei, CEO of Anthropic — AI safety pioneer, creator of Constitutional AI, and architect behind Claude. Apply mathematical safety guarantees, mechanistic interpretability, and robust reinforcement learning principles to build safe, steerable foundation models, manage race dynamics, and draft responsible deployment policies.",
        "capabilities": ["Constitutional AI", "AI Interpretability", "LLM Architecture", "AI Existential Risk", "Responsible Deployment", "Claude Architecture", "AI Safety Policy"],
        "status": "Online",
        "latency": "12ms"
    },
    "lex": {
        "name": "Sridhar Vembu",
        "role": "Founder & CEO, Zoho Corporation",
        "color": "#eab308",
        "skill_file": "SKILL_Sridhar_Vembu.md",
        "rag_file": "RAG_Master_Sridhar_Vembu.md",
        "description": "Embody Sridhar Vembu, founder of Zoho Corporation — the bootstrapped Indian tech pioneer advocating for rural development and digital sovereignty. Utilize his insights on sustainable business operations, locally-focused tech ecosystems, massive bootstrapping strategies, enterprise SaaS integration, and values-driven leadership to build long-term value.",
        "capabilities": ["Bootstrapping Strategy", "Rural Development", "Digital Sovereignty", "SaaS Business Models", "Values-Driven Leadership", "Enterprise SaaS", "Alternative Hiring"],
        "status": "Online",
        "latency": "22ms"
    },
    "learn": {
        "name": "Bhavish Aggarwal",
        "role": "Founder & CEO, Krutrim AI & Ola",
        "color": "#ec4899",
        "skill_file": "SKILL_Bhavish_Aggarwal.md",
        "rag_file": "RAG_Master_Bhavish_Aggarwal.md",
        "description": "Embody Bhavish Aggarwal, founder of Ola and Krutrim AI — India's first AI unicorn building indigenous LLMs and sovereign compute. Navigate multilingual model engineering, EV infrastructure scaling, and developing customized hardware architectures for emerging markets, challenging Western dominance with vernacular AI built for 1.4 billion users.",
        "capabilities": ["Indigenous LLMs", "Multilingual NLP", "Sovereign Compute", "Mobility & EV Tech", "Disruptive Innovation", "Vernacular AI", "Global South Markets"],
        "status": "Online",
        "latency": "15ms"
    }
}

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = {agent_id: [{"role": "assistant", "content": f"Initializing neural link with {info['name']}... Systems ready. How can I assist you today?"}] for agent_id, info in AGENT_MAPPING.items()}
if 'gemini_key' not in st.session_state or st.session_state.gemini_key == 'AIzaSyCUuDzSpT4RA1_AbdXZwBshQfsrNDjayOc' or st.session_state.gemini_key == '':
    st.session_state.gemini_key = os.getenv('GEMINI_API_KEY', '').strip().strip('"\'')
if 'groq_key' not in st.session_state:
    st.session_state.groq_key = os.getenv('GROQ_API_KEY', '').strip().strip('"\'')
if 'gemini_quota_exhausted' not in st.session_state:
    st.session_state.gemini_quota_exhausted = False

# --- Spectacular CSS Injection ---
def inject_custom_css(current_view):
    hide_sidebar_css = ""
    if current_view == 'Home':
        hide_sidebar_css = """
        [data-testid="collapsedControl"] { display: none; }
        [data-testid="stSidebar"] { display: none; }
        .block-container { max-width: 1400px; padding-top: 1rem; }
        """
        
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

        /* Base Theme - Deep Cosmic Indigo with Off-White Text */
        .stApp {{
            background-color: #080914 !important;
            background-image: none !important;
            color: #cbd5e1 !important;
            font-family: 'Outfit', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            overflow-x: hidden;
        }}

        /* Transparency for parent containers to reveal gorgeous 3D background */
        [data-testid="stAppViewContainer"], [data-testid="stHeader"], .main, [data-testid="stAppViewBlockContainer"] {{
            background: transparent !important;
        }}

        /* Spectacular Dynamic Gen AI Mesh Gradients - Glowing Cyberpunk Auroras */
        .stApp::after {{
            content: '';
            position: fixed;
            inset: 0;
            background:
                radial-gradient(circle 750px at 15% 20%, rgba(6, 182, 212, 0.22) 0%, transparent 100%),
                radial-gradient(circle 650px at 85% 15%, rgba(168, 85, 247, 0.2) 0%, transparent 100%),
                radial-gradient(circle 700px at 50% 85%, rgba(236, 72, 153, 0.15) 0%, transparent 100%),
                radial-gradient(circle 600px at 80% 50%, rgba(59, 130, 246, 0.2) 0%, transparent 100%);
            background-size: 200% 200%;
            z-index: -2;
            pointer-events: none;
            filter: blur(90px);
            animation: ai-aurora 25s ease-in-out infinite alternate;
            opacity: 1;
        }}

        @keyframes ai-aurora {{
            0%   {{ background-position: 0% 0% ; transform: scale(1); }}
            50%  {{ background-position: 100% 100%; transform: scale(1.08) rotate(1.5deg); }}
            100% {{ background-position: 50% 0%; transform: scale(0.95) rotate(-1deg); }}
        }}

        /* Premium 21st.dev Style Glowing Dot-Matrix & Cyber Grid Background (Dark Mode) */
        .stApp::before {{
            content: '';
            position: fixed;
            inset: 0;
            background-image: 
                radial-gradient(rgba(255, 255, 255, 0.07) 1.5px, transparent 1.5px),
                linear-gradient(rgba(99, 102, 241, 0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(99, 102, 241, 0.03) 1px, transparent 1px);
            background-size: 32px 32px, 64px 64px, 64px 64px;
            z-index: -1;
            pointer-events: none;
            -webkit-mask-image: radial-gradient(ellipse 90% 70% at 50% 50%, black 40%, transparent 80%);
            mask-image: radial-gradient(ellipse 90% 70% at 50% 50%, black 40%, transparent 80%);
            opacity: 0.95;
            animation: grid-pulse 8s ease-in-out infinite alternate;
        }}

        @keyframes grid-pulse {{
            0% {{ opacity: 0.8; }}
            100% {{ opacity: 0.98; }}
        }}

        /* ===== GEN AI BACKGROUND: Circuit Lines ===== */
        .circuit-container {{
            position: fixed;
            inset: 0;
            pointer-events: none;
            z-index: -1;
            overflow: hidden;
        }}

        /* Animated scan line effect */
        .scan-line {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, transparent, rgba(0, 210, 255, 0.4), rgba(168, 85, 247, 0.3), transparent);
            z-index: 0;
            pointer-events: none;
            animation: scan-sweep 6s linear infinite;
            opacity: 0.6;
            box-shadow: 0 0 15px rgba(0, 210, 255, 0.3), 0 0 30px rgba(0, 210, 255, 0.1);
        }}
        @keyframes scan-sweep {{
            0% {{ top: -2px; opacity: 0; }}
            10% {{ opacity: 0.6; }}
            90% {{ opacity: 0.6; }}
            100% {{ top: 100vh; opacity: 0; }}
        }}

        /* Glowing corner frame accents */
        .glow-frame {{
            position: fixed;
            inset: 0;
            pointer-events: none;
            z-index: 0;
        }}
        .glow-frame::before {{
            content: '';
            position: absolute;
            top: 0; left: 0;
            width: 200px; height: 200px;
            border-top: 1px solid rgba(0, 210, 255, 0.3);
            border-left: 1px solid rgba(0, 210, 255, 0.3);
            box-shadow: -5px -5px 25px rgba(0, 210, 255, 0.08);
        }}
        .glow-frame::after {{
            content: '';
            position: absolute;
            bottom: 0; right: 0;
            width: 200px; height: 200px;
            border-bottom: 1px solid rgba(168, 85, 247, 0.3);
            border-right: 1px solid rgba(168, 85, 247, 0.3);
            box-shadow: 5px 5px 25px rgba(168, 85, 247, 0.08);
        }}

        /* Holographic perspective grid floor */
        .holo-grid {{
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            height: 45vh;
            background:
                linear-gradient(rgba(6, 182, 212, 0.06) 1px, transparent 1px),
                linear-gradient(90deg, rgba(6, 182, 212, 0.06) 1px, transparent 1px);
            background-size: 60px 60px;
            transform: perspective(500px) rotateX(65deg);
            transform-origin: bottom;
            pointer-events: none;
            z-index: -1;
            mask-image: linear-gradient(to top, rgba(0,0,0,0.5) 0%, transparent 80%);
            -webkit-mask-image: linear-gradient(to top, rgba(0,0,0,0.5) 0%, transparent 80%);
            animation: grid-scroll 4s linear infinite;
        }}
        @keyframes grid-scroll {{
            0% {{ background-position: 0 0; }}
            100% {{ background-position: 0 60px; }}
        }}

        /* Floating neural network nodes */
        .neural-node {{
            position: fixed;
            width: 4px;
            height: 4px;
            border-radius: 50%;
            pointer-events: none;
            z-index: 0;
        }}
        .neural-node::after {{
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 40px;
            height: 1px;
            transform-origin: left center;
            opacity: 0.3;
        }}
        .nn1 {{
            background: #00d2ff;
            box-shadow: 0 0 8px #00d2ff, 0 0 20px rgba(0,210,255,0.3);
            top: 20%; left: 8%;
            animation: neural-pulse 3s ease-in-out infinite alternate;
        }}
        .nn1::after {{ background: linear-gradient(90deg, rgba(0,210,255,0.4), transparent); transform: rotate(25deg); }}
        .nn2 {{
            background: #a855f7;
            box-shadow: 0 0 8px #a855f7, 0 0 20px rgba(168,85,247,0.3);
            top: 35%; right: 12%;
            animation: neural-pulse 4s ease-in-out infinite alternate 1s;
        }}
        .nn2::after {{ background: linear-gradient(90deg, rgba(168,85,247,0.4), transparent); transform: rotate(-35deg); }}
        .nn3 {{
            background: #22c55e;
            box-shadow: 0 0 8px #22c55e, 0 0 20px rgba(34,197,94,0.3);
            top: 65%; left: 5%;
            animation: neural-pulse 3.5s ease-in-out infinite alternate 0.5s;
        }}
        .nn3::after {{ background: linear-gradient(90deg, rgba(34,197,94,0.4), transparent); transform: rotate(15deg); }}
        .nn4 {{
            background: #ec4899;
            box-shadow: 0 0 8px #ec4899, 0 0 20px rgba(236,72,153,0.3);
            top: 75%; right: 6%;
            animation: neural-pulse 5s ease-in-out infinite alternate 2s;
        }}
        .nn4::after {{ background: linear-gradient(90deg, rgba(236,72,153,0.4), transparent); transform: rotate(-20deg); }}
        .nn5 {{
            background: #eab308;
            box-shadow: 0 0 8px #eab308, 0 0 20px rgba(234,179,8,0.3);
            top: 15%; right: 30%;
            animation: neural-pulse 4.5s ease-in-out infinite alternate 1.5s;
        }}
        .nn5::after {{ background: linear-gradient(90deg, rgba(234,179,8,0.4), transparent); transform: rotate(40deg); }}
        .nn6 {{
            background: #00d2ff;
            box-shadow: 0 0 8px #00d2ff, 0 0 20px rgba(0,210,255,0.3);
            top: 50%; left: 25%;
            animation: neural-pulse 3s ease-in-out infinite alternate 3s;
        }}
        .nn6::after {{ background: linear-gradient(90deg, rgba(0,210,255,0.4), transparent); transform: rotate(-10deg); }}

        @keyframes neural-pulse {{
            0% {{ transform: scale(1); opacity: 0.5; }}
            50% {{ transform: scale(1.8); opacity: 1; }}
            100% {{ transform: scale(1); opacity: 0.4; }}
        }}

        /* Circuit connection lines */
        .circuit-line {{
            position: fixed;
            pointer-events: none;
            z-index: 0;
            opacity: 0.15;
        }}
        .cl-h1 {{
            top: 20%;
            left: 0;
            right: 60%;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(0,210,255,0.6), transparent);
            animation: circuit-flow-h 3s linear infinite;
        }}
        .cl-h2 {{
            top: 75%;
            left: 40%;
            right: 0;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(168,85,247,0.6), transparent);
            animation: circuit-flow-h 4s linear infinite 1s;
        }}
        .cl-v1 {{
            left: 8%;
            top: 10%;
            bottom: 60%;
            width: 1px;
            background: linear-gradient(180deg, transparent, rgba(0,210,255,0.5), transparent);
            animation: circuit-flow-v 5s linear infinite;
        }}
        .cl-v2 {{
            right: 12%;
            top: 30%;
            bottom: 20%;
            width: 1px;
            background: linear-gradient(180deg, transparent, rgba(168,85,247,0.5), transparent);
            animation: circuit-flow-v 6s linear infinite 2s;
        }}
        @keyframes circuit-flow-h {{
            0% {{ opacity: 0.05; }}
            50% {{ opacity: 0.25; }}
            100% {{ opacity: 0.05; }}
        }}
        @keyframes circuit-flow-v {{
            0% {{ opacity: 0.05; }}
            50% {{ opacity: 0.2; }}
            100% {{ opacity: 0.05; }}
        }}

        /* Data stream overlay */
        .data-stream {{
            position: fixed;
            top: 0;
            width: 1px;
            height: 100vh;
            pointer-events: none;
            z-index: 0;
            opacity: 0.08;
        }}
        .ds1 {{ left: 15%; background: linear-gradient(180deg, transparent 0%, #00d2ff 30%, #00d2ff 70%, transparent 100%); animation: data-fall 4s linear infinite; }}
        .ds2 {{ left: 35%; background: linear-gradient(180deg, transparent 0%, #a855f7 30%, #a855f7 70%, transparent 100%); animation: data-fall 5s linear infinite 1.5s; }}
        .ds3 {{ left: 65%; background: linear-gradient(180deg, transparent 0%, #00d2ff 30%, #00d2ff 70%, transparent 100%); animation: data-fall 3.5s linear infinite 0.8s; }}
        .ds4 {{ left: 85%; background: linear-gradient(180deg, transparent 0%, #ec4899 30%, #ec4899 70%, transparent 100%); animation: data-fall 6s linear infinite 2.5s; }}
        @keyframes data-fall {{
            0% {{ transform: translateY(-100%); }}
            100% {{ transform: translateY(100vh); }}
        }}



        /* Hide the native Streamlit button used to trigger navigation */
        div:has(#hidden-btn-container) + div {{
            position: absolute !important;
            width: 1px !important;
            height: 1px !important;
            padding: 0 !important;
            margin: -1px !important;
            overflow: hidden !important;
            clip: rect(0, 0, 0, 0) !important;
            white-space: nowrap !important;
            border: 0 !important;
            opacity: 0 !important;
            pointer-events: none !important;
        }}
        #hidden-btn-container {{
            display: none !important;
        }}
        
        h1, h2, h3, h4, h5, h6 {{
            color: #f8fafc !important;
            font-weight: 700;
            letter-spacing: -0.02em;
        }}

        .text-gradient {{
            background: linear-gradient(135deg, #00d2ff 0%, #a855f7 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        /* Sidebar styling - Advanced Frosted Dark Glassmorphism */
        [data-testid="stSidebar"] {{
            background: rgba(10, 11, 24, 0.6) !important;
            backdrop-filter: blur(30px) saturate(160%) !important;
            -webkit-backdrop-filter: blur(30px) saturate(160%) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.06) !important;
            box-shadow: 5px 0 30px rgba(0,0,0,0.3), 1px 0 10px rgba(99, 102, 241, 0.05) !important;
            perspective: 1000px;
        }}
        
        /* 3D Sidebar Buttons */
        [data-testid="stSidebar"] .stButton > button {{
            background: rgba(255, 255, 255, 0.04) !important;
            border: 1px solid rgba(255, 255, 255, 0.06) !important;
            justify-content: flex-start !important;
            padding: 0.8rem 1.2rem !important;
            color: #cbd5e1 !important;
            font-size: 1rem !important;
            font-weight: 500 !important;
            border-radius: 12px !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2), inset 0 1px 0 rgba(255,255,255,0.05) !important;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
            transform-style: preserve-3d !important;
            margin-bottom: 0.5rem !important;
        }}
        
        [data-testid="stSidebar"] .stButton > button:hover {{
            background: rgba(255, 255, 255, 0.08) !important;
            border-color: rgba(6, 182, 212, 0.4) !important;
            color: #ffffff !important;
            box-shadow: 0 4px 15px rgba(6, 182, 212, 0.2), inset 0 1px 0 rgba(255,255,255,0.1) !important;
            transform: translate3d(8px, -2px, 15px) !important;
        }}

        [data-testid="stSidebar"] .stButton > button:active {{
            transform: translate3d(4px, 0, 5px) !important;
        }}

        /* Active indicator selectors (Dark Mode) */
        div:has(#active-hub) + div button,
        div:has(#active-chat) + div button,
        div:has(#active-settings) + div button {{
            background: linear-gradient(135deg, rgba(6, 182, 212, 0.15), rgba(168, 85, 247, 0.15)) !important;
            border: 1px solid rgba(6, 182, 212, 0.4) !important;
            color: #ffffff !important;
            box-shadow: 0 4px 15px rgba(6, 182, 212, 0.25), inset 0 0 12px rgba(255, 255, 255, 0.1) !important;
            transform: translate3d(10px, -2px, 20px) !important;
            font-weight: 600 !important;
        }}

        /* Sidebar Logo Animations */
        @keyframes logo-breathe {{
            0% {{ box-shadow: 0 0 15px rgba(0, 210, 255, 0.4); }}
            50% {{ box-shadow: 0 0 25px rgba(168, 85, 247, 0.8); }}
            100% {{ box-shadow: 0 0 15px rgba(0, 210, 255, 0.4); }}
        }}
        @keyframes core-spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        .sidebar-logo-container {{
            animation: logo-breathe 4s ease-in-out infinite !important;
        }}
        .sidebar-logo-core {{
            animation: core-spin 6s linear infinite !important;
        }}

        /* Hide default Streamlit elements */
        #MainMenu {{visibility: hidden;}}
        header {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        .block-container {{ padding-top: 3rem; padding-bottom: 3rem; max-width: 1200px; position: relative; z-index: 5; }}

        {hide_sidebar_css}        /* --- STUNNING LANDING PAGE --- */
        .landing-top-pill {{
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 20px;
            padding: 0.3rem 1.2rem;
            font-size: 0.8rem;
            letter-spacing: 0.1em;
            color: #94a3b8;
            display: inline-flex;
            align-items: center;
            margin: 0 auto;
            position: absolute;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            backdrop-filter: blur(10px);
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }}
        
        .hero-title {{
            font-size: 5rem;
            font-weight: 800;
            margin: 0;
            line-height: 1.1;
            letter-spacing: -0.04em;
            text-shadow: 0 4px 30px rgba(6, 182, 212, 0.2);
        }}
        .hero-title span {{
            background: linear-gradient(90deg, #00d2ff, #a855f7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .hero-subtitle {{
            font-size: 1.4rem;
            color: #94a3b8;
            margin-top: 1rem;
            margin-bottom: 3rem;
            font-weight: 400;
        }}
        
        /* Spectacular AI Core */
        .tech-frame {{
            position: relative;
            border-radius: 24px;
            background: radial-gradient(circle at center, rgba(6,182,212,0.04) 0%, transparent 70%);
            display: flex;
            justify-content: center;
            align-items: center;
            height: 550px;
            overflow: hidden;
            box-shadow: inset 0 0 50px rgba(6,182,212,0.02);
        }}
        
        .ai-core-container {{
            position: relative;
            width: 400px;
            height: 400px;
            display: flex;
            align-items: center;
            justify-content: center;
            perspective: 1200px;
            z-index: 5;
        }}
        .core-brain {{
            position: absolute;
            width: 140px; height: 140px;
            border-radius: 50%;
            background: radial-gradient(circle at 30% 30%, #fff 0%, #00d2ff 30%, #a855f7 80%);
            box-shadow: 0 10px 60px rgba(6, 182, 212, 0.5), inset 0 0 40px #fff;
            animation: pulse-brain 4s ease-in-out infinite alternate;
            z-index: 10;
        }}
        .hologram-ring {{
            position: absolute;
            border-radius: 50%;
            border: 2px solid rgba(6, 182, 212, 0.4);
            box-shadow: inset 0 0 20px rgba(6,182,212,0.1), 0 0 20px rgba(6,182,212,0.15);
            transform-style: preserve-3d;
        }}
        .ring1 {{ width: 360px; height: 140px; border-color: rgba(168, 85, 247, 0.5); animation: spin1 10s linear infinite; }}
        .ring2 {{ width: 140px; height: 360px; border-color: rgba(6, 182, 212, 0.5); animation: spin2 14s linear infinite; }}
        .ring3 {{ width: 380px; height: 380px; border: 1px dashed rgba(255, 255, 255, 0.1); box-shadow: none; animation: spin3 20s linear infinite; }}
        
        @keyframes spin1 {{ 0% {{ transform: rotateX(75deg) rotateZ(0deg); }} 100% {{ transform: rotateX(75deg) rotateZ(360deg); }} }}
        @keyframes spin2 {{ 0% {{ transform: rotateY(75deg) rotateZ(0deg); }} 100% {{ transform: rotateY(75deg) rotateZ(360deg); }} }}
        @keyframes spin3 {{ 0% {{ transform: rotateZ(0deg); }} 100% {{ transform: rotateZ(360deg); }} }}
        @keyframes pulse-brain {{ 0% {{ transform: scale(0.9); opacity: 0.85; filter: drop-shadow(0 0 40px rgba(168, 85, 247, 0.3)); }} 100% {{ transform: scale(1.1); opacity: 1; filter: drop-shadow(0 0 80px rgba(6, 182, 212, 0.5)); }} }}
 
        /* Dashboard UI / 3D Glassmorphism Cards */
        .dash-stat-box {{
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 12px;
            padding: 1rem 1.5rem;
            display: flex;
            align-items: center;
            gap: 1rem;
            backdrop-filter: blur(10px);
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            transform-style: preserve-3d;
            box-shadow: 0 4px 15px rgba(0,0,0,0.15);
        }}
        .dash-stat-box:hover {{
            transform: translateY(-5px) scale(1.05) rotateX(10deg) rotateY(5deg);
            box-shadow: 0 15px 35px rgba(0,0,0,0.3), inset 0 0 15px rgba(255,255,255,0.05);
            border-color: rgba(6, 182, 212, 0.3);
            z-index: 10;
        }}
        
        .glass-card {{
            background: rgba(255, 255, 255, 0.03) !important; 
            border: 1px solid rgba(255, 255, 255, 0.06) !important; 
            border-radius: 20px !important; 
            padding: 1.5rem; 
            margin-bottom: 1.5rem; 
            display: flex; flex-direction: column; height: 100%; 
            backdrop-filter: blur(28px) saturate(160%) !important; 
            -webkit-backdrop-filter: blur(28px) saturate(160%) !important; 
            box-shadow: 0 10px 30px rgba(0,0,0,0.2), inset 0 1px 0 rgba(255,255,255,0.05) !important; 
            transition: all 0.5s cubic-bezier(0.23, 1, 0.32, 1);
            position: relative; 
            transform-style: preserve-3d;
            perspective: 1000px;
        }}
        .glass-card:hover {{ 
            transform: translateY(-12px) scale(1.03) rotateX(4deg) rotateY(-4deg); 
            border-color: rgba(255, 255, 255, 0.15) !important; 
            box-shadow: 
                0 20px 40px rgba(0, 0, 0, 0.3), 
                0 0 35px rgba(6, 182, 212, 0.15),
                inset 0 0 20px rgba(255,255,255,0.05) !important; 
            z-index: 20;
        }}
        /* Make inner elements pop out in 3D on hover */
        .glass-card > * {{
            transition: transform 0.5s cubic-bezier(0.23, 1, 0.32, 1);
        }}
        .glass-card:hover > * {{
            transform: translateZ(30px);
        }}
        /* 3D Agent Core inside Dashboard Cards */
        .agent-3d-core {{
            position: relative;
            width: 64px;
            height: 64px;
            perspective: 800px;
            display: flex;
            justify-content: center;
            align-items: center;
            margin-right: 1.2rem;
            flex-shrink: 0;
            transform-style: preserve-3d;
        }}
        .agent-3d-core .ring {{
            position: absolute;
            width: 100%;
            height: 100%;
            border-radius: 50%;
            border: 2px solid var(--agent-color);
            box-shadow: 0 0 10px var(--agent-color), inset 0 0 10px var(--agent-color);
            opacity: 0.8;
        }}
        .agent-3d-core .ring-x {{ animation: spin-x 4s linear infinite; }}
        .agent-3d-core .ring-y {{ animation: spin-y 5s linear infinite; border: 2px dashed var(--agent-color); }}
        .agent-3d-core .ring-z {{ animation: spin-z 6s linear infinite; }}
        .agent-3d-core .core-dot {{
            position: absolute;
            width: 18px;
            height: 18px;
            background: #fff;
            border-radius: 50%;
            box-shadow: 0 0 20px 8px var(--agent-color);
            animation: pulse-dot 2s ease-in-out infinite alternate;
        }}

        @keyframes spin-x {{ 0% {{ transform: rotateX(0deg) rotateY(45deg); }} 100% {{ transform: rotateX(360deg) rotateY(45deg); }} }}
        @keyframes spin-y {{ 0% {{ transform: rotateY(0deg) rotateZ(45deg); }} 100% {{ transform: rotateY(360deg) rotateZ(45deg); }} }}
        @keyframes spin-z {{ 0% {{ transform: rotateZ(0deg) rotateX(45deg); }} 100% {{ transform: rotateZ(360deg) rotateX(45deg); }} }}
        @keyframes pulse-dot {{ 0% {{ transform: scale(0.8); }} 100% {{ transform: scale(1.3); }} }}
        .agent-role {{ 
            font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.1em; 
            color: #cbd5e1; background: rgba(255, 255, 255, 0.04); padding: 0.3rem 0.8rem; 
            border-radius: 20px; display: inline-block; margin-top: 0.4rem; 
            border: 1px solid rgba(255, 255, 255, 0.08); 
        }}
        
        /* Buttons */
        .btn-primary > button {{
            background: linear-gradient(90deg, #00d2ff, #8b5cf6) !important;
            border: none !important;
            color: #fff !important;
            border-radius: 8px !important;
            padding: 0.6rem 2rem !important;
            font-size: 1.1rem !important;
            font-weight: 600 !important;
            box-shadow: 0 4px 15px rgba(6, 182, 212, 0.3) !important;
            transition: all 0.3s ease !important;
        }}
        .btn-primary > button:hover {{
            box-shadow: 0 6px 20px rgba(6, 182, 212, 0.45) !important;
            transform: scale(1.03) !important;
            color: #fff !important;
        }}
        
        /* Absolute positioning for Initialize buttons inside columns */
        div[data-testid="column"]:has(.agent-card) [data-testid="stVerticalBlock"] {{
            position: relative !important;
            height: 580px !important;
        }}
        
        div[data-testid="column"]:has(.agent-card) [data-testid="stVerticalBlock"] > div:has(button) {{
            position: absolute !important;
            bottom: 2.2rem !important;
            left: 0 !important;
            right: 0 !important;
            margin: 0 !important;
            padding: 0 1.5rem !important;
            z-index: 10 !important;
        }}
        
        div[data-testid="column"]:has(.agent-card) [data-testid="stVerticalBlock"] > div:has(button) button {{
            background: linear-gradient(90deg, #00d2ff, #8b5cf6) !important;
            border: none !important;
            color: #fff !important;
            border-radius: 8px !important;
            padding: 0.6rem 2rem !important;
            font-size: 1.1rem !important;
            font-weight: 600 !important;
            box-shadow: 0 4px 15px rgba(6, 182, 212, 0.3) !important;
            transition: all 0.3s ease !important;
            width: 100% !important;
        }}
        
        div[data-testid="column"]:has(.agent-card) [data-testid="stVerticalBlock"] > div:has(button) button:hover {{
            box-shadow: 0 6px 20px rgba(6, 182, 212, 0.45) !important;
            transform: scale(1.03) !important;
            color: #fff !important;
        }}
        
        .agent-card {{
            height: 580px !important;
            display: flex !important;
            flex-direction: column !important;
        }}
        .btn-secondary > button {{
            background: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            color: #f1f5f9 !important;
            border-radius: 8px !important;
            padding: 0.6rem 2rem !important;
            font-size: 1.1rem !important;
            font-weight: 500 !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
        }}
        .btn-secondary > button:hover {{
            background: rgba(255, 255, 255, 0.08) !important;
            border-color: rgba(6, 182, 212, 0.4) !important;
            color: #00d2ff !important;
            box-shadow: 0 4px 15px rgba(6, 182, 212, 0.2) !important;
        }}
        
        /* Chat background */
        .stChatMessageContainer::before {{
            content: '';
            position: absolute;
            top: 0; right: 0; bottom: 0; left: 0;
            background-image: radial-gradient(circle at center, rgba(6, 182, 212, 0.12) 0%, transparent 60%);
            pointer-events: none;
            z-index: -1;
        }}

        /* Chat messages styling */
        [data-testid="stChatMessage"] {{
            background-color: rgba(255, 255, 255, 0.03) !important;
            border: 1px solid rgba(255, 255, 255, 0.06) !important;
            border-radius: 16px !important;
            transition: all 0.3s ease !important;
        }}
        [data-testid="stChatMessage"]:hover {{
            background-color: rgba(255, 255, 255, 0.05) !important;
            border-color: rgba(255, 255, 255, 0.1) !important;
        }}

        /* Chat name labels */
        .chat-name-label {{
            font-size: 0.8rem;
            font-weight: 700;
            letter-spacing: 0.03em;
            margin-bottom: 0.35rem;
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        .chat-name-agent {{
            color: var(--agent-chat-color, #00d2ff);
        }}
        .chat-name-user {{
            color: #94a3b8;
        }}
        .chat-name-label .chat-dot {{
            width: 6px;
            height: 6px;
            border-radius: 50%;
            display: inline-block;
        }}
        .chat-name-agent .chat-dot {{
            background: var(--agent-chat-color, #00d2ff);
            box-shadow: 0 0 6px var(--agent-chat-color, #00d2ff);
        }}
        .chat-name-user .chat-dot {{
            background: #64748b;
            box-shadow: 0 0 4px rgba(100, 116, 139, 0.5);
        }}

        /* ===== Native SVG Chat Avatars ===== */
        .agent-chat-wrapper [data-testid="stChatMessageAvatar"] {{
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            overflow: visible !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            width: 40px !important;
            height: 40px !important;
        }}
        .agent-chat-wrapper [data-testid="stChatMessageAvatar"] img {{
            width: 40px !important;
            height: 40px !important;
            border-radius: 50% !important;
            object-fit: contain !important;
            filter: drop-shadow(0 0 6px var(--chat-agent-color, #00d2ff)) !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }}
        .agent-chat-wrapper [data-testid="stChatMessageAvatar"] img:hover {{
            transform: scale(1.15) rotate(10deg) !important;
            filter: drop-shadow(0 0 12px var(--chat-agent-color, #00d2ff)) !important;
        }}
        /* User avatar specific shadow styling */
        .agent-chat-wrapper [data-testid="stChatMessage"]:has(.chat-name-user) [data-testid="stChatMessageAvatar"] img {{
            filter: drop-shadow(0 0 4px rgba(148, 163, 184, 0.4)) !important;
        }}
        .agent-chat-wrapper [data-testid="stChatMessage"]:has(.chat-name-user) [data-testid="stChatMessageAvatar"] img:hover {{
            transform: scale(1.15) rotate(-10deg) !important;
            filter: drop-shadow(0 0 8px rgba(148, 163, 184, 0.6)) !important;
        }}

        /* Chat input container */
        [data-testid="stChatInput"] {{
            background: rgba(15, 17, 36, 0.6) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 24px !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255,255,255,0.05) !important;
            backdrop-filter: blur(20px) !important;
        }}
        [data-testid="stChatInput"] textarea {{
            color: #f8fafc !important;
            background: transparent !important;
            border: none !important;
        }}

        /* Streamlit Input fields & text areas */
        div[data-baseweb="input"] {{
            background-color: rgba(255, 255, 255, 0.03) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 8px !important;
        }}
        div[data-baseweb="input"] input {{
            color: #f8fafc !important;
        }}
        </style>

        <!-- Gen AI Background Elements -->
        <div class="scan-line"></div>
        <div class="glow-frame"></div>
        <div class="holo-grid"></div>

        <!-- Neural Network Nodes -->
        <div class="neural-node nn1"></div>
        <div class="neural-node nn2"></div>
        <div class="neural-node nn3"></div>
        <div class="neural-node nn4"></div>
        <div class="neural-node nn5"></div>
        <div class="neural-node nn6"></div>

        <!-- Circuit Lines -->
        <div class="circuit-line cl-h1"></div>
        <div class="circuit-line cl-h2"></div>
        <div class="circuit-line cl-v1"></div>
        <div class="circuit-line cl-v2"></div>

        <!-- Data Streams -->
        <div class="data-stream ds1"></div>
        <div class="data-stream ds2"></div>
        <div class="data-stream ds3"></div>
        <div class="data-stream ds4"></div>
    """, unsafe_allow_html=True)


# --- RAG Core Logic ---
class TFIDFRetriever:
    def __init__(self, chunks: List[Dict[str, str]]):
        self.chunks = chunks
        self.stopwords = {"the", "a", "an", "and", "or", "but", "is", "are", "was", "were", "to", "of", "in", "on", "at", "for", "with"}
        self.idf = {}
        self.doc_tfs = []
        self._build_index()
        
    def _tokenize(self, text: str) -> List[str]:
        text = text.lower().translate(str.maketrans('', '', string.punctuation))
        return [t for t in text.split() if t not in self.stopwords]
        
    def _build_index(self):
        N = len(self.chunks)
        if N == 0: return
        df = {}
        for chunk in self.chunks:
            tokens = self._tokenize(chunk["content"])
            tf = {}
            for token in tokens: tf[token] = tf.get(token, 0) + 1
            self.doc_tfs.append(tf)
            for token in set(tokens): df[token] = df.get(token, 0) + 1
        for token, count in df.items():
            self.idf[token] = math.log(1 + (N / (1 + count)))
            
    def retrieve(self, query: str, top_k: int = 5) -> List[tuple]:
        query_tokens = self._tokenize(query)
        if not query_tokens or not self.chunks: return [(chunk, 0.0) for chunk in self.chunks[:top_k]]
        
        query_tf = {}
        for t in query_tokens: query_tf[t] = query_tf.get(t, 0) + 1
        
        query_tfidf = {t: c * self.idf.get(t, 0) for t, c in query_tf.items() if t in self.idf}
        query_len = math.sqrt(sum(v*v for v in query_tfidf.values()))
        
        if query_len == 0: return [(chunk, 0.0) for chunk in self.chunks[:top_k]]
        
        scores = []
        for i, doc_tf in enumerate(self.doc_tfs):
            dot_product = sum(query_tfidf[t] * (tf * self.idf.get(t, 0)) for t, tf in doc_tf.items() if t in query_tfidf)
            doc_len = math.sqrt(sum((tf * self.idf.get(t, 0))**2 for t, tf in doc_tf.items()))
            sim = dot_product / (query_len * doc_len) if doc_len > 0 else 0.0
            scores.append((self.chunks[i], sim))
            
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]

def chunk_document(content: str) -> List[Dict[str, str]]:
    chunks, current_header, current_lines = [], "Intro", []
    for line in content.split("\n"):
        if line.startswith("## "):
            if current_lines: chunks.append({"header": current_header, "content": "\n".join(current_lines).strip()})
            current_header, current_lines = line.replace("##", "").strip(), []
        else: current_lines.append(line)
    if current_lines: chunks.append({"header": current_header, "content": "\n".join(current_lines).strip()})
    return [c for c in chunks if len(c["content"].split()) > 15]

@st.cache_resource
def load_rag_indices():
    retrievers = {}
    for a_id, info in AGENT_MAPPING.items():
        paths = [f"backend/data/rag_documents/{info['rag_file']}", f"backend/{info['rag_file']}", info['rag_file']]
        file_path = next((p for p in paths if os.path.exists(p)), None)
        if file_path:
            with open(file_path, "r", encoding="utf-8") as f:
                retrievers[a_id] = TFIDFRetriever(chunk_document(f.read()))
        else: retrievers[a_id] = None
    return retrievers

retrievers = load_rag_indices()

def save_env_var(var_name, value):
    env_path = ".env"
    if not os.path.exists(env_path):
        with open(env_path, "w", encoding="utf-8") as f:
            f.write(f"{var_name}={value}\n")
        return
    with open(env_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    key_exists = False
    new_lines = []
    for line in lines:
        if line.strip().startswith(f"{var_name}="):
            new_lines.append(f"{var_name}={value}\n")
            key_exists = True
        else:
            new_lines.append(line)
    if not key_exists:
        new_lines.append(f"\n{var_name}={value}\n")
    with open(env_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

def save_key_to_env(key):
    save_env_var("GEMINI_API_KEY", key)

# --- Main App Execution ---
inject_custom_css(st.session_state.view)


# Sidebar (Only visible if not Home)
if st.session_state.view != 'Home':
    with st.sidebar:
        # High-end Logo
        st.markdown("""
        <div style='display:flex; align-items:center; gap:12px; margin-bottom: 2.5rem; padding: 0.5rem;'>
            <div class="sidebar-logo-container" style='width: 32px; height: 32px; border-radius: 8px; background: linear-gradient(135deg, #00d2ff, #a855f7); display:flex; align-items:center; justify-content:center; box-shadow: 0 0 15px rgba(0,210,255,0.4);'>
                <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="#ffffff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" style="display: block;"><path d="M6 18V6L18 18V6" /></svg>
            </div>
            <h2 style='margin:0; font-size:1.6rem; letter-spacing: -0.03em;' class='text-gradient'>NovaAgent</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Modules Hub Button
        if st.session_state.view == 'Hub':
            st.markdown('<div id="active-hub"></div>', unsafe_allow_html=True)
        if st.button("❖ Modules Hub", use_container_width=True): 
            st.session_state.view = 'Hub'
            st.rerun()
        
        # Neural Chat Button
        if st.session_state.view == 'Chat':
            st.markdown('<div id="active-chat"></div>', unsafe_allow_html=True)
        if st.button("💬 Neural Chat", use_container_width=True): 
            st.session_state.view = 'Chat'
            st.rerun()
        
        # Settings Button
        if st.session_state.view == 'Settings':
            st.markdown('<div id="active-settings"></div>', unsafe_allow_html=True)
        if st.button("⚙️ Settings", use_container_width=True): 
            st.session_state.view = 'Settings'
            st.rerun()
        
        # Disconnect Button
        if st.button("⏏️ Disconnect", use_container_width=True): 
            st.session_state.view = 'Home'
            st.rerun()

# Views
view = st.session_state.view

if view == 'Home':
    # Inject extra landing-page-only CSS
    st.markdown("""
    <style>
    /* Full-screen hero adjustments */
    .block-container { max-width: 1200px !important; padding-top: 0 !important; }
    

    
    /* Floating particles */
    @keyframes float-up { 0%{transform:translateY(0) scale(1);opacity:0.6} 100%{transform:translateY(-80vh) scale(0.2);opacity:0} }
    .particle { position:fixed; width:3px; height:3px; background:#00d2ff; border-radius:50%; pointer-events:none; z-index:0; }
    .p1{left:10%;bottom:0;animation:float-up 8s linear infinite;opacity:0.4}
    .p2{left:25%;bottom:0;animation:float-up 12s linear infinite 2s;opacity:0.3;background:#a855f7}
    .p3{left:50%;bottom:0;animation:float-up 10s linear infinite 4s;opacity:0.5}
    .p4{left:75%;bottom:0;animation:float-up 9s linear infinite 1s;opacity:0.3;background:#ec4899}
    .p5{left:90%;bottom:0;animation:float-up 11s linear infinite 3s;opacity:0.4;background:#a855f7}
    .p6{left:40%;bottom:0;animation:float-up 13s linear infinite 5s;opacity:0.2}
    .p7{left:60%;bottom:0;animation:float-up 7s linear infinite 6s;opacity:0.5;background:#22c55e}
    .p8{left:15%;bottom:0;animation:float-up 14s linear infinite 7s;opacity:0.3;background:#eab308}
    
    /* Feature cards */
    .feat-card {
        background: rgba(255, 255, 255, 0.035);
        border: 1px solid rgba(255, 255, 255, 0.09);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        backdrop-filter: blur(20px) saturate(150%);
        -webkit-backdrop-filter: blur(20px) saturate(150%);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        transform-style: preserve-3d;
        height: 100%;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    .feat-card:hover {
        transform: translateY(-8px) scale(1.02);
        border-color: rgba(255, 255, 255, 0.3);
        box-shadow: 0 20px 40px rgba(0,0,0,0.6), 0 0 35px var(--fc);
    }
    .feat-icon {
        width: 56px; height: 56px; border-radius: 12px;
        display: flex; align-items:center; justify-content:center;
        margin: 0 auto 1rem auto; font-size: 1.8rem;
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 0 20px var(--fc);
    }
    
    /* Stats row */
    .stat-item { text-align: center; }
    .stat-num { font-size: 2.5rem; font-weight: 800; letter-spacing: -0.03em; }
    .stat-label { font-size: 0.85rem; color: #71717a; text-transform: uppercase; letter-spacing: 0.1em; margin-top: 0.25rem; }
    
    /* Nav bar */
    .top-nav {
        position: fixed; top: 0; left: 0; right: 0; z-index: 1000;
        display: flex; align-items: center; justify-content: space-between;
        padding: 1rem 3rem;
        background: rgba(0,0,0,0.5);
        backdrop-filter: blur(20px);
        border-bottom: 1px solid rgba(255,255,255,0.05);
    }
    .nav-logo { display:flex; align-items:center; gap:10px; }
    .nav-links { display:flex; gap: 2rem; }
    .nav-links a { color: #a1a1aa; text-decoration:none; font-size:0.95rem; font-weight:500; transition: color 0.2s; }
    .nav-links a:hover { color: #fff; }
    </style>
    
    <!-- Floating Particles -->
    <div class="particle p1"></div><div class="particle p2"></div><div class="particle p3"></div>
    <div class="particle p4"></div><div class="particle p5"></div><div class="particle p6"></div>
    <div class="particle p7"></div><div class="particle p8"></div>
    
    <!-- Top Navigation Bar -->
    <div class="top-nav">
        <div class="nav-logo">
            <div style='width:28px;height:28px;border-radius:6px;background:linear-gradient(135deg,#00d2ff,#a855f7);display:flex;align-items:center;justify-content:center;box-shadow:0 0 12px rgba(0,210,255,0.5);'>
                <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="#ffffff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" style="display: block;"><path d="M6 18V6L18 18V6" /></svg>
            </div>
            <span style='font-size:1.3rem;font-weight:700;color:#fff;letter-spacing:-0.02em;'>NovaAgent</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br><br><br><br>", unsafe_allow_html=True)
    
    # --- HERO SECTION ---
    # Shimmer animation CSS for gradient text
    st.markdown("""
    <style>
    @keyframes shimmer-gradient {
        0% { background-position: 0% center; }
        100% { background-position: -300% center; }
    }
    .hero-gradient-text {
        background: linear-gradient(120deg, #22d3ee, #a78bfa, #f472b6, #22d3ee) !important;
        background-size: 300% 100% !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        animation: shimmer-gradient 4s linear infinite !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center; position:relative; z-index:5; padding: 0 1rem; max-width: 800px; margin: 0 auto;">
        <h1 style="font-size:4.5rem; font-weight:800; letter-spacing:-0.05em; margin:0; line-height:1.05; text-shadow: 0 0 60px rgba(0,210,255,0.2);">
            Your AI Agents,<br>
            <span class="hero-gradient-text">Ready to Work.</span>
        </h1>
        <p style="font-size:1.2rem; color:#a1a1aa; max-width:600px; margin:1.5rem auto 0 auto; line-height:1.7; font-weight:300;">
            Deploy a suite of specialized AI agents that plan, analyze, learn, and execute — so you can focus on what matters most.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Custom CSS to style the native Streamlit button directly using sibling selectors
    st.markdown("""
    <style>
    /* Select the Streamlit button element container directly following our trigger div */
    div:has(#get-started-trigger) + div {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
        margin-top: 1rem !important;
        position: relative !important;
        z-index: 100 !important;
    }
    div:has(#get-started-trigger) + div > div {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
    }
    div:has(#get-started-trigger) + div .stButton {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
    }
    div:has(#get-started-trigger) + div button {
        background: linear-gradient(90deg, #00d2ff, #a855f7, #ec4899) !important;
        background-size: 200% 200% !important;
        animation: btn-glow-shift 3s ease infinite !important;
        border: none !important;
        color: #fff !important;
        border-radius: 50px !important;
        padding: 0.8rem 3.5rem !important;
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.03em !important;
        box-shadow: 0 0 25px rgba(0,210,255,0.4), 0 0 50px rgba(168,85,247,0.2) !important;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        height: auto !important;
        width: auto !important;
    }
    div:has(#get-started-trigger) + div button:hover {
        transform: scale(1.08) translateY(-3px) !important;
        box-shadow: 0 0 35px rgba(0,210,255,0.6), 0 0 70px rgba(168,85,247,0.4) !important;
        color: #ffffff !important;
    }
    div:has(#get-started-trigger) + div button:active {
        transform: scale(0.97) translateY(-1px) !important;
    }
    div:has(#get-started-trigger) + div button p {
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        margin: 0 !important;
    }
    @keyframes btn-glow-shift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    </style>
    """, unsafe_allow_html=True)

    # Trigger marker
    st.markdown('<div id="get-started-trigger"></div>', unsafe_allow_html=True)
    
    # Native Streamlit Button (which gets styled to look like our custom button)
    if st.button("Get Started →", key="get_started_action_btn"):
        st.session_state.view = 'Hub'
        st.rerun()
    
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    
    # --- STATS ROW ---
    st.markdown("""
    <div style="display:flex; justify-content:center; gap:5rem; position:relative; z-index:5; padding: 2rem 0; border-top:1px solid rgba(255,255,255,0.06); border-bottom:1px solid rgba(255,255,255,0.06);">
        <div class="stat-item">
            <div class="stat-num text-gradient">5</div>
            <div class="stat-label">AI Agents</div>
        </div>
        <div class="stat-item">
            <div class="stat-num" style="color:#22c55e;">99.9%</div>
            <div class="stat-label">Uptime</div>
        </div>
        <div class="stat-item">
            <div class="stat-num text-gradient">RAG</div>
            <div class="stat-label">Powered</div>
        </div>
        <div class="stat-item">
            <div class="stat-num" style="color:#eab308;">&lt;20ms</div>
            <div class="stat-label">Latency</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # --- FEATURE CARDS ---
    st.markdown("<h2 style='text-align:center; font-size:2.5rem; letter-spacing:-0.03em; margin-bottom:0.5rem; position:relative; z-index:5;'>Powered by <span class='text-gradient'>Specialized Intelligence</span></h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#a1a1aa; margin-bottom:3rem; position:relative; z-index:5;'>Each agent is purpose-built with domain expertise and RAG-enhanced knowledge.</p>", unsafe_allow_html=True)
    
    feat_cols = st.columns(4)
    features = [
        {"icon": "⚡", "title": "Lightning Fast", "desc": "Streaming responses powered by Gemini with sub-20ms inference latency.", "color": "#00d2ff"},
        {"icon": "🧠", "title": "RAG Enhanced", "desc": "Retrieval-augmented generation from curated domain-specific knowledge bases.", "color": "#a855f7"},
        {"icon": "🔒", "title": "Secure & Local", "desc": "Your API keys and data never leave your machine. Full privacy by design.", "color": "#22c55e"},
        {"icon": "🎯", "title": "Task Specialized", "desc": "5 dedicated agents, each an expert in their domain — from legal to health.", "color": "#ec4899"},
    ]
    for i, feat in enumerate(features):
        with feat_cols[i]:
            st.markdown(f"""
            <div class="feat-card" style="--fc:{feat['color']};">
                <div class="feat-icon" style="--fc:{feat['color']};">{feat['icon']}</div>
                <h3 style="font-size:1.1rem; margin-bottom:0.5rem;">{feat['title']}</h3>
                <p style="font-size:0.9rem; line-height:1.6;">{feat['desc']}</p>
            </div>
            """, unsafe_allow_html=True)

elif view == 'Hub':
    st.markdown("<h1 style='margin-bottom: 0.5rem; font-size: 3rem;' class='text-gradient'>Modules Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #a1a1aa; font-size: 1.1rem; margin-bottom: 2rem;'>System Overview and active neural link management.</p>", unsafe_allow_html=True)
    
    # System Status Row
    stat_cols = st.columns(3)
    with stat_cols[0]:
        st.markdown("""
        <div class="dash-stat-box">
            <div style="width:10px; height:10px; border-radius:50%; background:#00d2ff; box-shadow: 0 0 10px #00d2ff;"></div>
            <div>
                <div style="font-size:0.8rem; color:#a1a1aa; text-transform:uppercase;">Core Network</div>
                <div style="font-size:1.2rem; font-weight:600; color:#fff;">ONLINE</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with stat_cols[1]:
        st.markdown("""
        <div class="dash-stat-box">
            <div style="width:10px; height:10px; border-radius:50%; background:#a855f7; box-shadow: 0 0 10px #a855f7;"></div>
            <div>
                <div style="font-size:0.8rem; color:#a1a1aa; text-transform:uppercase;">Active Agents</div>
                <div style="font-size:1.2rem; font-weight:600; color:#fff;">5 / 5</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with stat_cols[2]:
        st.markdown("""
        <div class="dash-stat-box">
            <div style="width:10px; height:10px; border-radius:50%; background:#22c55e; box-shadow: 0 0 10px #22c55e;"></div>
            <div>
                <div style="font-size:0.8rem; color:#a1a1aa; text-transform:uppercase;">Avg Latency</div>
                <div style="font-size:1.2rem; font-weight:600; color:#fff;">16.2 ms</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br><hr style='border-color: rgba(255,255,255,0.05);'><br>", unsafe_allow_html=True)
    
    agents = list(AGENT_MAPPING.items())
    for i in range(0, len(agents), 2):
        cols = st.columns(2)
        
        # Left card (Column 1)
        with cols[0]:
            agent_id, info = agents[i]
            st.markdown(textwrap.dedent(f"""
            <div class="glass-card agent-card" style="--agent-color: {info['color']}; height: 580px; display: flex; flex-direction: column;">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.25rem;">
                    <div style="display: flex; align-items: center;">
                        <div class="agent-3d-core">
                            <div class="ring ring-x"></div>
                            <div class="ring ring-y"></div>
                            <div class="ring ring-z"></div>
                            <div class="core-dot"></div>
                        </div>
                        <div>
                            <h3 style="margin:0; font-size:1.4rem; color:#fff;">{info['name']}</h3>
                            <div class="agent-role" style="color:{info['color']}; border-color:{info['color']}40; background:{info['color']}10;">{info['role']}</div>
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <div style="color: #22c55e; font-size: 0.8rem; font-weight: 600; display:flex; align-items:center; gap:4px; justify-content:flex-end;">
                            <span style="width:6px; height:6px; border-radius:50%; background:#22c55e; display:inline-block; box-shadow: 0 0 5px #22c55e;"></span> {info['status']}
                        </div>
                        <div style="color: #a1a1aa; font-size: 0.7rem;">PING: {info['latency']}</div>
                    </div>
                </div>
                <div style="font-size: 1rem; line-height: 1.6; color: #a1a1aa; margin-bottom: 1.5rem;">{info['description']}</div>
                <div style="margin-top: auto;">
                    <div style="font-size:0.8rem; color:#71717a; font-weight: 700; margin-bottom:0.75rem; letter-spacing:0.05em;">CAPABILITIES</div>
                    <div style="display:flex; gap:8px; flex-wrap:wrap; margin-bottom: 5.5rem;">
                        {''.join([f'<span style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; color: #d4d4d8;">{cap}</span>' for cap in info['capabilities']])}
                    </div>
                </div>
            </div>
            """).strip(), unsafe_allow_html=True)
            
            st.markdown(textwrap.dedent(f"""
            <div id="trigger-{agent_id}"></div>
            """).strip(), unsafe_allow_html=True)
            if st.button(f"Initialize {info['name']}", key=f"launch_{agent_id}", use_container_width=True):
                st.session_state.active_agent = agent_id
                st.session_state.view = 'Chat'
                st.rerun()

        # Right card (Column 2)
        with cols[1]:
            if i + 1 < len(agents):
                agent_id, info = agents[i+1]
                st.markdown(textwrap.dedent(f"""
                <div class="glass-card agent-card" style="--agent-color: {info['color']}; height: 580px; display: flex; flex-direction: column;">
                    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.25rem;">
                        <div style="display: flex; align-items: center;">
                            <div class="agent-3d-core">
                                <div class="ring ring-x"></div>
                                <div class="ring ring-y"></div>
                                <div class="ring ring-z"></div>
                                <div class="core-dot"></div>
                            </div>
                            <div>
                                <h3 style="margin:0; font-size:1.4rem; color:#fff;">{info['name']}</h3>
                                <div class="agent-role" style="color:{info['color']}; border-color:{info['color']}40; background:{info['color']}10;">{info['role']}</div>
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <div style="color: #22c55e; font-size: 0.8rem; font-weight: 600; display:flex; align-items:center; gap:4px; justify-content:flex-end;">
                                <span style="width:6px; height:6px; border-radius:50%; background:#22c55e; display:inline-block; box-shadow: 0 0 5px #22c55e;"></span> {info['status']}
                            </div>
                            <div style="color: #a1a1aa; font-size: 0.7rem;">PING: {info['latency']}</div>
                        </div>
                    </div>
                    <div style="font-size: 1rem; line-height: 1.6; color: #a1a1aa; margin-bottom: 1.5rem;">{info['description']}</div>
                    <div style="margin-top: auto;">
                        <div style="font-size:0.8rem; color:#71717a; font-weight: 700; margin-bottom:0.75rem; letter-spacing:0.05em;">CAPABILITIES</div>
                        <div style="display:flex; gap:8px; flex-wrap:wrap; margin-bottom: 5.5rem;">
                            {''.join([f'<span style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; color: #d4d4d8;">{cap}</span>' for cap in info['capabilities']])}
                        </div>
                    </div>
                </div>
                """).strip(), unsafe_allow_html=True)
                
                st.markdown(textwrap.dedent(f"""
                <div id="trigger-{agent_id}"></div>
                """).strip(), unsafe_allow_html=True)
                if st.button(f"Initialize {info['name']}", key=f"launch_{agent_id}", use_container_width=True):
                    st.session_state.active_agent = agent_id
                    st.session_state.view = 'Chat'
                    st.rerun()
            else:
                st.markdown('<div style="height: 100%;"></div>', unsafe_allow_html=True)

elif view == 'Settings':
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

elif view == 'Chat':
    agent_id = st.session_state.active_agent
    info = AGENT_MAPPING[agent_id]
    
    st.markdown(f"""
    <div class="glass-card" style="--agent-color: {info['color']}; padding: 1rem 1.5rem; margin-bottom: 2rem; display: flex; flex-direction: row; align-items: center; height: auto;">
        <div class="agent-3d-core" style="width: 48px; height: 48px; transform: scale(0.8);">
            <div class="ring ring-x"></div>
            <div class="ring ring-y"></div>
            <div class="ring ring-z"></div>
            <div class="core-dot"></div>
        </div>
        <div>
            <h2 style='margin:0;' class='text-gradient'>{info['name']}</h2>
            <div style='color:{info['color']}; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.1em; font-weight: 600;'>{info['role']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Helper to generate animated 3D core SVG avatars matching the Hub page style
    def get_svg_avatar_base64(color_hex):
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <defs>
    <radialGradient id="glow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#ffffff" />
      <stop offset="40%" stop-color="{color_hex}" />
      <stop offset="100%" stop-color="transparent" />
    </radialGradient>
  </defs>
  <!-- Glowing background space -->
  <circle cx="50" cy="50" r="30" fill="url(#glow)" opacity="0.35" />
  
  <!-- Outer Spinning Dashed Ring -->
  <ellipse cx="50" cy="50" rx="42" ry="15" fill="none" stroke="{color_hex}" stroke-width="2" stroke-dasharray="6 6">
    <animateTransform attributeName="transform" type="rotate" from="0 50 50" to="360 50 50" dur="8s" repeatCount="indefinite" />
  </ellipse>
  
  <!-- Inner Orbiting Solid Ring 1 (Tilted X) -->
  <ellipse cx="50" cy="50" rx="36" ry="12" fill="none" stroke="{color_hex}" stroke-width="2.5" transform="rotate(45 50 50)">
    <animateTransform attributeName="transform" type="rotate" from="45 50 50" to="405 50 50" dur="5s" repeatCount="indefinite" />
  </ellipse>

  <!-- Inner Orbiting Solid Ring 2 (Tilted Z) -->
  <ellipse cx="50" cy="50" rx="36" ry="12" fill="none" stroke="{color_hex}" stroke-width="2.5" transform="rotate(-45 50 50)">
    <animateTransform attributeName="transform" type="rotate" from="-45 50 50" to="-405 50 50" dur="4s" repeatCount="indefinite" />
  </ellipse>
  
  <!-- Glowing central dot -->
  <circle cx="50" cy="50" r="14" fill="url(#glow)" opacity="0.8">
    <animate attributeName="r" values="10;15;10" dur="2s" repeatCount="indefinite" />
  </circle>
  <circle cx="50" cy="50" r="6" fill="#ffffff" />
</svg>"""
        encoded = base64.b64encode(svg.encode('utf-8')).decode('utf-8')
        return f"data:image/svg+xml;base64,{encoded}"

    def get_user_svg_avatar_base64():
        color = "#94a3b8"
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <defs>
    <radialGradient id="userGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#64748b" />
      <stop offset="100%" stop-color="transparent" />
    </radialGradient>
  </defs>
  <circle cx="50" cy="50" r="45" fill="url(#userGlow)" opacity="0.25" />
  <circle cx="50" cy="50" r="40" fill="none" stroke="{color}" stroke-width="2" opacity="0.3" />
  <path d="M50 45c5.5 0 10-4.5 10-10s-4.5-10-10-10-10 4.5-10 10 4.5 10 10 10zm0 8c-9.3 0-28 4.7-28 14v6h56v-6c0-9.3-18.7-14-28-14z" fill="{color}" />
</svg>"""
        encoded = base64.b64encode(svg.encode('utf-8')).decode('utf-8')
        return f"data:image/svg+xml;base64,{encoded}"

    agent_avatar_url = get_svg_avatar_base64(info['color'])
    user_avatar_url = get_user_svg_avatar_base64()

    # Inject agent-specific style variable wrapper
    st.markdown(f"""
    <div class="agent-chat-wrapper" style="--chat-agent-color: {info['color']}">
    """, unsafe_allow_html=True)
    
    chat_container = st.container(height=600)
    with chat_container:
        for msg in st.session_state.chat_history[agent_id]:
            avatar_url = agent_avatar_url if msg["role"] == "assistant" else user_avatar_url
            with st.chat_message(msg["role"], avatar=avatar_url):
                if msg["role"] == "assistant":
                    st.markdown(f'<div class="chat-name-label chat-name-agent" style="--agent-chat-color: {info["color"]}"><span class="chat-dot"></span>{info["name"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="chat-name-label chat-name-user"><span class="chat-dot"></span>You</div>', unsafe_allow_html=True)
                st.markdown(msg["content"])
                
    if prompt := st.chat_input("Transmit message..."):
        st.session_state.chat_history[agent_id].append({"role": "user", "content": prompt})
        with chat_container:
            with st.chat_message("user", avatar=user_avatar_url):
                st.markdown('<div class="chat-name-label chat-name-user"><span class="chat-dot"></span>You</div>', unsafe_allow_html=True)
                st.markdown(prompt)
                
            with st.chat_message("assistant", avatar=agent_avatar_url):
                st.markdown(f'<div class="chat-name-label chat-name-agent" style="--agent-chat-color: {info["color"]}"><span class="chat-dot"></span>{info["name"]}</div>', unsafe_allow_html=True)
                response_placeholder = st.empty()
                api_key = st.session_state.gemini_key.strip().strip('\"\'')

                
                if not api_key:
                    error_msg = "Error: API Key not configured. Please visit Settings."
                    response_placeholder.markdown(error_msg)
                    st.session_state.chat_history[agent_id].append({"role": "assistant", "content": error_msg})
                else:
                    context_str = "No internal documentation retrieved."
                    retriever = retrievers.get(agent_id)
                    if retriever:
                        results = retriever.retrieve(prompt, top_k=5)
                        retrieved = [f"### {c['header']}\n{c['content']}" for c, s in results if s > 0.05]
                        if retrieved: context_str = "\n\n".join(retrieved)
                            
                    skill_content = ""
                    skill_file = info.get("skill_file")
                    if skill_file:
                        paths = [f"backend/data/rag_documents/{skill_file}", f"backend/{skill_file}", skill_file]
                        skill_path = next((p for p in paths if os.path.exists(p)), None)
                        if skill_path:
                            with open(skill_path, "r", encoding="utf-8") as f:
                                skill_content = f.read()
                    
                    if not skill_content:
                        skill_content = f"You are {info['name']}, {info['role']}. {info['description']}"
                        
                    sys_prompt = f"""{skill_content}

RETRIEVED CONTEXT FROM RAG KNOWLEDGE BASE:
---
{context_str}
---

CRITICAL DIRECTIVES:
1. Respond in character, adhering to your identity, communication rules, and core beliefs.
2. NEVER add headers like "🤖 NAME | Company responds:" or decorative lines (─────).
3. NEVER add a signature line at the end like "— Name, Title @ Company".
4. Respond naturally and professionally — like a real CEO/founder having a genuine conversation.
5. Just speak directly. No role-play formatting. Clean, articulate, professional responses."""
                    
                    gemini_failed = False
                    groq_key = st.session_state.groq_key.strip().strip('"\'')
                    response_generated = False
                    
                    # --- Helper: Try Groq ---
                    def try_groq(placeholder, system_prompt, user_prompt, groq_api_key, status_msg=""):
                        """Attempt to generate response using Groq. Returns (success, response_text)."""
                        if not groq_api_key:
                            return False, ""
                        try:
                            if status_msg:
                                placeholder.markdown(status_msg)
                            import groq as groq_sdk
                            client = groq_sdk.Groq(api_key=groq_api_key)
                            
                            # Try multiple Groq models
                            groq_models = ['llama-3.3-70b-versatile', 'llama3-70b-8192', 'llama3-8b-8192', 'mixtral-8x7b-32768']
                            last_groq_err = None
                            for groq_model in groq_models:
                                try:
                                    chat_completion = client.chat.completions.create(
                                        model=groq_model,
                                        messages=[
                                            {"role": "system", "content": system_prompt},
                                            {"role": "user", "content": user_prompt}
                                        ],
                                        stream=True
                                    )
                                    
                                    full_res = ""
                                    for chunk in chat_completion:
                                        if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                                            delta = chunk.choices[0].delta.content
                                            full_res += delta
                                            placeholder.markdown(full_res + "▌")
                                    if full_res:
                                        placeholder.markdown(full_res)
                                        return True, full_res
                                    else:
                                        continue
                                except Exception as model_err:
                                    last_groq_err = model_err
                                    err_str = str(model_err).lower()
                                    if "api_key" in err_str or "authentication" in err_str or "invalid" in err_str:
                                        raise model_err
                                    continue
                            return False, f"All Groq models failed. Last error: {last_groq_err}"
                        except Exception as groq_err:
                            return False, str(groq_err)
                    
                    # --- Helper: Try Gemini ---
                    def try_gemini(placeholder, system_prompt, user_prompt, gemini_api_key):
                        """Attempt to generate response using Gemini. Returns (success, response_text, is_quota_error)."""
                        try:
                            import google.generativeai as genai
                            genai.configure(api_key=gemini_api_key)
                            
                            model_names = ['gemini-2.0-flash-lite', 'gemini-2.0-flash']
                            response_stream = None
                            first_chunk = None
                            
                            for model_name in model_names:
                                try:
                                    model = genai.GenerativeModel(model_name)
                                    stream = model.generate_content(f"{system_prompt}\n\nUser Query: {user_prompt}", stream=True)
                                    first_chunk = next(iter(stream))
                                    response_stream = stream
                                    break
                                except Exception as model_err:
                                    err_str = str(model_err).lower()
                                    if any(kw in err_str for kw in ["api key", "api_key", "invalid key", "credentials", "unauthorized", "forbidden", "permission"]):
                                        return False, f"⚠️ **API Key Invalid**: The configured Gemini API key is not valid. Please go to **Settings** to configure a valid API key.", False
                                    if any(kw in err_str for kw in ["quota", "rate limit", "429", "exhausted", "resourceexhausted"]):
                                        return False, "quota_exhausted", True
                                    if "404" in err_str or "not found" in err_str or "not supported" in err_str:
                                        continue
                                    else:
                                        return False, str(model_err), False
                            
                            if response_stream is None or first_chunk is None:
                                return False, "quota_exhausted", True
                            
                            full_res = first_chunk.text if first_chunk.text else ""
                            placeholder.markdown(full_res + "▌")
                            for chunk in response_stream:
                                if chunk.text:
                                    full_res += chunk.text
                                    placeholder.markdown(full_res + "▌")
                            placeholder.markdown(full_res)
                            return True, full_res, False
                            
                        except Exception as e:
                            err_lower = str(e).lower()
                            is_quota = any(kw in err_lower for kw in ["quota", "rate limit", "429", "exhausted"])
                            return False, str(e), is_quota
                    
                    # ---- STRATEGY: Smart provider selection ----
                    # If Gemini quota was previously exhausted, try Groq first
                    if st.session_state.gemini_quota_exhausted and groq_key:
                        response_placeholder.markdown("⚡ Connecting via **Groq (Llama 3)**...")
                        success, result = try_groq(response_placeholder, sys_prompt, prompt, groq_key, "⚡ Generating response via **Groq (Llama 3)**...")
                        if success:
                            st.session_state.chat_history[agent_id].append({"role": "assistant", "content": result})
                            response_generated = True
                        else:
                            # Groq also failed, try Gemini as fallback (maybe quota reset)
                            response_placeholder.markdown("⏳ Groq unavailable, retrying **Gemini**...")
                            success, result, is_quota = try_gemini(response_placeholder, sys_prompt, prompt, api_key)
                            if success:
                                st.session_state.gemini_quota_exhausted = False
                                st.session_state.chat_history[agent_id].append({"role": "assistant", "content": result})
                                response_generated = True
                            else:
                                if is_quota:
                                    error_msg = ("⚠️ **Both AI providers are currently unavailable.**\n\n"
                                                f"**Gemini**: Quota exhausted (free tier daily limit reached)\n"
                                                f"**Groq**: {result}\n\n"
                                                "**To fix this:**\n"
                                                "1. Get a **new free Groq API key** at [console.groq.com/keys](https://console.groq.com/keys) and update it in **Settings**\n"
                                                "2. Or generate a **new Gemini key** from a different project at [Google AI Studio](https://aistudio.google.com/apikey)\n"
                                                "3. Or **wait** for the daily quota reset (midnight PT)")
                                else:
                                    error_msg = f"⚠️ **Error**: {result}"
                                response_placeholder.markdown(error_msg)
                                st.session_state.chat_history[agent_id].append({"role": "assistant", "content": error_msg})
                                response_generated = True
                    
                    # Default: Try Gemini first
                    if not response_generated:
                        success, result, is_quota = try_gemini(response_placeholder, sys_prompt, prompt, api_key)
                        if success:
                            st.session_state.chat_history[agent_id].append({"role": "assistant", "content": result})
                            response_generated = True
                        elif is_quota:
                            st.session_state.gemini_quota_exhausted = True
                            # Try Groq fallback
                            if groq_key:
                                success, groq_result = try_groq(response_placeholder, sys_prompt, prompt, groq_key, "⏳ Gemini quota exhausted. Switching to **Groq (Llama 3)** fallback...")
                                if success:
                                    st.session_state.chat_history[agent_id].append({"role": "assistant", "content": groq_result})
                                    response_generated = True
                                else:
                                    error_msg = ("⚠️ **Both AI providers failed.**\n\n"
                                                f"**Gemini**: Quota exhausted\n"
                                                f"**Groq**: {groq_result}\n\n"
                                                "**To fix this:**\n"
                                                "1. Get a **new free Groq API key** at [console.groq.com/keys](https://console.groq.com/keys) and update in **Settings**\n"
                                                "2. Or generate a **new Gemini key** at [Google AI Studio](https://aistudio.google.com/apikey)\n"
                                                "3. Or **wait** for daily quota reset (midnight PT)")
                                    response_placeholder.markdown(error_msg)
                                    st.session_state.chat_history[agent_id].append({"role": "assistant", "content": error_msg})
                                    response_generated = True
                            else:
                                error_msg = ("⚠️ **Gemini Quota Exhausted** — No Groq fallback configured.\n\n"
                                            "Your Gemini free tier daily quota is used up. To fix this:\n\n"
                                            "1. **Add a free Groq API key** in **Settings** — get one at [console.groq.com/keys](https://console.groq.com/keys)\n"
                                            "2. **Create a new Gemini key** from a different project at [Google AI Studio](https://aistudio.google.com/apikey)\n"
                                            "3. **Wait** for daily quota reset (midnight PT)")
                                response_placeholder.markdown(error_msg)
                                st.session_state.chat_history[agent_id].append({"role": "assistant", "content": error_msg})
                                response_generated = True
                        else:
                            # Non-quota Gemini error
                            error_msg = f"⚠️ **Error**: {result}"
                            response_placeholder.markdown(error_msg)
                            st.session_state.chat_history[agent_id].append({"role": "assistant", "content": error_msg})
                            response_generated = True

    # Close the agent-chat-wrapper div
    st.markdown("</div>", unsafe_allow_html=True)
