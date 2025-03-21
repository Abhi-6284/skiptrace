from pydantic import BaseModel
from typing import List, Optional

class ScrapeResult(BaseModel):
    source: str
    sourceLink: str
    title: str
    description: str
    emails: List[str]
    phones: List[str]

class ScrapeResponse(BaseModel):
    knowledge_panel: Optional[str]
    search_results: List[ScrapeResult]
    emails_found: List[str]
    phones_found: List[str]