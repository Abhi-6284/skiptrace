from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
# from app.services.scraper import scrape_google_details
from app.services.sc import scrape_google_details
from pydantic import BaseModel
import uvicorn
import json

import aiohttp
import pandas as pd
import asyncio
from concurrently import concurrently
from typing import List, Dict, Optional
from concurrent.futures import ProcessPoolExecutor

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

class FileScrapeRequest(BaseModel):
    data: str

@app.post("/scrape")
async def scrape(request: ScrapeRequest):
    try:
        result = scrape_google_details(request.querysearch)
        if result is None:
            raise HTTPException(status_code=500, detail="Error occurred during scraping.")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/file-scrape")
async def file_scrape(request: 'FileScrapeRequest') -> dict:
    try:
        # Parse the incoming data
        parsed_data = json.loads(request.data)
        print(f"Parsed data: {parsed_data}")
        print(f"Length of parsed_data: {len(parsed_data)}")

        # Define the individual scraping task
        async def scrape_task(query: str) -> dict:
            # If scrape_google_details is synchronous, wrap it in run_in_executor
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(None, scrape_google_details, query)
            return result

        # Run all scraping tasks in parallel
        scrape_tasks = [scrape_task(query) for query in parsed_data]
        scrape_results = await asyncio.gather(*scrape_tasks, return_exceptions=True)

        # Check for any exceptions in results
        for result in scrape_results:
            if isinstance(result, Exception):
                raise Exception(f"Scraping task failed: {str(result)}")

        # Return success message with results
        return {
            "message": "Scraping completed successfully.",
            "results": scrape_results
        }
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON data: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scraping error: {str(e)}")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Google Scraper API"}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
