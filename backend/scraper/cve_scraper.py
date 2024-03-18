from .base_scraper import BaseScraper
import requests
import zipfile
import io
import json

class CveScraper(BaseScraper):
    def __init__(self, url="https://api.github.com/repos/CVEProject/cvelistV5/releases/latest"):
        super().__init__(url)
        # Get the latest release from the CVEProject GitHub.

    def get_latest_cve_zip(self):
        """
        This function collects the latest CVE zip file from the CVEProject GitHub Releases page.
        """
        # page_links = self.get_links()
        page_data = self.page.json()
        assets = page_data.get("assets", [])
        # Only pull out the 'delta_CVEs' zip file
        latest_zip = [asset for asset in assets if "delta_CVEs" in asset.get("name", "")][0]
        return latest_zip
    
    def process_cve_zip(self, zip_url):
        """
        This function processes the CVE zip file by extracting the contents and returning the filestream.

        Parameters:
        zip_url (str): The URL of the zip file.

        Returns:
        zipfile.ZipFile: The filestream of the zip file.
        """
        print(f"Zip URL: {zip_url}")
        zip_response = requests.get(zip_url)
        zip_response.raise_for_status()
        zip_bytes = io.BytesIO(zip_response.content)


        # Open the zip file and process the json files within the "deltaCves" folder
        json_data = []
        with zipfile.ZipFile(zip_bytes, "r") as zip_ref:
           for zip_info in zip_ref.infolist():
               print(zip_info.filename)
               if zip_info.filename.endswith(".json"):
                   with zip_ref.open(zip_info.filename) as json_file:
                        # Decode file bytes to string
                        content_string = json_file.read().decode("utf-8")
                        # Convert string to json
                        content_json = json.loads(content_string)
                        json_data.append(content_json)
        return json_data

    def process_json_files(self, json_files):
        """
        This function processes the json files within the zip file.

        Parameters:
        json_files (list): A list of json files to process.
        """
        # Pull out the relevant data from the json files
        cve_data_list = []
        for json_file in json_files:
            cve_id = json_file.get("cveMetadata", {}).get("cveId", "")
            cve_published_data = json_file.get("cveMetadata", {}).get("datePublished", "")
            cve_containers = json_file.get("containers", {}).get("cna", {})
            affected_products_list = cve_containers.get("affected", [])[0] if cve_containers.get("affected") else None
            affected_products = affected_products_list.get("product") if affected_products_list else None
            cve_description_list = cve_containers.get("descriptions", [])[0] if cve_containers.get("descriptions") else None
            cve_description = cve_description_list.get("value") if cve_description_list else None
            cve_references = cve_containers.get("references", [])
            # References field is an array of dictionaries and needs to be formatted
            # to be stored in a Pinecone index
            cve_references = [ref.get("url", "") for ref in cve_references]
            formatted_cve_data = {
                "cve_id": cve_id,
                "published_date": cve_published_data,
                "affected_products": affected_products if affected_products is not None else "N/A",
                "description": cve_description if cve_description is not None else "N/A",
                "references": cve_references
            }
            cve_data_list.append(formatted_cve_data)
        return cve_data_list
    
    def extract_all_data(self):
        latest_zip = self.get_latest_cve_zip()
        json_data = self.process_cve_zip(latest_zip["browser_download_url"])
        formatted_cve_data = self.process_json_files(json_data)
        return formatted_cve_data
