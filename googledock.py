import whois
import requests
from bs4 import BeautifulSoup
from googlesearch import search
import validators
from PIL import Image
import pytesseract
import io
import sqlite3
from datetime import datetime

# Function to connect to the database
def connect_db():
    conn = sqlite3.connect('search_results.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS results
                      (url TEXT, domain TEXT, title TEXT, description TEXT, is_fake INTEGER, logo_text TEXT, date TIMESTAMP)''')
    return conn, cursor

# Function to save results to the database
def save_to_db(cursor, url, domain, title, description, is_fake, logo_text):
    cursor.execute('''INSERT INTO results (url, domain, title, description, is_fake, logo_text, date)
                      VALUES (?, ?, ?, ?, ?, ?, ?)''', (url, domain, title, description, is_fake, logo_text, datetime.now()))

# Perform a Google search and return the top results
def google_search(query, num_results):
    results = []
    try:
        for result in search(query, num=num_results, stop=num_results, pause=2):
            results.append(result)
    except Exception as e:
        print(f"An error occurred during Google search: {e}")
    return results

# Fetch page details such as title and meta description
def fetch_page_details(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.find('title').text if soup.find('title') else 'No title'
            description = soup.find('meta', attrs={'name': 'description'})
            description = description['content'] if description else 'No description'
            return {'title': title, 'description': description, 'soup': soup}
        else:
            return {'title': 'N/A', 'description': 'N/A', 'soup': None}
    except requests.RequestException as e:
        print(f"An error occurred while fetching the page: {e}")
        return {'title': 'N/A', 'description': 'N/A', 'soup': None}

# Check if a website is likely to be fake
def is_fake_website(url):
    try:
        domain_info = whois.whois(url)
        if domain_info and (domain_info.creation_date and domain_info.creation_date > datetime.now().replace(year=datetime.now().year-1)):
            return True
        return False
    except Exception as e:
        print(f"An error occurred while performing WHOIS lookup: {e}")
        return True

# Extract domain from URL
def extract_domain(url):
    if validators.url(url):
        domain = url.split('/')[2]
        return domain
    return 'Invalid URL'

# Fetch and analyze logo details
def analyze_logo(soup):
    try:
        logo_url = None
        for img in soup.find_all('img'):
            if 'logo' in img.get('alt', '').lower() or 'logo' in img.get('src', '').lower():
                logo_url = img['src']
                break
        if logo_url:
            if not logo_url.startswith('http'):
                logo_url = 'http:' + logo_url
            response = requests.get(logo_url, timeout=10)
            img = Image.open(io.BytesIO(response.content))
            text = pytesseract.image_to_string(img)
            return text.strip()
        return 'No logo found'
    except Exception as e:
        print(f"An error occurred while analyzing the logo: {e}")
        return 'Error in logo analysis'

def main():
    conn, cursor = connect_db()
    query = input("Enter your Google search query: ")
    num_results = int(input("Enter the number of results you want to fetch: "))
    
    results = google_search(query, num_results)
    for url in results:
        domain = extract_domain(url)
        details = fetch_page_details(url)
        fake_check = is_fake_website(url)
        logo_text = analyze_logo(details['soup']) if details['soup'] else 'No soup'
        
        print(f"URL: {url}")
        print(f"Domain: {domain}")
        print(f"Title: {details['title']}")
        print(f"Description: {details['description']}")
        print(f"Is Fake: {'Yes' if fake_check else 'No'}")
        print(f"Logo Text: {logo_text}")
        print("-" * 80)
        
        save_to_db(cursor, url, domain, details['title'], details['description'], fake_check, logo_text)
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
