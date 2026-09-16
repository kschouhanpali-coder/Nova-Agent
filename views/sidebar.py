import streamlit as st


def render_sidebar():
    """Render the sidebar navigation (only visible when not on Home view)."""
    with st.sidebar:
        # High-end Logo
        st.markdown("""
        <div style='display:flex; align-items:center; gap:12px; margin-bottom: 2.5rem; padding: 0.5rem;'>
            <div class="sidebar-logo-container" style='width: 32px; height: 32px; border-radius: 8px; background: linear-gradient(135deg, #00d2ff, #a855f7); display:flex; align-items:center; justify-content:center; box-shadow: 0 0 15px rgba(0,210,255,0.4); font-family: "Outfit", sans-serif; font-weight: 800; color: #ffffff; font-size: 1.15rem; line-height: 1;'>
                N
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
