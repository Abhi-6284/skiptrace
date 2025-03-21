# FastAPI Google Scraper

This project is a FastAPI application that provides a REST API for scraping Google search results to extract emails and phone numbers associated with a given person's name.

## Project Structure

```
fastapi-google-scraper
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── api
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── core
│   │   ├── __init__.py
│   │   └── config.py
│   ├── services
│   │   ├── __init__.py
│   │   └── scraper.py
│   └── models
│       ├── __init__.py
│       └── schemas.py
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd fastapi-google-scraper
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Start the FastAPI application:
   ```
   uvicorn app.main:app --reload
   ```

2. Access the API documentation at `http://127.0.0.1:8000/docs`.

## API Endpoint

- **POST /scrape**
  - Request Body:
    ```json
    {
      "first_name": "string",
      "last_name": "string",
      "state": "string"  // optional
    }
    ```
  - Response:
    ```json
    {
      "knowledge_panel": "string",
      "search_results": [
        {
          "source": "string",
          "sourceLink": "string",
          "title": "string",
          "description": "string",
          "emails": ["string"],
          "phones": ["string"]
        }
      ],
      "emails_found": ["string"],
      "phones_found": ["string"]
    }
    ```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.