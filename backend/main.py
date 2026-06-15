import os
import re
import math
import string
import logging
import asyncio
import json
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("novaagent-backend")

app = FastAPI(title="NovaAgent Multi-Agent Orchestrator")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

AGENT_MAPPING = {
    "planner": {
        "name": "Sam Altman",
        "role": "CEO & Co-Founder, OpenAI",
        "skill_file": "SKILL.md",
        "rag_file": "SAM_ALTMAN_RAG_MASTER.md",
        "color": "#00d2ff",  # cyan
        "avatar": "SAM",
        "description": "Embody Sam Altman, CEO of OpenAI — architect of ChatGPT, GPT-4, and the modern AGI race. Leverage his expertise in hyper-growth scaling, geopolitical AI alignment, and venture funding to steer groundbreaking technical initiatives, manage complex GPU compute infrastructure, and navigate global AI safety regulations.",
        "capabilities": ["AGI Strategy", "Product Scaling", "Venture & Fundraising", "AI Policy", "Org Design", "AI Economics", "Future of Work"]
    },
    "oracle": {
        "name": "Demis Hassabis",
        "role": "CEO & Co-Founder, Google DeepMind",
        "skill_file": "SKILL-2-2.md",
        "rag_file": "DEMIS_HASSABIS_RAG_MASTER.md",
        "color": "#a855f7",  # purple
        "avatar": "DEMIS",
        "description": "Embody Demis Hassabis, CEO of Google DeepMind — neuroscientist, chess prodigy, game designer, and 2024 Chemistry Nobel laureate. Harness deep reinforcement learning, AlphaFold systems biology, and neuroscience-inspired AI models to solve complex scientific challenges, advance materials science, and pioneer next-generation general intelligence.",
        "capabilities": ["Reinforcement Learning", "Protein Biology", "Neuroscience-Inspired AI", "Scientific AI Applications", "AGI Research Strategy", "Multimodal AI", "Game AI"]
    },
    "medic": {
        "name": "Dario Amodei",
        "role": "CEO & Co-Founder, Anthropic",
        "skill_file": "SKILL-3-2.md",
        "rag_file": "DARIO_AMODEI_RAG_MASTER.md",
        "color": "#22c55e",  # green
        "avatar": "DARIO",
        "description": "Embody Dario Amodei, CEO of Anthropic — AI safety pioneer, creator of Constitutional AI, and architect behind Claude. Apply mathematical safety guarantees, mechanistic interpretability, and robust reinforcement learning principles to build safe, steerable foundation models, manage race dynamics, and draft responsible deployment policies.",
        "capabilities": ["Constitutional AI", "AI Interpretability", "LLM Architecture", "AI Existential Risk", "Responsible Deployment", "Claude Architecture", "AI Safety Policy"]
    },
    "lex": {
        "name": "Sridhar Vembu",
        "role": "Founder & CEO, Zoho Corporation",
        "skill_file": "SKILL_Sridhar_Vembu.md",
        "rag_file": "RAG_Master_Sridhar_Vembu.md",
        "color": "#eab308",  # yellow
        "avatar": "SRIDHAR",
        "description": "Embody Sridhar Vembu, founder of Zoho Corporation — the bootstrapped Indian tech pioneer advocating for rural development and digital sovereignty. Utilize his insights on sustainable business operations, locally-focused tech ecosystems, massive bootstrapping strategies, enterprise SaaS integration, and values-driven leadership to build long-term value.",
        "capabilities": ["Bootstrapping Strategy", "Rural Development", "Digital Sovereignty", "SaaS Business Models", "Values-Driven Leadership", "Enterprise SaaS", "Alternative Hiring"]
    },
    "learn": {
        "name": "Bhavish Aggarwal",
        "role": "Founder & CEO, Krutrim AI & Ola",
        "skill_file": "SKILL_Bhavish_Aggarwal.md",
        "rag_file": "RAG_Master_Bhavish_Aggarwal.md",
        "color": "#ec4899",  # pink
        "avatar": "BHAVISH",
        "description": "Embody Bhavish Aggarwal, founder of Ola and Krutrim AI — India's first AI unicorn building indigenous LLMs and sovereign compute. Navigate multilingual model engineering, EV infrastructure scaling, and developing customized hardware architectures for emerging markets, challenging Western dominance with vernacular AI built for 1.4 billion users.",
        "capabilities": ["Indigenous LLMs", "Multilingual NLP", "Sovereign Compute", "Mobility & EV Tech", "Disruptive Innovation", "Vernacular AI", "Global South Markets"]
    }
}

