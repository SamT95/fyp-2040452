from .base_scraper import BaseScraper


class CisaScraper(BaseScraper):
    def __init__(self, url="https://www.cisa.gov/news-events/cybersecurity-advisories"):
        super().__init__(url)

    def collect_alert_links(self):
        """
        This function collects all the page links from the CISA website.
        """
        links = self.get_links()
        # filter to only include cyber security alerts
        # i.e. links pointing to /news-events/alerts/* or /news-events/ics-advisories/*
        filtered_links = [link for link in links if link and ("/news-events/alerts/" in link or "/news-events/ics-advisories/" in link)]
        # prepend links with the base url
        filtered_links = [f"https://www.cisa.gov{link}" for link in filtered_links]
        print(f"Found {len(filtered_links)} alert links: {filtered_links}")

        return filtered_links
    
    def get_alert(self, link):
        """
        This function gets the alert from the given link.
        """
        alert_scraper = BaseScraper(link)
        # get text from the l-full__main class
        alert = {}
        alert["title"] = alert_scraper.get_title()
        alert["text"] = alert_scraper.get_soup().find("div", class_="l-full__main").get_text()
        alert["source"] = link
        return alert
    
    def clean_text(self, text):
        """
        This function cleans the text by removing whitespace, newlines, and lowercasing the text.
        """
        formatted_text = self.format_text(text)
        return formatted_text
    
    def extract_all_data(self):
        """
        This function collects all the alerts from the CISA website.
        """
        alert_links = self.collect_alert_links()
        alerts = []
        for link in alert_links:
            alert = self.get_alert(link)
            alert["text"] = self.clean_text(alert["text"])
            alerts.append({
                "title": alert["title"],
                "source": alert["source"],
                "text": alert["text"],
            })
        print(alerts)
        return alerts


    

if __name__ == "__main__":
    cisa_scraper = CisaScraper()
    cisa_scraper.extract_all_data()