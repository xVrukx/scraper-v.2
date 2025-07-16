🛠️ Alibaba RFQ Scraper using Selenium + BeautifulSoup
This is a web scraping project that extracts Request For Quotation (RFQ) data from Alibaba's sourcing portal using Selenium and BeautifulSoup. It collects buyer request details from multiple pages and saves them into a CSV file.

📌 Features
✅ Headless browser scraping (no UI popup)

✅ Handles pagination automatically

✅ Extracts:

Title & Description

Quantity and Units

Country, Buyer Name, Posted Time

Inquiry Detail Page URL

Tags like:

Experienced Buyer

Complete RFQ Order

Typical Replies

Interactive User

Email Confirmation

✅ Saves all data to alibaba.csv

🧰 Technologies Used
Python 3

Selenium

BeautifulSoup (bs4)

pandas

re (Regex)

📦 Installation
Clone the repository:
git clone https://github.com/yourusername/alibaba-rfq-scraper.git
cd alibaba-rfq-scraper

Install the required libraries:
pip install selenium beautifulsoup4 pandas
Download ChromeDriver matching your Chrome version and place it in your project folder or system PATH.

🚀 Usage
Just run the script:
python scrap.py
This will launch the browser in headless mode, navigate through all RFQ pages, and save the scraped data to:

📝 Output Sample
Title	Quantity Required	Unit	Buyer Name	Country	Inquiry URL
LED Strip	1000	pcs	John Buyer	UAE	https://sourcing.alibaba.com/...
Mobile Phone	200	pcs	Sarah L.	India	https://sourcing.alibaba.com/...

⚠️ Notes
Alibaba may change DOM structure often, so selector adjustments might be needed.

Avoid scraping too frequently to prevent getting blocked.

Consider adding proxy or delay logic for production use.

👤 Author
Vruk
🚀 Passionate about scraping, automation, and smart data pipelines.
📧 For freelance/project help: developeryuvrajsirganor@gmail.com