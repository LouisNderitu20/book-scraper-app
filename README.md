# 📚 Book Scraper App

The **Book Scraper App** is a simple and elegant Flask-based web application that scrapes book data from [Books to Scrape](http://books.toscrape.com/) by category and displays the results in a clean, paginated table. You can search through scraped books and export them to a downloadable CSV file.

---

## 🚀 Features

- 🔎 Scrape books by category from books.toscrape.com
- 📥 Download scraped data as a `.csv` file
- 🔍 Search functionality
- 📄 Pagination for easy navigation through large results
- ✅ Clean, modern, and professional UI

---

## 🛠 Technologies Used

- Python 3.x
- Flask
- BeautifulSoup (bs4)
- Requests
- HTML5 & CSS3

---

## 🧰 Setup Instructions

1. Clone the repository
   ```bash
   git clone https://github.com/LouisNderitu20/book-scraper-app.git
   cd book-scraper-app
2. Create a virtual environment (recommended)
python -m venv venv
# Activate it:
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
Install dependencies

3. Install dependencies.
pip install -r requirements.txt

4. Run the app
python app.py

5.Visit in browser
http://localhost:5000

📁 Project Structure

book-scraper-app/
│
├── templates/
│   └── index.html         # Main HTML template
├── static/
│   └── style.css          # CSS styling
├── scraper.py             # Scraper logic using requests + BeautifulSoup
├── app.py                 # Flask web server
├── books.csv              # Generated data file (after scraping)
├── requirements.txt       # List of required Python packages
└── README.md              # Project documentation (this file)

📝 License
This project is open source and available under the MIT License.

🙋‍♂️ Author
Louis Nderitu
Frontend Developer | UI Designer