# In-memory TF-IDF Retreiver implementation
class TFIDFRetriever:
    def __init__(self, chunks: List[Dict[str, str]]):
        self.chunks = chunks
        self.stopwords = {"the", "a", "an", "and", "or", "but", "is", "are", "was", "were", "to", "of", "in", "on", "at", "for", "with", "by", "about", "how", "what", "why", "who", "where", "you", "i", "we", "they", "he", "she", "it", "this", "that"}
        self.doc_tokens = []
        self.vocab = set()
        self.doc_tfs = []
        self.df = {}
        self.idf = {}
        self._build_index()
        
    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))
        tokens = text.split()
        return [t for t in tokens if t not in self.stopwords]
        
    def _build_index(self):
        N = len(self.chunks)
        if N == 0:
            return
            
        for chunk in self.chunks:
            tokens = self._tokenize(chunk["content"])
            self.doc_tokens.append(tokens)
            
            # Compute term frequency
            tf = {}
            for token in tokens:
                tf[token] = tf.get(token, 0) + 1
                self.vocab.add(token)
            self.doc_tfs.append(tf)
            
            # Document frequency
            seen_tokens = set(tokens)
            for token in seen_tokens:
                self.df[token] = self.df.get(token, 0) + 1
                
        # Compute IDF
        for token in self.vocab:
            df_val = self.df.get(token, 0)
            self.idf[token] = math.log(1 + (N / (1 + df_val)))
            
    def retrieve(self, query: str, top_k: int = 5) -> List[tuple]:
        query_tokens = self._tokenize(query)
        if not query_tokens or len(self.chunks) == 0:
            return [(chunk, 0.0) for chunk in self.chunks[:top_k]]
            
        # Compute Query TF-IDF
        query_tf = {}
        for token in query_tokens:
            query_tf[token] = query_tf.get(token, 0) + 1
            
        query_tfidf = {}
        query_len = 0.0
        for token, count in query_tf.items():
            if token in self.idf:
                val = count * self.idf[token]
                query_tfidf[token] = val
                query_len += val * val
        query_len = math.sqrt(query_len)
        
        if query_len == 0:
            return [(chunk, 0.0) for chunk in self.chunks[:top_k]]
            
        scores = []
        for i, chunk in enumerate(self.chunks):
            doc_tf = self.doc_tfs[i]
            dot_product = 0.0
            doc_len = 0.0
            
            for token, tf_val in doc_tf.items():
                idf_val = self.idf.get(token, 0.0)
                doc_tfidf_val = tf_val * idf_val
                doc_len += doc_tfidf_val * doc_tfidf_val
                if token in query_tfidf:
                    dot_product += query_tfidf[token] * doc_tfidf_val
                    
            doc_len = math.sqrt(doc_len)
            
            if doc_len == 0:
                sim = 0.0
            else:
                sim = dot_product / (query_len * doc_len)
                
            scores.append((chunk, sim))
            
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]

# Global retrievers cache
retrievers: Dict[str, TFIDFRetriever] = {}

def find_file(filename: str) -> Optional[str]:
    paths = [
        os.path.join("/mnt/user-data/uploads", filename),
        os.path.join("backend/data/rag_documents", filename),
        os.path.join("data/rag_documents", filename),
        filename
    ]
    for p in paths:
        if os.path.exists(p):
            return p
    return None

def chunk_document(content: str) -> List[Dict[str, str]]:
    chunks = []
    current_header = "Introduction"
    current_lines = []
    
    for line in content.split("\n"):
        if line.startswith("## "):
            if current_lines:
                chunks.append({
                    "header": current_header,
                    "content": "\n".join(current_lines).strip()
                })
            current_header = line.replace("##", "").strip()
            current_lines = [line]
        else:
            current_lines.append(line)
            
    if current_lines:
        chunks.append({
            "header": current_header,
            "content": "\n".join(current_lines).strip()
        })
        
    valid_chunks = []
    for chunk in chunks:
        if len(chunk["content"].split()) > 15 and "table of contents" not in chunk["header"].lower():
            valid_chunks.append(chunk)
            
    return valid_chunks

@app.on_event("startup")
def startup_event():
    logger.info("Initializing in-memory RAG TF-IDF indices...")
    for agent_id, info in AGENT_MAPPING.items():
        file_path = find_file(info["rag_file"])
        if file_path:
            logger.info(f"Indexing RAG file {info['rag_file']} for {info['name']}...")
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            chunks = chunk_document(content)
            retrievers[agent_id] = TFIDFRetriever(chunks)
            logger.info(f"Indexed {len(chunks)} chunks for {info['name']}.")
        else:
            logger.warning(f"Could not find RAG file {info['rag_file']} for {info['name']}. Using fallback.")

