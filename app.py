from flask import Flask, render_template, request, send_file
from scraper import scrape_books, get_categories
import csv
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    categories = get_categories()
    search_query = request.args.get('search', '').strip()
    page = int(request.args.get('page', 1))
    books = []

    # Only load books if the user entered a search query
    if search_query and os.path.exists('books.csv'):
        with open('books.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if search_query.lower() in row['Title'].lower():
                    books.append(row)

    # Pagination logic
    books_per_page = 10
    total_pages = max(1, (len(books) + books_per_page - 1) // books_per_page) if books else 1
    start = (page - 1) * books_per_page
    end = start + books_per_page
    paginated_books = books[start:end] if books else []

    return render_template(
        'index.html',
        categories=categories,
        books=paginated_books if search_query else None,
        status="",
        logs=None,
        search_query=search_query,
        current_page=page,
        total_pages=total_pages
    )

@app.route('/scrape', methods=['POST'])
def scrape():
    selected = request.form.get('category')
    categories = get_categories()

    # Find the readable category name
    category_name = next((name for name, url in categories if url == selected), "All")

    # Log using category name instead of URL
    logs = [f"Started scraping category: {category_name}"]
    books = scrape_books(selected)
    logs.append(f"Finished scraping. Total books: {len(books)}")

    # Save to CSV
    filename = 'books.csv'
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['Title', 'Price', 'Rating', 'Category'])
        writer.writeheader()
        for book in books:
            writer.writerow(book)

    return render_template(
        'index.html',
        categories=categories,
        books=books,
        status=f"Scraped {len(books)} books.",
        logs=logs,
        search_query="",
        current_page=1,
        total_pages=1
    )

@app.route('/download')
def download():
    filepath = 'books.csv'
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    return "No CSV found. Please scrape first."

if __name__ == '__main__':
    app.run(debug=True)
