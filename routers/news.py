from fastapi import APIRouter
from services.news_client import fetch_news

router = APIRouter(tags=["news"])

@router.get("/news")
def get_news():
    return fetch_news()