class ChatRequest(BaseModel):
    query: str
    agent: Optional[str] = None
    stream: Optional[bool] = True
    provider: Optional[str] = "groq"
    api_key: Optional[str] = None

def select_agent(query: str) -> str:
    query_lower = query.lower()
    
    if any(kw in query_lower for kw in ["sam", "altman", "openai", "chatgpt", "gpt", "agi", "y combinator", "yc", "silicon valley", "plan", "schedule", "timetable", "habit"]):
        return "planner"
    if any(kw in query_lower for kw in ["demis", "hassabis", "deepmind", "alphafold", "alphago", "chess", "nobel", "gemini", "future", "trend", "career", "predict", "market"]):
        return "oracle"
    if any(kw in query_lower for kw in ["dario", "amodei", "anthropic", "claude", "safety", "constitutional", "existential", "interpretability", "health", "diet", "mental", "symptom"]):
        return "medic"
    if any(kw in query_lower for kw in ["sridhar", "vembu", "zoho", "bootstrapped", "bootstrap", "rural", "sovereignty", "saas", "legal", "law", "fir", "contract", "rights"]):
        return "lex"
    if any(kw in query_lower for kw in ["bhavish", "aggarwal", "krutrim", "ola", "ev", "india", "indigenous", "mobility", "unicorn", "learn", "code", "quiz", "tutor", "exam"]):
        return "learn"
        
    return "planner"

@app.get("/api/agents")
def get_agents():
    return {agent_id: {**info, "id": agent_id} for agent_id, info in AGENT_MAPPING.items()}

