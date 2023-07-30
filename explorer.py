import requests
from bs4 import BeautifulSoup

# Function to get href values
def get_href_values(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Parse the HTML content of the page with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all 'div' tags with align="center" in the document
    div_tags = soup.find_all('div', {'align': 'center'})
    
    # Create a set to store unique href values
    href_set = set()
    
    # For each 'div' tag found, find 'a' tags within and add the 'href' attribute to the set
    for tag in div_tags:
        a_tags = tag.find_all('a')
        for a_tag in a_tags:
            href_value = a_tag.get('href')
            # Only add href values that start with "ed2k"
            if href_value.startswith("ed2k"):
                href_set.add(href_value)
    
    # Order the href values
    href_list = sorted(list(href_set))
    
    # Export the href values to a text file
    with open('href_values.txt', 'w') as file:
        for href_value in href_list:
            file.write(href_value + '\n')
    
    # Print the unique href values
    for href_value in href_list:
        print(href_value)

# Call the function with your URL
get_href_values('http://lamansion-crg.net/forum/index.php?showtopic=96333')
