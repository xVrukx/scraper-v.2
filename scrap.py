import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

BASE_URL = "https://sourcing.alibaba.com/rfq/rfq_search_list.htm?spm=a2700.8073608.1998677541.1.82be65aaoUUItC&country=AE&recently=Y&tracelog=newest"
HEADLESS = True

def get_driver():
    options = Options()
    if HEADLESS:
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--start-maximized')
        options.add_argument('--window-size=1920,1080')
    return webdriver.Chrome(options=options)

def scrape_rfq_page(driver):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    cards = soup.select("div.brh-rfq-item__main-info")
    data = []

    for card in cards:
        try:
            title = card.select_one("h1")
            desc = card.select_one("div.brh-rfq-item__detail")
            qty = card.select_one("div.brh-rfq-item__quantity")
            country = card.select_one("div.brh-rfq-item__country")
            quotes_left = card.select_one("div.brh-rfq-item__quote-left")
            posted_time = card.select_one("div.brh-rfq-item__publishtime")
            buyer_name = card.select_one("div.textt")
            tag_container = card.select_one("div.brh-rfq-item__buyer-tag")
            profile = card.select_one(".img-con > div")
            html = ''
            url = card.select_one('h1 > a')
            if url and url.has_attr('href'):
                href = url['href']
                if href.startswith('/rfq_detail.htm'):
                    html = ('https://sourcing.alibaba.com'+href)

            if qty:
                qty_n = qty.get_text(strip=True).lower().replace('quantity required:','').strip()
                qty_l = re.match(r'^(\d+)\s*(.*)', qty_n)
                if qty_l:
                    quantity_value = qty_l.group(1)
                    unit_value = qty_l.group(2)
                else:
                    quantity_value = ''
                    unit_value = ''
            else:
                quantity_value = ''
                unit_value = ''
            
            experienced = complete_rfq = typical_reply = interactive = email_status = 'No'

            if tag_container:
                tag_divs = tag_container.select('div > div')

                if len(tag_divs) > 0:
                    text = tag_divs[0].get_text(strip=True)
                    experienced = 'Yes' if 'Experienced buyer' in text else 'No'
                if len(tag_divs) > 1:
                    text = tag_divs[1].get_text(strip=True)
                    complete_rfq = 'Yes' if 'Complete order via RFQ' in text else 'No'
                if len(tag_divs) > 2:
                    text = tag_divs[2].get_text(strip=True)
                    typical_reply = 'Yes' if 'Typically replies' in text else 'No'
                if len(tag_divs) > 3:
                    text = tag_divs[3].get_text(strip=True)
                    interactive = 'Yes' if 'Interactive user' in text else 'No'
                if len(tag_divs) > 4:
                    text = tag_divs[4].get_text(strip=True)
                    email_status = 'Yes' if 'Email Confirmed' in text else 'No'

            data.append({
                "Title": title.get_text(strip=True) if title else '',
                "Description": desc.get_text(strip=True) if desc else '',
                "Quantity Required": quantity_value,
                "Unit": unit_value,
                "Quotes Left":quotes_left.get_text(strip=True) if quotes_left else '',
                "Location": country.get_text(strip=True) if country else '',
                "Buyer Name": buyer_name.get_text(strip=True) if buyer_name else '',
                "Experienced Buyer": experienced,
                "Complete Order via RFQ": complete_rfq,
                "Typical Replies": typical_reply,
                "Interactive User": interactive,
                "Email Status": email_status,
                "Buyer Profile": profile.get_text(strip=True) if profile else '',
                "Posted Time": posted_time.get_text(strip=True) if posted_time else '',
                "Inquiry Url": html,
            })
        except Exception as e:
            print(f"Error parsing card: {e}")

    return data

def scrape_all_pages():
    driver = get_driver()
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, 15)

    all_data = []
    page = 1

    while True:
        print(f"Scraping page {page}...")
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.brh-rfq-item__main-info")))
        all_data.extend(scrape_rfq_page(driver))

        try:
            # Check if the disabled span exists (only present at last page)
            driver.find_element(By.CSS_SELECTOR, 'span.next.disable')
            print("Reached last page.")
            break
        except:
            # Otherwise go next
            try:
                time.sleep(2)
                next_btn = driver.find_element(By.CSS_SELECTOR, 'a.next')
                next_btn.click()
                time.sleep(3)
                page += 1
            except Exception as e:
                print("No next button found or error:", e)
                break
    driver.quit()
    return all_data

def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"Saved {len(df)} records to {filename}")

if __name__ == '__main__':
    final_data = scrape_all_pages()
    save_to_csv(final_data, "alibaba.csv")