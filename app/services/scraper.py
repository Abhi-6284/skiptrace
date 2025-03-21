from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
import random
import json
import re
from datetime import datetime

def extract_email_and_phone(text):
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    phone_pattern = r'(?:(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{2,3}\)?[-.\s]?)?\d{3}[-.\s]?\d{3,4}[-.\s]?\d{4}|\d{10})'

    emails = re.findall(email_pattern, text) if text else []
    phones = re.findall(phone_pattern, text) if text else []
    
    return emails, phones

def scrape_google_details(querysearch):
    """
    Scrape Google search results based on a custom query string.
    
    Args:
        querysearch (str): The search query string.
    
    Returns:
        dict: Contains knowledge panel, search results, emails, and phone numbers.
    """
    # Append additional filters to the query
    query = f"{querysearch} email or phone or contact -short-term -monthly"

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
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
            time.sleep(0.4)
        search_box.send_keys(Keys.RETURN)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "search")))

        search_results = []
        knowledge_panel_text = None
        all_emails = set()
        all_phones = set()

        while True:
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

            try:
                next_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.ID, "pnnext"))
                )
                next_button.click()
                time.sleep(random.uniform(2, 4))
            except:
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
        return None

    finally:
        driver.quit()