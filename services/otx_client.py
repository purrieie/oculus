import requests
from datetime import datetime

COUNTRY_COORDS = {
    "ukraine": (49.0, 31.5), "russia": (61.5, 105.3), "china": (35.9, 104.2),
    "iran": (32.4, 53.7), "usa": (37.1, -95.7), "united states": (37.1, -95.7),
    "germany": (51.2, 10.5), "france": (46.2, 2.2), "uk": (55.4, -3.4),
    "india": (20.6, 78.9), "japan": (36.2, 138.3), "israel": (31.0, 34.9),
    "saudi": (23.9, 45.1), "australia": (-25.3, 133.8), "canada": (56.1, -106.3),
    "netherlands": (52.1, 5.3), "poland": (51.9, 19.1), "korea": (35.9, 127.8),
    "taiwan": (23.7, 121.0), "brazil": (-14.2, -51.9), "singapore": (1.3, 103.8),
    "pakistan": (30.4, 69.3), "turkey": (38.9, 35.2), "mexico": (23.6, -102.5),
    "italy": (41.9, 12.5), "spain": (40.4, -3.7), "switzerland": (46.8, 8.2),
}

SECTOR_KEYWORDS = {
    "energy": "power grid", "electric": "power grid", "power": "power grid",
    "grid": "power grid", "water": "water", "scada": "ICS/SCADA",
    "ics": "ICS/SCADA", "industrial": "ICS/SCADA", "pipeline": "oil & gas",
    "oil": "oil & gas", "gas": "oil & gas", "nuclear": "nuclear",
    "aviation": "aviation", "airport": "aviation", "maritime": "maritime",
    "port": "maritime", "ship": "maritime", "rail": "railway",
    "hospital": "healthcare", "medical": "healthcare", "manufacturing": "manufacturing",
}

def get_coords(text):
    text_lower = text.lower()
    for keyword, coords in COUNTRY_COORDS.items():
        if keyword in text_lower:
            return coords
    return None

def get_sector(text):
    text_lower = text.lower()
    for keyword, sector in SECTOR_KEYWORDS.items():
        if keyword in text_lower:
            return sector
    return "General"

def classify_severity(title, description):
    text = (title + " " + description).lower()
    if any(w in text for w in ["critical", "ransomware", "nation-state", "apt", "zero-day", "zeryday"]):
        return "critical"
    elif any(w in text for w in ["high", "exploit", "remote code", "rce", "backdoor", "malware"]):
        return "high"
    return "medium"

def fetch_incidents():
    incidents = []

    # ── Source 1: CISA KEV (Known Exploited Vulnerabilities) ──────────────
    try:
        r = requests.get(
            "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json",
            timeout=15
        )
        r.raise_for_status()
        vulns = r.json().get("vulnerabilities", [])
        # Sort by dateAdded descending, take top 30
        vulns_sorted = sorted(vulns, key=lambda x: x.get("dateAdded", ""), reverse=True)[:30]
        for i, v in enumerate(vulns_sorted):
            text = v.get("vendorProject", "") + " " + v.get("product", "") + " " + v.get("shortDescription", "")
            sector = get_sector(text)
            coords = get_coords(text)
            # Spread points slightly so they don't stack
            import random
            base_coords = coords or (20 + random.uniform(-40, 40), random.uniform(-150, 150))
            incidents.append({
                "id": v.get("cveID", str(i)),
                "title": f"{v.get('cveID')} — {v.get('vendorProject')} {v.get('product')}",
                "sector": sector,
                "lat": round(base_coords[0] + random.uniform(-3, 3), 2),
                "lon": round(base_coords[1] + random.uniform(-3, 3), 2),
                "threat": classify_severity(v.get("vendorProject",""), v.get("shortDescription","")),
                "date": v.get("dateAdded", ""),
                "summary": v.get("shortDescription", "")
            })
    except Exception as e:
        print(f"CISA KEV fetch failed: {e}")

    # ── Source 2: CISA ICS Advisories RSS ─────────────────────────────────
    try:
        r = requests.get(
            "https://www.cisa.gov/ics.xml",
            timeout=15,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        r.raise_for_status()
        import xml.etree.ElementTree as ET
        root = ET.fromstring(r.content)
        items = root.findall(".//item")[:20]
        for i, item in enumerate(items):
            title = item.findtext("title") or "ICS Advisory"
            desc = item.findtext("description") or ""
            date = item.findtext("pubDate") or ""
            text = title + " " + desc
            sector = get_sector(text)
            coords = get_coords(text)
            import random
            base_coords = coords or (30 + random.uniform(-20, 20), random.uniform(-100, 100))
            incidents.append({
                "id": f"ics_{i}",
                "title": title,
                "sector": sector,
                "lat": round(base_coords[0] + random.uniform(-2, 2), 2),
                "lon": round(base_coords[1] + random.uniform(-2, 2), 2),
                "threat": classify_severity(title, desc),
                "date": date,
                "summary": desc[:200]
            })
    except Exception as e:
        print(f"CISA ICS RSS fetch failed: {e}")

    if not incidents:
        print("All sources failed — using mock data")
        return []

    print(f"Fetched {len(incidents)} incidents from CISA")
    return incidents


