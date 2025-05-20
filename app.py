import os
from scraper import AdvancedScraper

if __name__ == "__main__":
    url = os.getenv("SCRAPER_URL")
    if not url:
        raise ValueError("SCRAPER_URL environment variable not set")
    scraper = AdvancedScraper(start_url=url)
    scraper.run()
