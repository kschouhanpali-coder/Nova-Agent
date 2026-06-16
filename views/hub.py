import streamlit as st
import textwrap

from config import AGENT_MAPPING


def render_hub():
    """Render the Modules Dashboard / Hub view."""
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
            _render_agent_card(agent_id, info)

        # Right card (Column 2)
        with cols[1]:
            if i + 1 < len(agents):
                agent_id, info = agents[i+1]
                _render_agent_card(agent_id, info)
            else:
                st.markdown('<div style="height: 100%;"></div>', unsafe_allow_html=True)


def _render_agent_card(agent_id, info):
    """Render a single agent card in the Hub dashboard."""
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
