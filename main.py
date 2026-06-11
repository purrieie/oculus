import os
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from routers import incidents, news, analyze, chat
import os
import requests as req
from fastapi.responses import FileResponse


def download_mitre():
    path = "data/mitre_attack.json"
    if not os.path.exists(path):
        print("Downloading MITRE ATT&CK...")
        os.makedirs("data", exist_ok=True)
        r = req.get(
            "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json",
            timeout=120
        )
        with open(path, "wb") as f:
            f.write(r.content)
        print("MITRE downloaded.")

download_mitre()

app = FastAPI(title="OCULUS API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(incidents.router, prefix="/api")
app.include_router(news.router, prefix="/api")
app.include_router(analyze.router, prefix="/api")
app.include_router(chat.router, prefix="/api")


@app.get("/")
async def home():
    return FileResponse("static/globe.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)