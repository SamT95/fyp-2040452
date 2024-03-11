from base_scraper import BaseScraper

class CveScraper(BaseScraper):
    def __init__(self, url="https://github.com/CVEProject/cvelistV5/releases/latest"):
        super().__init__(url)
        # Get the latest release from the CVEProject GitHub.

    def get_latest_cve_zip(self):
        """
        This function collects the latest CVE zip file from the CVEProject GitHub Releases page.
        """
        page_links = self.get_links()
        print(f"Links are: {page_links}")
        # filter to only include links containing /releases/downloads
        # also, only include the link to the delta .zip file (i.e. the one containing "delta" in the name)
        # this is because the full .zip file contains all the CVEs, and the delta .zip file contains only the new CVEs
        filtered_links = [link for link in page_links if "/CVEProject" in link]
        print(f"Found {len(filtered_links)} delta zip links: {filtered_links}")

        return filtered_links
    

if __name__ == "__main__":
    cve_scraper = CveScraper()
    cve_scraper.get_latest_cve_zip()
