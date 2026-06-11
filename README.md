# 👁️ OCULUS

### *The world's cyber threats, visualized in real time.*

OCULUS is an AI-powered cyber intelligence platform built to monitor, analyze, and investigate threats targeting critical infrastructure.

From real-time vulnerability intelligence to MITRE ATT&CK analysis and retrieval-augmented cyber investigations, OCULUS combines threat feeds, AI reasoning, and interactive visualization into a single operational workspace.

---

## ✨ Features

### 🌍 Global Threat Map

Interactive 3D globe displaying live cyber incidents and exploited vulnerabilities.

* Real-time incident ingestion
* Severity-based visualization
* Dynamic threat connections
* Critical infrastructure focus
* Sector classification

---

### 📰 Threat Intelligence Updates

Continuously updated cybersecurity intelligence feed.

* NewsAPI integration
* AI-generated summaries
* Threat categorization
* Source attribution
* Sector-specific filtering

---

### 🎯 MITRE ATT&CK Analyzer

Transform raw incident reports into structured intelligence.

Input:

> "Attackers gained access to a SCADA environment using compromised VPN credentials."

Output:

* Executive summary
* Severity assessment
* Attack timeline
* MITRE technique mapping
* IOC extraction
* Recommended mitigations

---

### 🤖 OCULUS Analyst

A RAG-powered cybersecurity assistant.

* ChromaDB vector retrieval
* MITRE ATT&CK knowledge base
* Context-aware conversations
* Source attribution
* Critical infrastructure expertise

---

## 🏗️ System Architecture

```mermaid
flowchart TD

    A[Frontend UI] --> B[FastAPI Backend]

    B --> C[/api/incidents]
    B --> D[/api/news]
    B --> E[/api/analyze]
    B --> F[/api/chat]

    C --> G[CISA KEV Feed]
    C --> H[CISA ICS Advisories]

    D --> I[NewsAPI]
    D --> J[Groq AI Summaries]

    E --> K[MITRE ATT&CK Dataset]
    E --> L[Groq Incident Analysis]

    F --> M[ChromaDB]
    M --> N[MITRE Knowledge Base]

    F --> O[Sentence Transformers]
    F --> P[Groq LLM]

    P --> B
```

---

## 🧠 Technology Stack

### Frontend

* HTML5
* CSS3
* Vanilla JavaScript
* Globe.gl
* Three.js

### Backend

* FastAPI
* Uvicorn
* Python 3.11+

### AI & Retrieval

* Groq
* Llama 3
* ChromaDB
* Sentence Transformers
* Retrieval-Augmented Generation (RAG)

### Threat Intelligence

* MITRE ATT&CK
* CISA KEV Feed
* CISA ICS Advisories
* NewsAPI

---

## 📂 Project Structure

```text
oculus/
│
├── main.py
│
├── routers/
│   ├── incidents.py
│   ├── news.py
│   ├── analyze.py
│   └── chat.py
│
├── services/
│   ├── otx_client.py
│   ├── news_client.py
│   ├── groq_client.py
│   └── rag.py
│
├── data/
│   └── mitre_attack.json
│
├── chroma_db/
│
├── static/
│   ├── globe.html
│   ├── updates.html
│   ├── mittar.html
│   └── chatrag.html
│
├── requirements.txt
└── .env
```

---

## 🔌 API Endpoints

### GET `/api/incidents`

Returns live cyber incidents and exploited vulnerabilities.

```json
[
  {
    "id": "CVE-2026-XXXXX",
    "title": "Critical Infrastructure Vulnerability",
    "sector": "ICS/SCADA",
    "lat": 35.7,
    "lon": 139.7,
    "threat": "high"
  }
]
```

---

### GET `/api/news`

Returns curated cyber intelligence articles.

```json
[
  {
    "headline": "...",
    "summary": "...",
    "sector": "Power Grid"
  }
]
```

---

### POST `/api/analyze`

Analyze an incident against MITRE ATT&CK.

```json
{
  "incident_text": "Attackers compromised a VPN credential..."
}
```

---

### POST `/api/chat`

Query the OCULUS Analyst.

```json
{
  "message": "What MITRE techniques are used in VPN attacks?",
  "history": []
}
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone <your-repository>
cd oculus
```

Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
GROQ_API_KEY=
NEWS_API_KEY=
OTX_API_KEY=
```

Start the server:

```bash
uvicorn main:app --reload
```

Open:

```text
http://localhost:8000
```

Swagger Docs:

```text
http://localhost:8000/docs
```

---

## 📸 Screenshots

### 🌍 Threat Map

---

### 📰 Intelligence Updates

---

### 🎯 MITRE Analyzer

---

### 🤖 OCULUS Analyst

---

## 🚀 Future Enhancements

* CVE impact scoring
* Threat actor profiling
* IOC enrichment
* Multi-source intelligence fusion
* Attack-path visualization
* SIEM integrations
* SOC analyst workflows
* Real-time alerting

---

## 🎖️ Why OCULUS?

Most cybersecurity dashboards show data.

**OCULUS shows context.**

Instead of forcing analysts to jump between threat feeds, ATT&CK mappings, advisories, reports, and AI tools, OCULUS brings them into a single intelligence workspace designed for investigation, understanding, and action.

---

### Built for defenders. Designed for curiosity. 

**OCULUS** 👁️
