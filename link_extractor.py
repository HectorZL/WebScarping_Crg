import requests
from bs4 import BeautifulSoup
import re

class LinkExtractor:
    def extract_links(self, url):
        links = []
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")

            for a_tag in soup.find_all("a"):
                href_value = a_tag.get("href")
                if href_value and href_value.startswith("ed2k"):
                    links.append(href_value)

        except requests.exceptions.RequestException as e:
            return None

        return links

    def is_valid_url(self, url):
        valid_url_pattern = r'^http://lamansion-crg\.net/forum/.*$'
        return bool(re.match(valid_url_pattern, url))
