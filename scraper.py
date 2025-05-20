import time
import yaml
import csv
import logging
from utils import get_random_headers, load_proxies
from captcha_solver import CaptchaSolver2Captcha
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

logging.basicConfig(filename="scraper.log", level=logging.INFO)

class AdvancedScraper:
    def __init__(self, start_url):
        self.start_url = start_url
        self.visited = set()
        self.load_config()
        self.results = []

    def load_config(self):
        with open("config.yaml", "r") as f:
            cfg = yaml.safe_load(f)
        self.proxies = load_proxies(cfg.get("proxies", []))
        self.delay = cfg.get("delay", 2)
        self.api_key = cfg.get("captcha_api_key", "")
        self.export_csv = cfg.get("export_csv", True)

    def run(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox"
                ]
            )
            context = browser.new_context(user_agent=get_random_headers()["User-Agent"])
            page = context.new_page()
            url = self.start_url

            while url and url not in self.visited:
                self.visited.add(url)
                try:
                    logging.info(f"Scraping: {url}")
                    page.goto(url, timeout=60000, wait_until="networkidle")

                    try:
                        page.wait_for_selector("h3", timeout=15000)
                    except PlaywrightTimeoutError:
                        logging.warning("No titles found or bot protection")
                        continue

                    self.simulate_human_interaction(page)
                    self.scroll_to_bottom(page)

                    soup = BeautifulSoup(page.content(), "html.parser")
                    self.extract_data(soup, url)

                    url = self.find_next_page(soup, url)
                    time.sleep(self.delay)
                except Exception as e:
                    logging.error(f"Error scraping {url}: {e}")
                    break

            browser.close()
            if self.export_csv:
                self.save_to_csv()

    def simulate_human_interaction(self, page):
        page.mouse.move(100, 100)
        page.keyboard.press("ArrowDown")
        time.sleep(1)

    def scroll_to_bottom(self, page):
        prev_height = 0
        for _ in range(5):
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(2)
            curr_height = page.evaluate("document.body.scrollHeight")
            if curr_height == prev_height:
                break
            prev_height = curr_height

    def extract_data(self, soup, page_url):
        titles = soup.find_all("h3")
        for title in titles:
            text = title.get_text(strip=True)
            print("[+] ", text)
            self.results.append({"url": page_url, "title": text})

    def find_next_page(self, soup, current_url):
        return None  # Reddit uses infinite scroll, handled already

    def save_to_csv(self):
        with open("scraped_data.csv", "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["url", "title"])
            writer.writeheader()
            writer.writerows(self.results)
        print("[*] Data saved to scraped_data.csv")
