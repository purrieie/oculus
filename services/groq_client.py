import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def expand_incident(raw_text: str) -> str:
    prompt = f"""You are a cybersecurity analyst. The following is a brief incident description or CVE summary. 
Expand it into a detailed technical incident narrative (150-200 words) suitable for MITRE ATT&CK analysis.
Include likely attack vectors, affected systems, potential threat actor behavior, and impact.
Return ONLY the expanded narrative, no headers, no JSON, no preamble.

Input: {raw_text}"""
    try:
        resp = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400
        )
        return resp.choices[0].message.content.strip() # pyright: ignore[reportOptionalMemberAccess]
    except Exception as e:
        print(f"Expand failed: {e}")
        return raw_text

def analyze_incident(incident_text: str, techniques_context: str) -> dict:
    incident_text = expand_incident(incident_text)
    prompt = f"""You are a cybersecurity analyst. Analyze this incident and return ONLY valid JSON, no markdown, no explanation.

MITRE ATT&CK context:
{techniques_context}

Incident:
{incident_text}

Return this exact JSON structure:
{{
  "title": "short incident title",
  "executive_summary": "2-3 sentence summary",
  "severity": "critical|high|medium|low",
  "confidence": "high|medium|low",
  "sector": "affected sector",
  "threat_actor": "actor name or Unknown",
  "timeline": [
    {{"step": 1, "title": "step title", "text": "what happened", "level": "initial|execution|exfiltration|impact"}}
  ],
  "techniques": [
    {{"tactic": "tactic name", "id": "TXXXX", "name": "technique name"}}
  ],
  "iocs": [
    {{"type": "ip|domain|hash|cve", "value": "indicator value", "confidence": "high|medium|low"}}
  ],
  "mitigations": [
    {{"phase": "phase name", "items": ["mitigation 1", "mitigation 2"]}}
  ]
}}"""

    resp = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1500
    )
    raw = resp.choices[0].message.content.strip()  # pyright: ignore[reportOptionalMemberAccess]
    raw = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(raw)