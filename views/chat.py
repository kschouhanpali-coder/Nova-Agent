import streamlit as st
import os

from config import AGENT_MAPPING
from rag_engine import load_rag_indices
from utils import get_svg_avatar_base64, get_user_svg_avatar_base64


def render_chat():
    """Render the Neural Chat view."""
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
                api_key = st.session_state.gemini_key.strip().strip('"\'')

                
                if not api_key:
                    error_msg = "Error: API Key not configured. Please visit Settings."
                    response_placeholder.markdown(error_msg)
                    st.session_state.chat_history[agent_id].append({"role": "assistant", "content": error_msg})
                else:
                    _generate_response(agent_id, info, prompt, api_key, response_placeholder)

    # Close the agent-chat-wrapper div
    st.markdown("</div>", unsafe_allow_html=True)


def _generate_response(agent_id, info, prompt, api_key, response_placeholder):
    """Handle the AI response generation with Gemini/Groq fallback logic."""
    context_str = "No internal documentation retrieved."
    retrievers = load_rag_indices()
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
5. Just speak directly. No role-play formatting. Clean, articulate, professional responses.

RESPONSE FORMATTING (MANDATORY — follow these in EVERY response):
- Structure your response with **bold** for key terms, names, and important concepts.
- Use bullet points (•) or numbered lists to organize ideas clearly when listing 2+ items.
- For longer answers, use ### section headers to divide topics.
- Use > blockquotes for particularly impactful or quotable statements.
- Keep paragraphs short (2-3 sentences max) for readability.
- Use line breaks between sections for visual breathing room.
- When discussing technical concepts, wrap them in `inline code`.
- For comparisons or multi-point arguments, use structured formatting:
  - **Point name** — explanation
- End with a clear, concise closing thought or question to continue the conversation.
- Make your response look polished, premium, and visually structured — never output a single wall of text."""
    
    gemini_failed = False
    groq_key = st.session_state.groq_key.strip().strip('"\'')
    response_generated = False
    
    # ---- STRATEGY: Smart provider selection ----
    # If Gemini quota was previously exhausted, try Groq first
    if st.session_state.gemini_quota_exhausted and groq_key:
        response_placeholder.markdown("⚡ Connecting via **Groq (Llama 3)**...")
        success, result = _try_groq(response_placeholder, sys_prompt, prompt, groq_key, "⚡ Generating response via **Groq (Llama 3)**...")
        if success:
            st.session_state.chat_history[agent_id].append({"role": "assistant", "content": result})
            response_generated = True
        else:
            # Groq also failed, try Gemini as fallback (maybe quota reset)
            response_placeholder.markdown("⏳ Groq unavailable, retrying **Gemini**...")
            success, result, is_quota = _try_gemini(response_placeholder, sys_prompt, prompt, api_key)
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
        success, result, is_quota = _try_gemini(response_placeholder, sys_prompt, prompt, api_key)
        if success:
            st.session_state.chat_history[agent_id].append({"role": "assistant", "content": result})
            response_generated = True
        elif is_quota:
            st.session_state.gemini_quota_exhausted = True
            # Try Groq fallback
            if groq_key:
                success, groq_result = _try_groq(response_placeholder, sys_prompt, prompt, groq_key, "⏳ Gemini quota exhausted. Switching to **Groq (Llama 3)** fallback...")
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


def _try_groq(placeholder, system_prompt, user_prompt, groq_api_key, status_msg=""):
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


def _try_gemini(placeholder, system_prompt, user_prompt, gemini_api_key):
    """Attempt to generate response using Gemini. Returns (success, response_text, is_quota_error)."""
    try:
        import google.generativeai as genai
        genai.configure(api_key=gemini_api_key, transport="rest")
        
        model_names = ['gemini-2.0-flash-lite', 'gemini-2.0-flash']
        response_stream = None
        first_chunk = None
        
        for model_name in model_names:
            try:
                model = genai.GenerativeModel(model_name)
                try:
                    stream = model.generate_content(f"{system_prompt}\n\nUser Query: {user_prompt}", stream=True)
                    first_chunk = next(iter(stream))
                    response_stream = stream
                    break
                except Exception as stream_err:
                    err_lower = str(stream_err).lower()
                    if "stream" in err_lower or "400" in err_lower:
                        # Fallback to non-streaming batch mode
                        response = model.generate_content(f"{system_prompt}\n\nUser Query: {user_prompt}", stream=False)
                        if response and response.text:
                            placeholder.markdown(response.text)
                            return True, response.text, False
                    raise stream_err
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
