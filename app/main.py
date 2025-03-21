from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.services.scraper import scrape_google_details
from pydantic import BaseModel
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# app.include_router(router)
class ScrapeRequest(BaseModel):
    querysearch: str

@app.post("/scrape")
async def scrape(request: ScrapeRequest):
    try:
        result = scrape_google_details(request.querysearch)
        if result is None:
            raise HTTPException(status_code=500, detail="Error occurred during scraping.")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "Welcome to the Google Scraper API"}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
