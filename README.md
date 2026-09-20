<div align="center">

# 🤖 NovaAgent Dashboard 🤖

### Your AI Agents, Ready to Work.

![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)
![Version](https://img.shields.io/badge/Version-1.0.0-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)
![Type](https://img.shields.io/badge/Type-Multi--Agent%20Dashboard-4285F4?style=for-the-badge)

A multi-agent AI dashboard with five specialized agents that plan, analyze, and answer, each with a distinct area of expertise. Chat with them in real time, powered by Google Gemini with an automatic Groq fallback and RAG-enhanced knowledge.

*Deploy specialized agents. Focus on what matters most.*

</div>

---

## 🚀 Live Demo

<div align="center">

### **[▶️ LAUNCH NOVAAGENT DASHBOARD - Live Demo](https://nova-agent-iayjoag9muyfjsruawenmh.streamlit.app)**

*Pick an agent and start a conversation right in your browser!*

</div>

---

## ✨ Features

- 🧠 **5 Specialized AI Agents** - Each with a distinct area of expertise and persona
- 💬 **Real-Time Neural Chat** - Interactive conversations with the agent of your choice
- 📚 **RAG-Powered Knowledge** - Retrieval-augmented generation to enhance agent answers
- 🛟 **Automatic Fallback** - Seamless switch between LLM providers if a quota is reached
- 📊 **Modules Dashboard** - Core network status, active agents, and per-agent status at a glance
- 🧩 **Modules Hub** - Initialize agents and view their capabilities
- ⚙️ **Settings Panel** - Add or update your API keys at any time

---

## 🏁 Quick Start

### Use Online
No installation needed! [Launch the live demo](https://nova-agent-iayjoag9muyfjsruawenmh.streamlit.app)

### Run Locally

**Prerequisites:** Python 3.8+, a Google Gemini API key, and (optionally) a [Groq API key](https://console.groq.com/keys) for fallback

1. Clone the repository:
```bash
git clone https://github.com/kschouhanpali-coder/NovaAgent.git
cd NovaAgent
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up your environment variables:
```bash
cp .env.example .env
```
```env
GEMINI_API_KEY=your_gemini_api_key_here
GROQ_API_KEY=your_groq_api_key_here
```

4. Start the app:
```bash
streamlit run app.py
```

5. Open `http://localhost:8501` in your browser

---

## 🎯 How to Use

1. **Open Neural Chat** from the sidebar
2. **Pick an Agent** - choose the persona that fits your question
3. **Ask Away** - type your query and press Enter
4. **Explore the Hub** - open the Modules Hub to see each agent's capabilities
5. **Check the Dashboard** - monitor network status and active agents
6. **Configure** - open **Settings** to add or update your API keys

---

## 🗂️ Agent Specializations

| Agent | Focus |
|-------|-------|
| **🛡️ Anthropic-Inspired** | AI safety, constitutional AI, LLM architecture |
| **🚀 OpenAI-Inspired** | AGI strategy, scaling, venture funding |
| **🔬 DeepMind-Inspired** | Reinforcement learning, neuroscience, scientific AI |
| **🌏 Krutrim/Ola-Inspired** | Indigenous LLMs, vernacular AI, sovereign compute |
| **💼 Zoho-Inspired** | Bootstrap strategy, rural development, SaaS |

> Each agent's persona is inspired by the publicly known thinking, strategy, and expertise areas associated with a leading figure or company in AI. These are not verified or endorsed statements from any individual, and the project is not affiliated with these organizations.

---

## 💻 Technologies Used

- **Frontend:** Streamlit
- **Primary LLM:** Google Gemini
- **Fallback LLM:** Groq
- **Knowledge Layer:** Retrieval-Augmented Generation (RAG) with LangChain
- **Deployment:** Streamlit Cloud

---

## 📝 License

MIT License - Free to use and modify

---

<div align="center">

**[Live Demo](https://nova-agent-iayjoag9muyfjsruawenmh.streamlit.app) | [GitHub](https://github.com/kschouhanpali-coder/NovaAgent) | [Report Issues](https://github.com/kschouhanpali-coder/NovaAgent/issues)**

*Your AI agents, ready to work.* 🤖

</div>
