from scraper import AdvancedScraper

if __name__ == "__main__":
    url = input("Enter the URL to scrape: ").strip()
    scraper = AdvancedScraper(start_url=url)
    scraper.run()
