import requests
from bs4 import BeautifulSoup
import re

class BaseScraper:
    def __init__(self, url):
        self.url = url
        headers = {
            'User-Agent': 'UP2040452/UoP'
        }
        try:
            response = requests.get(url, headers=headers, allow_redirects=True)
            response.raise_for_status()
            # if there is a redirect, follow it and fetch again
            if response.url != url:
                print(f"Redirected to {response.url}")
                response = requests.get(response.url, headers=headers, allow_redirects=True)
                response.raise_for_status()

            self.page = response
            self.soup = BeautifulSoup(self.page.content, 'html.parser')
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")

    def get_soup(self):
        return self.soup

    def get_page(self):
        return self.page

    def get_url(self):
        return self.url

    def get_title(self):
        return self.soup.title.string

    def get_text(self):
        return self.soup.get_text()
    
    def get_links(self):
        links = self.soup.find_all('a')
        return [link.get('href') for link in links]

    def clean_text(self, text):
        """
        This function is used to slightly clean the text extracted from the PDFs.
        The text is cleaned to remove any unwanted characters or formatting.
        This function can be modified to include additional cleaning steps as required.
        """
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove newlines
        text = re.sub(r'\n', ' ', text)
        # Remove tabs
        text = re.sub(r'\t', ' ', text)

        return text

    