@app.get("/api/agents/{agent_id}")
def get_agent(agent_id: str):
    if agent_id not in AGENT_MAPPING:
        raise HTTPException(status_code=404, detail="Agent not found")
    return {**AGENT_MAPPING[agent_id], "id": agent_id}

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    # Reload environment dynamically to sync with Streamlit updates
    load_dotenv(override=True)
    
    agent_id = request.agent
    if not agent_id or agent_id == "auto":
        agent_id = select_agent(request.query)
        
    if agent_id not in AGENT_MAPPING:
        raise HTTPException(status_code=404, detail="Agent not found")
        
    agent_info = AGENT_MAPPING[agent_id]
    
    skill_path = find_file(agent_info["skill_file"])
    skill_content = ""
    if skill_path:
        with open(skill_path, "r", encoding="utf-8") as f:
            skill_content = f.read()
    else:
        skill_content = f"You are {agent_info['name']}, {agent_info['role']}. {agent_info['description']}"
        
    retriever = retrievers.get(agent_id)
    retrieved_sections = []
    sources = []
    if retriever:
        results = retriever.retrieve(request.query, top_k=5)
        for chunk, score in results:
            if score > 0.05:
                retrieved_sections.append(
                    f"### SECTION: {chunk['header']} (relevance: {score:.2f})\n{chunk['content']}"
                )
                sources.append({
                    "file": agent_info["rag_file"],
                    "header": chunk["header"],
                    "score": score
                })
                
    context_str = "\n\n".join(retrieved_sections) if retrieved_sections else "No direct matching recorded data."
    
    system_prompt = f"""{skill_content}

RETRIEVED CONTEXT FROM RAG KNOWLEDGE BASE:
---
{context_str}
---

CRITICAL DIRECTIVE: Respond in character, adhering to your identity, communication rules, and core beliefs.
"""
    
    # Resolve the API key based on the provider
    resolved_api_key = request.api_key
    if not resolved_api_key:
        if request.provider == "gemini":
            resolved_api_key = os.getenv("GEMINI_API_KEY")
        elif request.provider == "groq":
            resolved_api_key = os.getenv("GROQ_API_KEY")

    async def event_generator():
        yield f"data: {json.dumps({'type': 'info', 'agent': agent_id, 'sources': sources})}\n\n"
        
        if not resolved_api_key:
            warning = f"[SYSTEM NOTICE: API Key not set. Responding in mock simulation mode.]\n\n"
            for char in warning:
                yield f"data: {json.dumps({'type': 'token', 'token': char})}\n\n"
                
            mock_replies = {
                "planner": "I am Sam Altman. Without an API key, I can't generate a full AGI plan, but once configured, I'll help you scale and strategize.",
                "oracle": "I am Demis Hassabis. The chess moves of the future are uncertain without an API key. Once set, we will analyze reinforcement learning and scientific breakthroughs.",
                "medic": "I am Dario Amodei. Without an API key, I cannot access Claude's constitutional safety models. Please configure it to explore AI safety and interpretability.",
                "lex": "I am Sridhar Vembu. Without an API key, I cannot advise on bootstrapping or rural development. Please configure the key to get started.",
                "learn": "I am Bhavish Aggarwal! Ready to teach you about multilingual NLP and compute, but please configure the API key first!"
            }
            reply = mock_replies.get(agent_id, "Hello! Please set your API key in settings to start chatting.")
            for chunk in re.findall(r'.{1,4}', reply):
                yield f"data: {json.dumps({'type': 'token', 'token': chunk})}\n\n"
                await asyncio.sleep(0.02)
            yield f"data: {json.dumps({'type': 'done'})}\n\n"
            return
            
        try:
            if request.provider == "groq":
                import groq
                client = groq.AsyncGroq(api_key=resolved_api_key)
                stream = await client.chat.completions.create(
                    model="llama3-8b-8192",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": request.query}
                    ],
                    stream=True
                )
                async for chunk in stream:
                    content = chunk.choices[0].delta.content
                    if content:
                        yield f"data: {json.dumps({'type': 'token', 'token': content})}\n\n"
                        
            elif request.provider == "gemini":
                import google.generativeai as genai
                resolved_api_key_clean = resolved_api_key.strip().strip('\"\'')
                with open("gemini_debug.log", "a", encoding="utf-8") as debug_file:
                    debug_file.write(f"Backend: Configuring genai with key: {resolved_api_key_clean[:10]}... (length={len(resolved_api_key_clean)})\n")
                genai.configure(api_key=resolved_api_key_clean, transport="rest")
                
                model_names = ['gemini-2.0-flash', 'gemini-2.0-flash-lite', 'gemini-1.5-flash', 'gemini-pro']
                response_stream = None
                last_err = None
                
                for m_name in model_names:
                    try:
                        model = genai.GenerativeModel(m_name)
                        response = await model.generate_content_async(
                            f"{system_prompt}\n\nUser Query: {request.query}", 
                            stream=True
                        )
                        # Force evaluation of the first chunk to catch unsupported models or invalid key errors immediately
                        iterator = response.__aiter__()
                        first_chunk = await iterator.__anext__()
                        
                        # Yield the first chunk's text
                        if first_chunk and first_chunk.text:
                            yield f"data: {json.dumps({'type': 'token', 'token': first_chunk.text})}\n\n"
                        response_stream = iterator
                        break
                    except Exception as model_err:
                        last_err = model_err
                        err_str = str(model_err).lower()
                        # Catch API Key / credentials / permission issues and raise immediately
                        if any(kw in err_str for kw in ["api key", "api_key", "invalid key", "invalid_key", "credentials", "unauthorized", "forbidden", "permission", "key not found", "key invalid"]):
                            raise model_err
                        # Catch API quota / rate limit / resource exhausted errors and raise immediately
                        if any(kw in err_str for kw in ["quota", "rate limit", "rate_limit", "429", "exhausted", "resourceexhausted"]):
                            raise model_err
                        # Catch model not found or unsupported errors to try other fallback models
                        if "404" in err_str or "not found" in err_str or "not supported" in err_str:
                            continue  # Try next model
                        else:
                            raise model_err
                
                if response_stream is None:
                    if last_err:
                        raise last_err
                    else:
                        raise Exception("No compatible Gemini model found.")
                
                # Consume the rest of the chunks
                try:
                    async for chunk in response_stream:
                        if chunk and chunk.text:
                            yield f"data: {json.dumps({'type': 'token', 'token': chunk.text})}\n\n"
                except Exception as stream_err:
                    logger.error(f"Error during streaming: {stream_err}")
                    raise stream_err
                    
            else:
                yield f"data: {json.dumps({'type': 'error', 'message': 'Unknown provider'})}\n\n"
                
            yield f"data: {json.dumps({'type': 'done'})}\n\n"
        except Exception as e:
            logger.error(f"Error calling {request.provider} API: {str(e)}")
            err_str = str(e).lower()
            if any(kw in err_str for kw in ["api key", "api_key", "invalid key", "invalid_key", "credentials", "unauthorized", "forbidden", "permission", "key not found", "key invalid"]):
                user_msg = "⚠️ API Key Invalid or Missing: Please check your API key configuration in settings."
            elif any(kw in err_str for kw in ["quota", "rate limit", "rate_limit", "429", "exhausted", "resourceexhausted"]):
                user_msg = "⚠️ API Rate Limit Exceeded or Invalid Key: Your Gemini API key might be invalid, or its free tier quota has been exhausted. Please verify your API key in settings and ensure it has active quota."
            else:
                user_msg = f"System Error: {str(e)}"
            yield f"data: {json.dumps({'type': 'error', 'message': user_msg})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
