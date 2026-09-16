import streamlit as st


def render_home():
    """Render the spectacular landing/home page."""
    # Inject extra landing-page-only CSS
    st.markdown("""
    <style>
    /* Full-screen hero adjustments */
    .block-container { max-width: 95% !important; padding-top: 0 !important; }
    

    
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
