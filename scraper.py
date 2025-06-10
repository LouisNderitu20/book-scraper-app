import requests
from bs4 import BeautifulSoup
import time
import csv
from urllib.parse import urljoin
from tqdm import tqdm

BASE_URL = 'http://books.toscrape.com/'
HEADERS = {'User-Agent': 'Mozilla/5.0'}

def get_category_links():
    res = requests.get(BASE_URL, headers=HEADERS)
    soup = BeautifulSoup(res.text, 'html.parser')
    links = soup.select('div.side_categories ul li ul li a')
    return [(link.text.strip(), urljoin(BASE_URL, link['href'])) for link in links]

def get_star_rating(star_class_list):
    mapping = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
    for word in mapping:
        if word in star_class_list:
            return mapping[word]
    return 0

def get_books_from_category(category_url):
    book_links = []
    page_url = category_url
    while True:
        res = requests.get(page_url, headers=HEADERS)
        soup = BeautifulSoup(res.text, 'html.parser')
        books = soup.select('article.product_pod h3 a')
        for book in books:
            book_links.append(urljoin(page_url, book['href']))
        next_page = soup.select_one('li.next a')
        if next_page:
            page_url = urljoin(page_url, next_page['href'])
        else:
            break
        time.sleep(1)
    return book_links

def get_book_details(book_url, category_name):
    res = requests.get(book_url, headers=HEADERS)
    soup = BeautifulSoup(res.text, 'html.parser')

    title = soup.select_one('div.product_main h1').text.strip()
    price = soup.select_one('p.price_color').text.strip()
    availability = soup.select_one('p.availability').text.strip()
    rating = get_star_rating(' '.join(soup.select_one('p.star-rating')['class']))
    description_tag = soup.select_one('#product_description ~ p')
    description = description_tag.text.strip() if description_tag else "No description"
    table = soup.select('table.table.table-striped')
    upc = ''
    if table:
        rows = table[0].select('tr')
        for row in rows:
            if 'UPC' in row.text:
                upc = row.select_one('td').text.strip()
                break

    return {
        'Title': title,
        'Price': price,
        'Availability': availability,
        'Rating': rating,
        'Category': category_name,
        'UPC': upc,
        'Description': description,
        'URL': book_url
    }

# =============== MAIN SCRIPT ===============

all_books = []
categories = get_category_links()

print(f"\n📚 Found {len(categories)} categories. Scraping all books...\n")

for category_name, category_url in tqdm(categories, desc="Categories"):
    book_links = get_books_from_category(category_url)
    for book_url in tqdm(book_links, desc=f"{category_name}", leave=False):
        try:
            book_data = get_book_details(book_url, category_name)
            all_books.append(book_data)
        except Exception as e:
            print(f"⚠️ Error scraping {book_url}: {e}")
        time.sleep(1)

# Save to CSV
with open('books_full_data.csv', mode='w', newline='', encoding='utf-8') as file:
    fieldnames = ['Title', 'Price', 'Availability', 'Rating', 'Category', 'UPC', 'Description', 'URL']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_books)

print(f"\n✅ Done! {len(all_books)} books saved to 'books_full_data.csv'.")
