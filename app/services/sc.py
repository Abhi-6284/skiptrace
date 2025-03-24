from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import random
import json
import re
from concurrent.futures import ProcessPoolExecutor
from fastapi import FastAPI, HTTPException
import asyncio

app = FastAPI()

def extract_email_and_phone(text):
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    phone_pattern = r'(?:(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{2,3}\)?[-.\s]?)?\d{3}[-.\s]?\d{3,4}[-.\s]?\d{4}|\d{10})'
    emails = re.findall(email_pattern, text) if text else []
    phones = re.findall(phone_pattern, text) if text else []
    return emails, phones

def scrape_google_details(querysearch):
    """
    Scrape Google search results based on a custom query string.
    """
    query = f"{querysearch} email or phone or contact -short-term -monthly"

    options = Options()
    # Uncomment for headless mode if you don’t need to see the browser
    # options.add_argument("--headless")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://www.google.com")
        time.sleep(random.uniform(1, 3))

        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        for char in query:
            search_box.send_keys(char)
            time.sleep(0.05)  # Slightly faster typing
        search_box.send_keys(Keys.RETURN)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "search")))

        search_results = []
        knowledge_panel_text = None
        all_emails = set()
        all_phones = set()

        max_pages = 3
        for page in range(max_pages):
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            if not knowledge_panel_text:
                knowledge_panel = soup.find('div', class_='kp-wholepage')
                knowledge_panel_text = knowledge_panel.get_text(separator=' ', strip=True) if knowledge_panel else None
                if knowledge_panel_text:
                    emails, phones = extract_email_and_phone(knowledge_panel_text)
                    all_emails.update(emails)
                    all_phones.update(phones)

            results = soup.select('div.MjjYud')
            for result in results:
                title = result.find('h3')
                title_text = title.get_text() if title else None
                snippet = result.find('div', {'style': '-webkit-line-clamp:2'})
                snippet_text = snippet.get_text() if snippet else None
                link = result.find('a')
                url = link['href'] if link and 'href' in link.attrs else None

                if title_text and url:
                    emails, phones = extract_email_and_phone(snippet_text)
                    all_emails.update(emails)
                    all_phones.update(phones)

                    search_results.append({
                        'title': title_text,
                        'description': snippet_text,
                        'url': url,
                        'emails': emails,
                        'phones': phones
                    })

            # Try to find and click the "Next" button
            try:
                # Use a more robust XPath for the "Next" link
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[@id='pnnext'] | //a[contains(@aria-label, 'Next')]"))
                )
                driver.execute_script("arguments[0].scrollIntoView(true);", next_button)  # Scroll to ensure visibility
                time.sleep(random.uniform(0.5, 1))  # Brief pause after scrolling
                next_button.click()
                time.sleep(random.uniform(2, 4))  # Wait for page load
                print(f"Navigated to page {page + 2}")
            except Exception as e:
                print(f"No more pages or error clicking Next: {str(e)}")
                break

        result_data = {
            'knowledge_panel': knowledge_panel_text,
            'search_results': search_results,
            'emails_found': list(all_emails),
            'phones_found': list(all_phones)
        }

        return result_data

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return {"error": str(e)}

    finally:
        driver.quit()

# Example usage
if __name__ == "__main__":
    result = scrape_google_detailss("example company contact")
    print(json.dumps(result, indent=2))