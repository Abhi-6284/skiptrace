from pydantic import BaseSettings

class Settings(BaseSettings):
    """Configuration settings for the FastAPI application."""
    google_search_url: str = "https://www.google.com"
    user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    chrome_driver_path: str = "/path/to/chromedriver"  # Update this path as necessary

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()