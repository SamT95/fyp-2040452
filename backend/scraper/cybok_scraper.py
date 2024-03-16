from .base_scraper import BaseScraper
from bs4 import BeautifulSoup
import requests
import fitz # PyMuPDF
import re
import io

# Data is being fetched from the CyBOK website. The information therein is licensed under the Open Government Licence v3.0.
# The data is free for use, provided that the following attribution is included:
# CyBOK © Crown Copyright, The National Cyber Security Centre 2021,
# licensed under the Open Government Licence: http://www.nationalarchives.gov.uk/doc/open-government-licence/.

individual_pdf_links_url = "https://www.cybok.org/knowledgebase1_1/"
combined_pdf_url = "https://www.cybok.org/media/downloads/CyBOK_v1.1.0.pdf"


class CybokScraper(BaseScraper):
    def __init__(self, url=combined_pdf_url):
        super().__init__(url)

        
    def remove_patterns(self, text, patterns):
        """
        This function removes patterns from the text.

        Parameters:
        text (str): The text to be cleaned.
        patterns (list): A list of patterns to be removed.

        Returns:
        str: The cleaned text.
        """
        for pattern in patterns:
            text = re.sub(pattern, '', text, flags=re.DOTALL)
        return text
    
    def clean_cybok_pdf_text(self, text):
        """
        This function removes patterns found in the CyBok PDFs.

        Parameters:
        text (str): The text to be cleaned.

        Returns:
        str: The cleaned text.
        """
        patterns = [
            r"The Cyber Security Body Of Knowledge", # remove the header title
            r"www.cybok.org", # remove the header and other links
            r"Page \d+", # remove page numbers
        ]

        text = self.remove_patterns(text, patterns)
        return text
        
    
    def chunk_text(self, text, chunk_size=1000):
        """
        This function chunks the text into smaller pieces.

        Parameters:
        text (str): The text to be chunked.
        chunk_size (int): The size of the chunks. Default is 1000.

        Returns:
        list: A list of chunks of text.
        """
        chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
        return chunks
        
    def preprocess_text(self, text):
        """
        This function preprocesses the text using the base scraper's preprocessing functions.

        Parameters:
        text (str): The text to be preprocessed.

        Returns:
        str: The preprocessed text.
        """
        text = self.clean_cybok_pdf_text(text)
        text = self.format_text(text)
        # text = self.remove_stopwords(text)
        # text = self.lemmatize_text(text)
        return text
        
    
    def get_pdf_filestream(self, pdf_page):
        """
        This function gets the filestream of a PDF.

        Parameters:
        pdf_page (requests.models.Response): The PDF page.

        Returns:
        io.BytesIO: The filestream of the PDF.
        """
        return io.BytesIO(pdf_page.content)
    
    def filestream_to_document(self, filestream):
        """
        This function converts the filestream to a fitz Document.

        Parameters:
        filestream (io.BytesIO): The filestream of the PDF.

        Returns:
        fitz.fitz.Document: The PDF document.
        """
        return fitz.open(stream=filestream, filetype="pdf")
    
    def extract_chapter_content(self, doc, toc):
        """
        This function extracts the content of each chapter from the PDF.

        Parameters:
        doc (fitz.fitz.Document): The PDF document.
        toc (list): The table of contents of the PDF.

        Returns:
        list: A list of dictionaries containing the title and text of each section.
        """
        extracted_text = []
        for i, toc_item in enumerate(toc):
            level, title, start_page = toc_item

            # Determine the end page of the current section
            # which is the start page of the next section (toc[level+1][2])
            end_page = toc[i+1][2] if i + 1 < len(toc) else len(doc)
            section_text = ""
            for page_number in range(start_page, end_page):
                page = doc.load_page(page_number)
                page_text = page.get_text()
                page_text = self.preprocess_text(page_text)
                section_text += page_text
            
            extracted_text.append({
                "source": self.url,
                "title": title,
                "text": section_text
            })
        return extracted_text
    
    def get_document_toc(self, doc):
        """
        This function gets the table of contents of the PDF.
        It also removes items under the "Appendix" section.

        Parameters:
        doc (fitz.fitz.Document): The PDF document.

        Returns:
        list: The table of contents of the PDF.
        """
        toc = doc.get_toc()
        appendix_start_index = None
        # Find the index of the "VI Appendix" chapter
        # Everything following this chapter is non-essential
        for i, (level, title, start_page) in enumerate(toc):
            if title.strip().upper() == "VI APPENDIX":
                appendix_start_index = i
                break
        if appendix_start_index is not None:
            # Exclude "VI Appendix" and any sub-sections that follow
            # This assumes the sub-chapters have a higher 'level' than the 'VI Appendix' chapter
            # indicating that they are children of the 'VI Appendix' chapter
            toc_without_appendix = [item for i, item in enumerate(toc) if i < appendix_start_index or item[0] < toc[appendix_start_index][0]]
            return toc_without_appendix
        else:
            # Return the original TOC if the "VI Appendix" chapter is not found
            return toc
    
    def extract_all_data(self):
        """
        This function coordinates the data fetching and cleaning functions within the CyBOK scraper
        and returns data as a list of dictionaries containing the title and text of each section.

        Returns:
        list: A list of dictionaries containing the title and text of each section.
        """
        pdf_page = self.get_page()
        filestream = self.get_pdf_filestream(pdf_page)
        doc = self.filestream_to_document(filestream)
        toc = self.get_document_toc(doc)
        extracted_text = self.extract_chapter_content(doc, toc)
        return extracted_text




# Example usage:
if __name__ == "__main__":
    cybok_scraper = CybokScraper()
    # pdf_text = cybok_scraper.test_combined_pdf()
    # # pdf_text = cybok_scraper.extract_all_data()
    # print(pdf_text[0])
    test_text = cybok_scraper.extract_all_data()
    print(test_text[1])