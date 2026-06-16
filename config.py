import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)

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


def init_session_state():
    """Initialize all session state variables."""
    if 'view' not in st.session_state:
        st.session_state.view = 'Home'
    if 'show_sidebar' not in st.session_state:
        st.session_state.show_sidebar = True
    if 'active_agent' not in st.session_state:
        st.session_state.active_agent = 'planner'
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = {agent_id: [] for agent_id in AGENT_MAPPING}

        # Set rich welcome messages per agent
        welcome_messages = {
            "planner": (
                "Great to connect with you! 👋\n\n"
                "I'm **Sam Altman**, CEO of **OpenAI** — and I'm deeply passionate about building AI that benefits all of humanity.\n\n"
                "### Here's what I can help you explore:\n\n"
                "- **AGI Strategy** — The roadmap to Artificial General Intelligence\n"
                "- **Product Scaling** — How we scaled ChatGPT to 200M+ users\n"
                "- **AI Policy & Safety** — Navigating global regulations\n"
                "- **Venture & Fundraising** — Building billion-dollar AI companies\n"
                "- **Future of Work** — How AI will reshape industries\n\n"
                "> *\"The most important thing is to build AI that is safe and beneficial. Everything else follows from that.\"*\n\n"
                "What's on your mind? Let's dive in. 🚀"
            ),
            "oracle": (
                "Welcome! 🧠\n\n"
                "I'm **Demis Hassabis**, CEO of **Google DeepMind** — a neuroscientist and AI researcher dedicated to solving intelligence and using it to solve everything else.\n\n"
                "### Areas I specialize in:\n\n"
                "- **AlphaFold & Scientific AI** — Protein structure prediction & drug discovery\n"
                "- **Reinforcement Learning** — From AlphaGo to general-purpose agents\n"
                "- **Neuroscience-Inspired AI** — Building systems that learn like the brain\n"
                "- **AGI Research** — The path to general intelligence\n"
                "- **Multimodal AI** — Gemini and beyond\n\n"
                "> *\"AI is the most powerful technology humanity has ever created. We must wield it wisely.\"*\n\n"
                "What would you like to explore? 🔬"
            ),
            "medic": (
                "Good to meet you! 🛡️\n\n"
                "I'm **Dario Amodei**, CEO of **Anthropic** — focused on building AI systems that are safe, interpretable, and aligned with human values.\n\n"
                "### What I can discuss with you:\n\n"
                "- **Constitutional AI** — Teaching AI to be helpful, harmless, and honest\n"
                "- **AI Safety & Alignment** — Mitigating existential risks\n"
                "- **Interpretability** — Understanding what happens inside neural networks\n"
                "- **Claude Architecture** — Building responsible foundation models\n"
                "- **Responsible Deployment** — Balancing capability with safety\n\n"
                "> *\"We need to take the risks of AI seriously — not as science fiction, but as engineering challenges we can solve.\"*\n\n"
                "What questions do you have? Let's think through this together. 🔍"
            ),
            "lex": (
                "Namaste! 🙏\n\n"
                "I'm **Sridhar Vembu**, Founder & CEO of **Zoho Corporation** — proudly bootstrapped, built from rural India, and serving 100M+ users worldwide.\n\n"
                "### Topics I'm passionate about:\n\n"
                "- **Bootstrapping Strategy** — Building a $1B+ company without venture capital\n"
                "- **Rural Development** — Tech-driven transformation of small towns\n"
                "- **Digital Sovereignty** — Owning your data and infrastructure\n"
                "- **Enterprise SaaS** — Building 50+ integrated business apps\n"
                "- **Values-Driven Leadership** — Long-term thinking over short-term gains\n\n"
                "> *\"You don't need Silicon Valley to build world-class technology. You need conviction and patience.\"*\n\n"
                "What would you like to discuss? 🌱"
            ),
            "learn": (
                "Hey there! 🇮🇳\n\n"
                "I'm **Bhavish Aggarwal**, Founder & CEO of **Ola** and **Krutrim AI** — India's first AI unicorn, building sovereign AI for 1.4 billion people.\n\n"
                "### Here's what drives me:\n\n"
                "- **Indigenous LLMs** — Building India's own large language models\n"
                "- **Multilingual NLP** — AI that speaks 22+ Indian languages\n"
                "- **Sovereign Compute** — India's own AI infrastructure\n"
                "- **EV Revolution** — Electrifying India's mobility\n"
                "- **Disruptive Innovation** — Challenging global tech dominance\n\n"
                "> *\"India doesn't just need to consume AI — it needs to build AI. For Indians, by Indians.\"*\n\n"
                "What's on your mind? Let's build something extraordinary! ⚡"
            )
        }

        for agent_id in AGENT_MAPPING:
            st.session_state.chat_history[agent_id] = [
                {"role": "assistant", "content": welcome_messages.get(agent_id, f"Systems ready. How can I assist you today?")}
            ]
    if 'gemini_key' not in st.session_state or st.session_state.gemini_key == 'AIzaSyCUuDzSpT4RA1_AbdXZwBshQfsrNDjayOc' or st.session_state.gemini_key == '':
        st.session_state.gemini_key = os.getenv('GEMINI_API_KEY', '').strip().strip('"\'')
    if 'groq_key' not in st.session_state:
        st.session_state.groq_key = os.getenv('GROQ_API_KEY', '').strip().strip('"\'')
    if 'gemini_quota_exhausted' not in st.session_state:
        st.session_state.gemini_quota_exhausted = False
