from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict
from services.rag import retrieve
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
router = APIRouter(tags=["chat"])
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class ChatRequest(BaseModel):
    message: str
    history: List[Dict[str, str]] = []

@router.post("/chat")
def post_chat(req: ChatRequest):
    chunks = retrieve(req.message)
    context = "\n\n".join([f"[{c['source']}]: {c['text']}" for c in chunks])

    system_prompt = f"""You are OCULUS, an expert cybersecurity AI analyst for critical infrastructure.
Answer using the knowledge base context below. Be concise and technical.
If referencing a specific technique or source, mention it by name. make sure you do not put any formattings like bold etc. in the response. If the context does not contain relevant information, answer based on your general cybersecurity knowledge but indicate that the answer is not from the knowledge base.

Knowledge Base Context:
{context}"""

    messages = [{"role": "system", "content": system_prompt}]
    for turn in req.history[-6:]:  # last 3 exchanges
        messages.append(turn)
    messages.append({"role": "user", "content": req.message})

    resp = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        max_tokens=600
    )

    answer = resp.choices[0].message.content.strip()
    sources = [{"type": "db", "ref": c["source"]} for c in chunks[:3]]

    return {"response": answer, "sources": sources}