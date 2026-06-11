# OCULUS
### Cyber Intelligence Platform for Critical Infrastructure

> *"The world's attacks, mapped in real time."*

OCULUS is a full-stack threat intelligence platform built for security analysts who work in the highest-stakes environments on earth — power grids, airports, ports, water treatment facilities. It pulls live vulnerability data, maps threats to the MITRE ATT&CK framework using RAG-powered AI, and surfaces everything through four interconnected interfaces that feel less like enterprise software and more like opening an intelligence dossier.

Built as an intern project at [Gramax Cybertech](https://gramaxcybertech.com) — a GMR Group subsidiary securing critical infrastructure across India and beyond.

---

## What it does

Most threat intelligence tools drown you in data. OCULUS is designed around a different philosophy: show analysts exactly what they need to see, connect the dots automatically, and get out of the way.

**You open the globe.** Live incidents from CISA's Known Exploited Vulnerabilities feed appear as glowing, pulsing dots on a rotating 3D earth. Red for critical. Amber for high. Each dot is a real vulnerability being actively exploited somewhere in the world, right now. You click one, and a frosted glass panel slides in with the full context — sector, location, severity, description. Two buttons at the bottom: *Analyze this incident* and *Ask AI*.

**You click Analyze.** The incident text travels to the MITRE ATT&CK Analyzer. Groq's LLaMA 3.1 first expands the brief CVE description into a full technical narrative, then runs it through a RAG pipeline against 709 MITRE techniques stored in ChromaDB. What comes back is a complete intelligence dossier — attack timeline reconstructed step by step, every relevant technique mapped with its T-ID, indicators of compromise, and a tiered mitigation strategy. The kind of report that would take an analyst hours, in about fifteen seconds.

**Or you click Ask AI.** The incident context loads directly into the conversational assistant. You ask follow-up questions in plain English. The assistant answers using the same MITRE knowledge base, with inline source citations — `[T1133]` `[CISA AA25-014A]` — embedded right inside the response text.

**Meanwhile, the news feed** is pulling live cybersecurity articles from NewsAPI, summarizing each one with Groq in real time, and presenting them as a horizontal editorial scroll. Every card has an Analyze button. Every card has an Ask AI button. The whole thing is connected.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Data Sources                          │
│  CISA KEV Feed    NewsAPI    MITRE ATT&CK JSON    ChromaDB  │
└──────────────┬──────────────────┬───────────────────────────┘
               │                  │
┌──────────────▼──────────────────▼───────────────────────────┐
│                     Services Layer                           │
│  otx_client.py   news_client.py   groq_client.py   rag.py  │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│               FastAPI Backend  (main.py)                     │
│                                                              │
│  GET /api/incidents    GET /api/news                        │
│  POST /api/analyze     POST /api/chat                       │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                    Frontend — 4 Pages                        │
│                                                              │
│  globe.html        updates.html                             │
│  Threat Map        News Intel                               │
│                                                              │
│  mittar.html       chatrag.html                             │
│  MITRE Analyzer    AI Assistant                             │
└─────────────────────────────────────────────────────────────┘
```

### Cross-page intelligence flow

Every page connects to every other. Click an incident on the globe → incident text pre-fills the Analyzer → Analyzer output → one click loads the AI Assistant with full context. Click a news card → same flow. No copy-pasting, no tab-switching. The context travels with you.

```
Globe (live incident)
    │
    ├──► Analyzer ──► full MITRE dossier
    │         │
    └──► AI Assistant ◄─────────────────┘
              ▲
News Feed ────┘
```

---

## Tech stack

| Layer | Technology |
|---|---|
| Backend | FastAPI + Uvicorn |
| LLM | LLaMA 3.1 8B Instant via Groq API |
| Vector DB | ChromaDB (local persistent) |
| Embeddings | sentence-transformers / all-MiniLM-L6-v2 |
| Knowledge Base | MITRE ATT&CK Enterprise (709 techniques) |
| Threat Intel | CISA Known Exploited Vulnerabilities |
| News | NewsAPI |
| 3D Globe | Globe.GL + Three.js |
| Animations | GSAP + ScrollTrigger |
| Frontend | Vanilla HTML / CSS / JS |
| Fonts | Alfa Slab One, Stardos Stencil, PT Serif Caption |

---

## Project structure

```
oculus/
├── main.py                      # FastAPI app, CORS, router registration
├── .env                         # API keys — not committed
├── requirements.txt
│
├── routers/
│   ├── incidents.py             # GET /api/incidents
│   ├── news.py                  # GET /api/news
│   ├── analyze.py               # POST /api/analyze
│   └── chat.py                  # POST /api/chat
│
├── services/
│   ├── otx_client.py            # CISA KEV fetcher + coordinate mapping
│   ├── news_client.py           # NewsAPI + Groq summarization
│   ├── groq_client.py           # expand_incident + analyze_incident
│   └── rag.py                   # ChromaDB ingestion + semantic retrieval
│
├── data/
│   └── mitre_attack.json        # MITRE ATT&CK Enterprise — not committed
│
├── chroma_db/                   # Persistent vector store — not committed
│
└── static/
    ├── globe.html               # Threat Map
    ├── updates.html             # News Intel
    ├── mittar.html              # MITRE Analyzer
    ├── chatrag.html             # AI Assistant
    └── oculus-logo.svg
```

---

## Setup

### Prerequisites

- Python 3.10+
- ~1.5GB disk space (sentence-transformers + MITRE dataset)
- Three free API keys (details below)

### 1. Clone

```bash
git clone https://github.com/purrieie/oculus.git
cd oculus
```

### 2. Virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Mac / Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install fastapi uvicorn python-dotenv groq chromadb \
            sentence-transformers requests newsapi-python
```

> First install takes 3-5 minutes — sentence-transformers pulls PyTorch.

### 4. Get your API keys

| Service | URL | Free tier |
|---|---|---|
| Groq | [console.groq.com](https://console.groq.com) | Yes — generous |
| NewsAPI | [newsapi.org](https://newsapi.org) | Yes |
| CISA KEV | No key required | Public |

### 5. Configure environment

Create `.env` in the project root:

```
GROQ_API_KEY=gsk_...
NEWS_API_KEY=...
```

### 6. Download MITRE ATT&CK data

```bash
curl -L "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json" \
     -o data/mitre_attack.json
```

This is ~50MB. On first server start, OCULUS will automatically ingest all 709 techniques into ChromaDB — takes about 2 minutes, only happens once.

### 7. Run

```bash
uvicorn main:app --reload --port 8000
```

### 8. Open

| Page | URL |
|---|---|
| Threat Map | http://localhost:8000/static/globe.html |
| News Intel | http://localhost:8000/static/updates.html |
| MITRE Analyzer | http://localhost:8000/static/mittar.html |
| AI Assistant | http://localhost:8000/static/chatrag.html |
| API Docs | http://localhost:8000/docs |

---

## Deploying to HuggingFace Spaces

OCULUS runs on HuggingFace Spaces (Docker) for free. The 2GB RAM free tier handles the full stack.

Add a `Dockerfile` to the repo root:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p data chroma_db

RUN curl -L "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json" \
    -o data/mitre_attack.json

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
```

Then on HuggingFace: New Space → Docker SDK → connect GitHub → add `GROQ_API_KEY` and `NEWS_API_KEY` as repository secrets → deploy.

> Note: ChromaDB is not persistent on the free tier. MITRE re-ingests on every cold start (~2 min). Paid tier adds persistent storage.

---

## API reference

### `GET /api/incidents`

Returns live incidents from CISA KEV with coordinates and severity classification.

```json
[
  {
    "id": "CVE-2026-11645",
    "title": "CVE-2026-11645 — Google Chromium V8",
    "sector": "General",
    "lat": 37.1,
    "lon": -95.7,
    "threat": "high",
    "date": "2026-06-09",
    "summary": "..."
  }
]
```

### `GET /api/news`

Returns recent cybersecurity news with Groq-generated summaries and sector classification.

```json
[
  {
    "headline": "...",
    "summary": "One-line Groq summary",
    "sector": "ICS/SCADA",
    "threat_level": "medium",
    "source": "Wired",
    "published_at": "2026-06-10T10:30:00Z",
    "url": "..."
  }
]
```

### `POST /api/analyze`

Accepts any incident text. Expands it, retrieves MITRE context, returns full intelligence dossier.

```json
// Request
{ "incident_text": "Attackers gained access to a water treatment SCADA system..." }

// Response
{
  "title": "Water Treatment Plant SCADA Compromise",
  "severity": "critical",
  "confidence": "high",
  "sector": "Water and Wastewater",
  "threat_actor": "Unknown",
  "executive_summary": "...",
  "timeline": [
    { "step": 1, "title": "Initial Access", "text": "...", "level": "initial" }
  ],
  "techniques": [
    { "tactic": "Initial Access", "id": "T1190", "name": "Exploit Public-Facing Application" }
  ],
  "iocs": [
    { "type": "cve", "value": "CVE-2025-1234", "confidence": "high" }
  ],
  "mitigations": [
    { "phase": "Immediate Actions", "items": ["Patch CVE-2025-1234...", "Rotate credentials..."] }
  ]
}
```

### `POST /api/chat`

RAG-backed conversational endpoint. Maintains context across turns.

```json
// Request
{
  "message": "What MITRE techniques are used in VPN attacks on OT systems?",
  "history": []
}

// Response
{
  "response": "...",
  "sources": [{ "type": "db", "ref": "Valid Accounts" }]
}
```

---

## How the RAG pipeline works

On first run, `rag.py` reads all 709 MITRE ATT&CK Enterprise techniques from `mitre_attack.json`. Each technique name, description, and tactic is embedded using `sentence-transformers/all-MiniLM-L6-v2` and stored as a vector in ChromaDB. This only happens once — subsequent runs load from the persisted store in `./chroma_db`.

On every `/api/analyze` request, the incident text is first passed through `expand_incident()` — a Groq call that enriches brief CVE descriptions into full technical narratives before analysis. Then the expanded text is embedded, the top-5 semantically similar MITRE techniques are retrieved, and those chunks are injected into the analysis prompt as grounding context. The LLM is generating structure, not guessing technique IDs.

On every `/api/chat` request, the user's message is embedded and the top-5 relevant KB chunks are retrieved and prepended to the conversation context. The assistant answers from real documents, not training data.

---

## Design

Four pages, four moods, one visual language.

The globe is cinematic — dark satellite tiles, glowing incident markers, atmospheric depth. The news feed is editorial — soft blue-gray, horizontal scroll, serif headlines, magazine archive energy. The analyzer is the intelligence dossier — structured, precise, data-dense but never cluttered. The assistant is intimate — deep navy, floating bubbles, an ops room at 2am.

Everything shares the same foundation: `#030712` void backgrounds, glassmorphism panels at `rgba(10,22,40,0.65)`, `#3b82f6` blue accents, Three.js star fields, and Quantico monospace labels. The design system was built to feel like Apple × Linear × Palantir — not Splunk.

---

## License

MIT — do whatever you want with it.

---

*Built with way too much attention to detail and a genuine belief that security tooling doesn't have to be ugly.*
