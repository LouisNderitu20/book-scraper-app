import requests
from bs4 import BeautifulSoup
import time

BASE_URL = "https://books.toscrape.com/"

def get_categories():
    res = requests.get(BASE_URL)
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
    logs = []

    if category_url == "all":
        page_url = BASE_URL + "catalogue/page-1.html"
    else:
        page_url = BASE_URL + category_url

    page_num = 1
    while True:
        logs.append(f"Scraping page {page_num}...")
        res = requests.get(page_url)
        soup = BeautifulSoup(res.text, 'html.parser')
        time.sleep(1)

        for book in soup.select('article.product_pod'):
            title = book.h3.a['title']
            price = book.select_one('.price_color').text.strip()
            rating = book.p['class'][1]
            rating_map = {
                "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5
            }
            books.append({
                "Title": title,
                "Price": price,
                "Rating": rating_map.get(rating, 0),
                "Category": "All" if category_url == "all" else category_url.split('/')[2]
            })

        next_page = soup.select_one('li.next a')
        if next_page:
            next_url = next_page['href']
            if 'catalogue' in page_url:
                page_url = BASE_URL + "catalogue/" + next_url
            else:
                page_url = BASE_URL + "/".join(category_url.split('/')[:-1]) + "/" + next_url
            page_num += 1
        else:
            logs.append("Scraping complete.")
            break

    return books, logs

