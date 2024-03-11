from base_scraper import BaseScraper


class CisaScraper(BaseScraper):
    def __init__(self, url="https://www.cisa.gov/news-events/cybersecurity-advisories"):
        super().__init__(url)

    def collect_pdf_links(self):
        """
        This function collects all the page links from the CISA website.
        """
        links = self.get_links()
        # filter to only include cyber security alerts
        # i.e. links pointing to /news-events/alerts/*
        filtered_links = [link for link in links if "/news-events/alerts/" in link]
        print(f"Found {len(filtered_links)} alert links: {filtered_links}")

        return filtered_links