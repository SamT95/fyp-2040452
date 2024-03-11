from base_scraper import BaseScraper
from bs4 import BeautifulSoup
import requests
import fitz # PyMuPDF

# Data is being fetched from the CyBOK website. The information therein is licensed under the Open Government Licence v3.0.
# The data is free for use, provided that the following attribution is included:
# CyBOK © Crown Copyright, The National Cyber Security Centre 2021,
# licensed under the Open Government Licence: http://www.nationalarchives.gov.uk/doc/open-government-licence/.


class CybokScraper(BaseScraper):
    def __init__(self, url="https://www.cybok.org/knowledgebase1_1/"):
        super().__init__(url)
    
    def collect_pdf_links(self):
        """
        This function collects all the PDF links from the Cybok website.
        """
        links = self.get_links()
        base_url = "https://www.cybok.org"
        # filter all hrefs containing "webinar" or "tree", or those not pointing to the /media/downloads slug
        filtered_links = [link for link in links if "webinar" not in link and "tree" not in link and "/media/downloads" in link]
        pdf_links = [base_url + link for link in filtered_links if link.endswith(".pdf")]
        print(f"Found {len(pdf_links)} PDF links: {pdf_links}")

        return pdf_links

    def extract_pdf_text(self, pdf_url):
        """
        This function extracts the text from a PDF file.
        """
        response = requests.get(pdf_url)
        if response.status_code == 200:
            with fitz.open("pdf", response.content) as doc:
                text = ""
                for page in doc:
                    text += page.get_text()
                text = self.clean_text(text)
                return text
        else:
            print(f"Error fetching {pdf_url}: {response.status_code}")
            return None
        
    def extract_all_data(self):
        """
        This function collects all the PDF links from the Cybok website and extracts the text from each PDF.
        """
        pdf_links = self.collect_pdf_links()
        pdf_text = []
        for link in pdf_links:
            text = self.extract_pdf_text(link)
            pdf_text.append(text)
        return pdf_text