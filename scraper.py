import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

BASE_URL = "https://books.toscrape.com/"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def get_categories():
    res = requests.get(BASE_URL, headers=HEADERS)
    soup = BeautifulSoup(res.text, 'html.parser')
    category_tags = soup.select('.side_categories ul li ul li a')
    categories = []
    for tag in category_tags:
        name = tag.text.strip()
        relative_url = tag['href']
        categories.append((name, relative_url))
    return categories

def scrape_books(category_url):
    books = []

    if category_url == "all":
        page_url = urljoin(BASE_URL, "catalogue/page-1.html")
        category_name = "All"
    else:
        page_url = urljoin(BASE_URL, category_url)
        category_name = category_url.split('/')[-2]  # e.g., 'travel_2'

    while True:
        print(f"Scraping {page_url}")
        res = requests.get(page_url, headers=HEADERS)
        soup = BeautifulSoup(res.text, 'html.parser')
        time.sleep(1)  # Respectful delay

        for book in soup.select('article.product_pod'):
            title = book.h3.a['title']
            price = book.select_one('.price_color').text.strip()
            rating_class = book.p['class'][1]  # e.g., "One", "Three"
            rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

            books.append({
                "Title": title,
                "Price": price,
                "Rating": rating_map.get(rating_class, 0),
                "Category": category_name
            })

        # Check for next page
        next_page = soup.select_one('li.next a')
        if next_page:
            next_url = next_page['href']
            page_url = urljoin(page_url, next_url)
        else:
            break

    return books
