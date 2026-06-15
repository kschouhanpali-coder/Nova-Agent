import streamlit as st


def inject_custom_css(current_view):
    """Inject the spectacular CSS theme and background elements."""
    from config import AGENT_MAPPING
    active_agent = st.session_state.get('active_agent', 'planner')
    agent_info = AGENT_MAPPING.get(active_agent, AGENT_MAPPING['planner'])
    agent_color = agent_info['color']

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
        [data-testid="stAppViewContainer"], [data-testid="stHeader"], .main, [data-testid="stAppViewBlockContainer"], [data-testid="stBottom"], [data-testid="stBottom"] > div, div.stChatInputContainer {{
            background: transparent !important;
            background-color: transparent !important;
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
        
        /* Premium Flat Sidebar Buttons */
        [data-testid="stSidebar"] .stButton > button {{
            background: rgba(255, 255, 255, 0.03) !important;
            border: 1px solid rgba(255, 255, 255, 0.04) !important;
            justify-content: flex-start !important;
            padding: 0.8rem 1.2rem !important;
            color: #94a3b8 !important;
            font-size: 0.95rem !important;
            font-weight: 500 !important;
            border-radius: 12px !important;
            box-shadow: none !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            margin-bottom: 0.5rem !important;
        }}
        
        [data-testid="stSidebar"] .stButton > button:hover {{
            background: rgba(255, 255, 255, 0.06) !important;
            border-color: rgba(0, 210, 255, 0.35) !important;
            color: #ffffff !important;
            box-shadow: 0 4px 12px rgba(0, 210, 255, 0.15) !important;
        }}

        /* Active indicator selectors - Glowing cyan-purple gradient border and subtle inner glow */
        div:has(#active-hub) + div button,
        div:has(#active-chat) + div button,
        div:has(#active-settings) + div button {{
            background: linear-gradient(#0a0b18, #0a0b18) padding-box, linear-gradient(135deg, #00d2ff, #a855f7) border-box !important;
            border: 1px solid transparent !important;
            color: #ffffff !important;
            box-shadow: 0 0 15px rgba(0, 210, 255, 0.35), inset 0 0 10px rgba(168, 85, 247, 0.15) !important;
            font-weight: 600 !important;
        }}

        /* Active buttons hover */
        div:has(#active-hub) + div button:hover,
        div:has(#active-chat) + div button:hover,
        div:has(#active-settings) + div button:hover {{
            background: linear-gradient(#0c0d20, #0c0d20) padding-box, linear-gradient(135deg, #00d2ff, #a855f7) border-box !important;
            border: 1px solid transparent !important;
            color: #ffffff !important;
            box-shadow: 0 0 20px rgba(0, 210, 255, 0.5), inset 0 0 12px rgba(168, 85, 247, 0.2) !important;
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

        /* Ensure collapsed sidebar expander button is visible and styled beautifully */
        [data-testid="collapsedControl"] {{
            visibility: visible !important;
            background: rgba(10, 11, 24, 0.7) !important;
            backdrop-filter: blur(20px) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 8px !important;
            margin-top: 0.5rem !important;
            margin-left: 0.5rem !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
            transition: all 0.3s ease !important;
        }}
        [data-testid="collapsedControl"]:hover {{
            border-color: rgba(6, 182, 212, 0.4) !important;
            box-shadow: 0 4px 20px rgba(6, 182, 212, 0.25) !important;
        }}

        /* Premium custom styling for Sidebar Expanders to match navigation buttons */
        [data-testid="stSidebar"] [data-testid="stExpander"] {{
            background: rgba(255, 255, 255, 0.04) !important;
            border: 1px solid rgba(255, 255, 255, 0.06) !important;
            border-radius: 12px !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2), inset 0 1px 0 rgba(255,255,255,0.05) !important;
            margin-bottom: 0.5rem !important;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        }}
        [data-testid="stSidebar"] [data-testid="stExpander"] > details {{
            border: none !important;
        }}
        [data-testid="stSidebar"] [data-testid="stExpander"] summary {{
            padding: 0.8rem 1.2rem !important;
            color: #cbd5e1 !important;
            font-size: 1rem !important;
            font-weight: 500 !important;
            background: transparent !important;
        }}
        [data-testid="stSidebar"] [data-testid="stExpander"] summary:hover {{
            color: #ffffff !important;
        }}
        [data-testid="stSidebar"] [data-testid="stExpander"] [data-testid="stExpanderDetails"] {{
            padding: 1rem !important;
            background: rgba(0, 0, 0, 0.2) !important;
            border-bottom-left-radius: 12px !important;
            border-bottom-right-radius: 12px !important;
        }}

        .block-container {{ padding-top: 3rem; padding-bottom: 3rem; max-width: 1200px; position: relative; z-index: 5; }}

        /* Unified Settings Inputs Panel inside Dashboard */
        .hub-settings-inputs-wrapper {{
            background: rgba(255, 255, 255, 0.03) !important;
            border-left: 1px solid rgba(255, 255, 255, 0.06) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.06) !important;
            padding: 0.5rem 1.5rem 1.5rem 1.5rem !important;
            margin-top: 0px !important;
            margin-bottom: 0px !important;
            backdrop-filter: blur(28px) saturate(160%) !important;
            -webkit-backdrop-filter: blur(28px) saturate(160%) !important;
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.02) !important;
        }}
        
        /* Premium custom labels inside the inputs area */
        .hub-settings-inputs-wrapper label {{
            font-size: 0.85rem !important;
            color: #94a3b8 !important;
            font-weight: 600 !important;
            letter-spacing: 0.02em !important;
        }}

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

        /* Chat messages styling (Outer layout) */
        [data-testid="stChatMessage"] {{
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
            display: flex !important;
            gap: 16px !important;
            align-items: flex-start !important;
            margin-bottom: 1.25rem !important;
            padding: 0 !important;
        }}

        /* Chat messages bubble content (The actual text box) */
        [data-testid="stChatMessageContent"] {{
            background-color: rgba(255, 255, 255, 0.03) !important;
            border: 1px solid rgba(255, 255, 255, 0.06) !important;
            border-radius: 16px !important;
            padding: 1.2rem 1.5rem !important;
            transition: all 0.3s ease !important;
            color: #cbd5e1 !important;
            flex-grow: 1 !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15) !important;
        }}
        [data-testid="stChatMessageContent"]:hover {{
            background-color: rgba(255, 255, 255, 0.05) !important;
            border-color: rgba(255, 255, 255, 0.1) !important;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.25) !important;
        }}

        /* Ensure message body paragraphs/lists/spans are clean off-white readable color with neat typography */
        [data-testid="stChatMessageContent"] p,
        [data-testid="stChatMessageContent"] li,
        [data-testid="stChatMessageContent"] span:not(.chat-dot),
        [data-testid="stChatMessageContent"] strong {{
            color: #e2e8f0 !important;
            font-size: 0.98rem !important;
            line-height: 1.75 !important;
        }}

        /* Bold text stands out with a brighter color */
        [data-testid="stChatMessageContent"] strong {{
            color: #ffffff !important;
            font-weight: 700 !important;
        }}

        /* High-end markdown formatting inside the chat bubble */
        [data-testid="stChatMessageContent"] [data-testid="stMarkdownContainer"] p:last-child {{
            margin-bottom: 0 !important;
        }}
        [data-testid="stChatMessageContent"] [data-testid="stMarkdownContainer"] p {{
            margin-bottom: 0.6rem !important;
        }}

        /* Headings inside chat */
        [data-testid="stChatMessageContent"] [data-testid="stMarkdownContainer"] h1 {{
            font-size: 1.3rem !important;
            font-weight: 700 !important;
            margin-top: 1.2rem !important;
            margin-bottom: 0.6rem !important;
            color: #ffffff !important;
            background: linear-gradient(135deg, #00d2ff, #a855f7) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            background-clip: text !important;
        }}
        [data-testid="stChatMessageContent"] [data-testid="stMarkdownContainer"] h2 {{
            font-size: 1.15rem !important;
            font-weight: 700 !important;
            margin-top: 1.1rem !important;
            margin-bottom: 0.5rem !important;
            color: #ffffff !important;
        }}
        [data-testid="stChatMessageContent"] [data-testid="stMarkdownContainer"] h3 {{
            font-size: 1.05rem !important;
            font-weight: 600 !important;
            margin-top: 1rem !important;
            margin-bottom: 0.4rem !important;
            color: #e2e8f0 !important;
        }}

        /* Unordered lists — custom bullet styling */
        [data-testid="stChatMessageContent"] ul {{
            list-style: none !important;
            padding-left: 1rem !important;
            margin: 0.5rem 0 0.8rem 0 !important;
        }}
        [data-testid="stChatMessageContent"] ul li {{
            position: relative !important;
            padding-left: 1rem !important;
            margin-bottom: 0.4rem !important;
        }}
        [data-testid="stChatMessageContent"] ul li::before {{
            content: '▸' !important;
            position: absolute !important;
            left: 0 !important;
            color: #00d2ff !important;
            font-weight: bold !important;
            font-size: 0.9rem !important;
        }}

        /* Ordered lists — styled numbers */
        [data-testid="stChatMessageContent"] ol {{
            padding-left: 1.2rem !important;
            margin: 0.5rem 0 0.8rem 0 !important;
            counter-reset: item !important;
            list-style: none !important;
        }}
        [data-testid="stChatMessageContent"] ol li {{
            counter-increment: item !important;
            position: relative !important;
            padding-left: 1.4rem !important;
            margin-bottom: 0.4rem !important;
        }}
        [data-testid="stChatMessageContent"] ol li::before {{
            content: counter(item) !important;
            position: absolute !important;
            left: 0 !important;
            background: linear-gradient(135deg, #00d2ff, #a855f7) !important;
            color: #0a0f1a !important;
            font-weight: 700 !important;
            font-size: 0.7rem !important;
            width: 1.2rem !important;
            height: 1.2rem !important;
            border-radius: 50% !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            top: 0.25rem !important;
        }}

        /* Nested list items — smaller, indented */
        [data-testid="stChatMessageContent"] ul ul,
        [data-testid="stChatMessageContent"] ol ul {{
            margin: 0.3rem 0 0.4rem 0.5rem !important;
        }}
        [data-testid="stChatMessageContent"] ul ul li::before {{
            content: '•' !important;
            color: #a855f7 !important;
        }}

        /* Blockquotes — glowing left border accent */
        [data-testid="stChatMessageContent"] blockquote {{
            border-left: 3px solid #00d2ff !important;
            background: rgba(0, 210, 255, 0.04) !important;
            margin: 0.8rem 0 !important;
            padding: 0.7rem 1rem !important;
            border-radius: 0 10px 10px 0 !important;
            box-shadow: -2px 0 12px rgba(0, 210, 255, 0.1) !important;
        }}
        [data-testid="stChatMessageContent"] blockquote p {{
            color: #cbd5e1 !important;
            font-style: italic !important;
            margin-bottom: 0 !important;
        }}

        /* Horizontal rules */
        [data-testid="stChatMessageContent"] hr {{
            border: none !important;
            height: 1px !important;
            background: linear-gradient(90deg, transparent, rgba(0, 210, 255, 0.3), rgba(168, 85, 247, 0.3), transparent) !important;
            margin: 1rem 0 !important;
        }}

        /* Inline code */
        [data-testid="stChatMessageContent"] [data-testid="stMarkdownContainer"] code {{
            background-color: rgba(0, 210, 255, 0.1) !important;
            color: #00d2ff !important;
            padding: 0.15rem 0.45rem !important;
            border-radius: 5px !important;
            font-family: 'JetBrains Mono', 'Fira Code', monospace !important;
            font-size: 0.88rem !important;
            border: 1px solid rgba(0, 210, 255, 0.15) !important;
        }}

        /* Code blocks (pre) */
        [data-testid="stChatMessageContent"] pre {{
            background: rgba(0, 0, 0, 0.4) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 10px !important;
            padding: 1rem !important;
            margin: 0.8rem 0 !important;
            overflow-x: auto !important;
        }}
        [data-testid="stChatMessageContent"] pre code {{
            background: transparent !important;
            border: none !important;
            padding: 0 !important;
            color: #e2e8f0 !important;
        }}

        /* Links inside chat */
        [data-testid="stChatMessageContent"] a {{
            color: #00d2ff !important;
            text-decoration: none !important;
            border-bottom: 1px dotted rgba(0, 210, 255, 0.4) !important;
            transition: all 0.2s ease !important;
        }}
        [data-testid="stChatMessageContent"] a:hover {{
            color: #a855f7 !important;
            border-bottom-color: #a855f7 !important;
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
            color: var(--agent-chat-color, #00d2ff) !important;
        }}
        .chat-name-user {{
            color: #94a3b8 !important;
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

        /* ===== Native SVG Chat Avatars - Clean and aligned outside the bubble ===== */
        .agent-chat-wrapper [data-testid="stChatMessageAvatar"] {{
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            width: 36px !important;
            height: 36px !important;
            flex-shrink: 0 !important;
            margin-top: 4px !important;
            overflow: hidden !important;
        }}
        .agent-chat-wrapper [data-testid="stChatMessageAvatar"] img {{
            width: 36px !important;
            height: 36px !important;
            border-radius: 50% !important;
            object-fit: contain !important;
            filter: drop-shadow(0 0 6px var(--chat-agent-color, #00d2ff)) !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }}
        .agent-chat-wrapper [data-testid="stChatMessageAvatar"] img:hover {{
            transform: scale(1.1) rotate(5deg) !important;
            filter: drop-shadow(0 0 10px var(--chat-agent-color, #00d2ff)) !important;
        }}
        /* User avatar specific shadow styling */
        .agent-chat-wrapper [data-testid="stChatMessage"]:has(.chat-name-user) [data-testid="stChatMessageAvatar"] img {{
            filter: drop-shadow(0 0 4px rgba(148, 163, 184, 0.4)) !important;
        }}
        .agent-chat-wrapper [data-testid="stChatMessage"]:has(.chat-name-user) [data-testid="stChatMessageAvatar"] img:hover {{
            transform: scale(1.1) rotate(-5deg) !important;
            filter: drop-shadow(0 0 8px rgba(148, 163, 184, 0.6)) !important;
        }}

        /* Premium Chat Input Container Overrides */
        [data-testid="stChatInput"] {{
            background-color: transparent !important;
            border: none !important;
            padding: 0 !important;
        }}
        [data-testid="stChatInput"] > div,
        [data-testid="stChatInput"] textarea {{
            background-color: rgba(15, 17, 36, 0.7) !important;
            color: #f8fafc !important;
            border: none !important;
        }}
        /* Intermediate layout container transparency */
        [data-testid="stChatInput"] div:not(:has(button)) {{
            background-color: transparent !important;
        }}
        [data-testid="stChatInput"] > div {{
            background-color: rgba(15, 17, 36, 0.7) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 16px !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255,255,255,0.05) !important;
            backdrop-filter: blur(20px) !important;
            -webkit-backdrop-filter: blur(20px) !important;
            padding: 6px 12px !important;
            transition: all 0.3s ease !important;
        }}
        [data-testid="stChatInput"] > div:focus-within {{
            border-color: {agent_color} !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4), 0 0 15px {agent_color}66, inset 0 1px 0 rgba(255,255,255,0.05) !important;
        }}
        [data-testid="stChatInput"] textarea {{
            color: #f8fafc !important;
            background-color: transparent !important;
            border: none !important;
            font-family: 'Outfit', sans-serif !important;
            font-size: 1rem !important;
            line-height: 1.5 !important;
            caret-color: {agent_color} !important;
        }}
        [data-testid="stChatInput"] textarea::placeholder {{
            color: #64748b !important;
        }}
        [data-testid="stChatInput"] button {{
            background-color: {agent_color} !important;
            border: 1px solid {agent_color} !important;
            color: #ffffff !important;
            border-radius: 50% !important;
            width: 32px !important;
            height: 32px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            transition: all 0.3s ease !important;
            margin-left: 8px !important;
            box-shadow: 0 0 10px {agent_color}66 !important;
        }}
        [data-testid="stChatInput"] button:hover {{
            background-color: #ffffff !important;
            border-color: #ffffff !important;
            color: {agent_color} !important;
            box-shadow: 0 0 15px rgba(255, 255, 255, 0.6) !important;
        }}
        [data-testid="stChatInput"] button svg {{
            fill: currentColor !important;
            stroke: currentColor !important;
        }}

        /* Premium Text Input & Password Input Overrides */
        div[data-testid="stTextInput"] {{
            margin-bottom: 1rem !important;
        }}
        div[data-testid="stTextInput"] label {{
            color: #94a3b8 !important;
            font-weight: 600 !important;
            font-size: 0.9rem !important;
            margin-bottom: 0.5rem !important;
        }}
        div[data-testid="stTextInput"] > div[data-baseweb="input"],
        div[data-testid="stTextInput"] div[data-baseweb="base-input"] {{
            background-color: rgba(15, 17, 36, 0.7) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 10px !important;
            color: #f8fafc !important;
            transition: all 0.3s ease !important;
        }}
        div[data-testid="stTextInput"] > div[data-baseweb="input"]:focus-within,
        div[data-testid="stTextInput"] div[data-baseweb="base-input"]:focus-within {{
            border-color: {agent_color} !important;
            box-shadow: 0 0 15px {agent_color}40 !important;
            background-color: rgba(15, 17, 36, 0.85) !important;
        }}
        div[data-testid="stTextInput"] input {{
            color: #f8fafc !important;
            background-color: transparent !important;
            font-family: 'Outfit', sans-serif !important;
            font-size: 0.95rem !important;
        }}
        div[data-testid="stTextInput"] button {{
            background-color: transparent !important;
            color: #cbd5e1 !important;
            border: none !important;
            transition: color 0.2s ease !important;
        }}
        div[data-testid="stTextInput"] button:hover {{
            color: #ffffff !important;
        }}
        div[data-testid="stTextInput"] button svg {{
            fill: currentColor !important;
        }}

        /* Premium Styling for general Streamlit buttons inside the main body container */
        div.stButton > button {{
            background-color: rgba(255, 255, 255, 0.04) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            color: #ffffff !important;
            border-radius: 8px !important;
            padding: 0.6rem 2rem !important;
            font-size: 0.95rem !important;
            font-weight: 500 !important;
            transition: all 0.3s ease !important;
            margin-top: 0.5rem !important;
            height: auto !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2) !important;
        }}
        div.stButton > button:hover {{
            background-color: rgba(255, 255, 255, 0.08) !important;
            border-color: {agent_color} !important;
            color: {agent_color} !important;
            box-shadow: 0 4px 15px {agent_color}40 !important;
        }}
        div.stButton > button:active {{
            transform: scale(0.98) !important;
        }}
        div.stButton > button p {{
            color: inherit !important;
            font-weight: inherit !important;
            font-size: inherit !important;
            margin: 0 !important;
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
