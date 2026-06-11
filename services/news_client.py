import requests
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

QUERIES = ["ICS cybersecurity", "SCADA attack", "power grid hack", "OT security incident"]

SECTOR_MAP = {
    "power": "Power Grid", "grid": "Power Grid",
    "scada": "ICS/SCADA", "ics": "ICS/SCADA",
    "aviation": "Aviation", "airport": "Aviation",
    "water": "Water", "maritime": "Maritime", "ship": "Maritime",
    "oil": "Oil & Gas", "gas": "Oil & Gas", "pipeline": "Oil & Gas",
    "nuclear": "Nuclear", "railway": "Railway", "hospital": "Healthcare"
}

def detect_sector(text):
    text_lower = text.lower()
    for keyword, sector in SECTOR_MAP.items():
        if keyword in text_lower:
            return sector
    return "General"

def summarize(title, description):
    try:
        resp = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{
                "role": "user",
                "content": f"Summarize this cybersecurity news in one sentence (max 20 words):\nTitle: {title}\n{description or ''}"
            }],
            max_tokens=60
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        print(f"Groq summarize failed: {e}")
        return description[:120] if description else "No summary available."

def fetch_news():
    headers = {"X-Api-Key": NEWS_API_KEY}
    seen = set()
    articles = []

    for query in QUERIES:
        try:
            url = f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&pageSize=5&language=en"
            r = requests.get(url, headers=headers, timeout=10)
            r.raise_for_status()
            for a in r.json().get("articles", []):
                if a["title"] in seen:
                    continue
                seen.add(a["title"])
                articles.append({
                    "headline": a["title"],
                    "summary": summarize(a["title"], a.get("description")),
                    "sector": detect_sector(a["title"] + " " + (a.get("description") or "")),
                    "threat_level": "medium",
                    "source": a["source"]["name"],
                    "published_at": a["publishedAt"],
                    "url": a["url"]
                })
        except Exception as e:
            print(f"NewsAPI failed for '{query}': {e}")
            continue

    return articles