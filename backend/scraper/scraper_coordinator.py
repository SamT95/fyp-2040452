from classes.cybok_scraper import CybokScraper
from classes.cisa_scraper import CisaScraper
from classes.cve_scraper import CveScraper

def fetch_all_content():
    # Fetch all the content from the different sources
    scrapers = [CybokScraper(), CisaScraper(), CveScraper()]
    content = []
    for scraper in scrapers:
        content.append(scraper.extract_all_data())
    return content