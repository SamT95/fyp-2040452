import requests
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
import nltk
import spacy
import re

nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords


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

    def format_text(self, text):
        """
        Removes whitespace and newlines and lowercases the text
        """
        formatted_text = re.sub(r'\s+', ' ', text)
        formatted_text = formatted_text.lower()
        return formatted_text

    def remove_stopwords(self, text):
        """
        Removes stopwords from the text
        """
        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(text)
        filtered_text = [word for word in word_tokens if word not in stop_words]
        return ' '.join(filtered_text)
    
    def tokenize_into_sentences(text):
        """
        Tokenizes the input text into sentences using the spaCy library
        
        Parameters:
        text (str): The text to be tokenized

        Returns:
        list: A list of sentences
        """
        nlp = spacy.load('en_core_web_sm')
        doc = nlp(text)
        sentences = [sent.text for sent in doc.sents]
        return sentences

    def lemmatize_text(self, text):
        """
        Lemmatizes the text

        Parameters:
        text (str): The text to lemmatize

        Returns:
        str: The lemmatized text
        """
        nlp = spacy.load('en_core_web_sm')
        doc = nlp(text)
        lemmatized_text = ' '.join([token.lemma_ for token in doc])
        return lemmatized_text
    