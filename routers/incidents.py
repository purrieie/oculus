from fastapi import APIRouter
router = APIRouter(tags=["incidents"])

from fastapi import APIRouter
from services.otx_client import fetch_incidents
import time

router = APIRouter(tags=["incidents"])

_cache = {"data": [], "ts": 0}
CACHE_TTL = 900  # 15 minutes


@router.get("/incidents")
def get_incidents():
    now = time.time()
    if now - _cache["ts"] < CACHE_TTL and _cache["data"]:
        return _cache["data"]

    data = fetch_incidents()
    _cache["data"] = data
    _cache["ts"] = now
    return data