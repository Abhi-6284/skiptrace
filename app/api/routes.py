from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.scraper import scrape_google_details

router = APIRouter()

class ScrapeRequest(BaseModel):
    querysearch: str

@router.post("/scrape")
async def scrape(request: ScrapeRequest):
    try:
        result = scrape_google_details(request.querysearch)
        if result is None:
            raise HTTPException(status_code=500, detail="Error occurred during scraping.")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))