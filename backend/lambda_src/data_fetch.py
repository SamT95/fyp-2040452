# WIP
# Currently, this code just fetches PDFs from CyBOK (Cyber Security Body of Knowledge) and stores them in a local directory.
# The next steps include fetching a wider variety of content, and storing the fetched documents in an S3 bucket.
# Automated or scheduled fetching of content is also a possibility that is being explored.

import requests
import os
from bs4 import BeautifulSoup

# Data is being fetched from the CyBOK website. The information therein is licensed under the Open Government Licence v3.0.
# The data is free for use, provided that the following attribution is included:
# CyBOK © Crown Copyright, The National Cyber Security Centre 2021,
# licensed under the Open Government Licence: http://www.nationalarchives.gov.uk/doc/open-government-licence/.

def collect_cybok_pdf_links():
    """
    Fetches PDFs URLs from the CyBOK website and returns them as a list.
    This function uses BeautifulSoup to parse the HTML of the CyBOK website.
    All the `div` tags with the class `document-row` are selected, and the `href` attribute of the `a` tag is extracted.
    If the `href` attribute ends with `.pdf`, it is added to the dictionary of PDF URLs.
    """

    cybok_knowledge_url = "https://www.cybok.org/knowledgebase1_1/"
    cybok_base_url = "https://www.cybok.org/"
    cybok_knowledge_page = requests.get(cybok_knowledge_url)

    if cybok_knowledge_page.status_code != 200:
        print(f"Error fetching {cybok_knowledge_url}")
        return None
    soup = BeautifulSoup(cybok_knowledge_page.content, 'html.parser')
    pdf_links = {}
    for div in soup.find_all("div", class_="document-row"):
        pdf_link = div.find("a", href=lambda href: href and href.endswith(".pdf"))
        title = pdf_link["title"].replace(" download link", "")
        pdf_links[title] = cybok_base_url + pdf_link["href"]
    
    return pdf_links

def save_pdfs_locally(pdf_links):
    """
    Saves the PDFs locally in a directory called `pdfs`.
    """

    # Create a directory called `pdfs` if it doesn't exist
    os.makedirs("pdfs", exist_ok=True)

    for title, pdf_link in pdf_links.items():
        pdf = requests.get(pdf_link)
        if pdf.status_code != 200:
            print(f"Error fetching {pdf_link}")
            continue
        with open(f"pdfs/{title}.pdf", "wb") as f:
            f.write(pdf.content)
        print(f"Saved {title}.pdf")

def main():
    pdf_links = collect_cybok_pdf_links()
    save_pdfs_locally(pdf_links)

if __name__ == "__main__":
    main()

