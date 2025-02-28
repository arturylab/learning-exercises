"""
This script is designed to scrape specific div elements from a given webpage URL using the BeautifulSoup library in Python. 
It includes a decorator to handle potential HTTP errors during the request process. 
The main function, get_divs, sends a GET request to the specified URL (Warcarft Wiki), parses the HTML content, 
and extracts text from div elements with class names 'ClassLink', 'ProfLink', and 'RaceLink'. 
The extracted text is then printed to the console, categorized by their class names.
"""

import requests
from bs4 import BeautifulSoup


def handle_request(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An error occurred: {err}")
    return wrapper


@handle_request
def get_div(url):
    """
    Fetches and prints the text content of specific div elements from a given URL.
    Args:
        url (str): The URL of the webpage to scrape.
    Raises:
        requests.exceptions.HTTPError: If the HTTP request returned an unsuccessful status code.
    Decorators:
        handle_request: A decorator to handle the request.
    The function performs the following steps:
        1. Sends a GET request to the specified URL.
        2. Parses the HTML content of the response using BeautifulSoup.
        3. Searches for div elements with class names 'ClassLink', 'ProfLink', and 'RaceLink'.
        4. Prints the text content of each found div element, categorized by their class name.
    """
    # Send a GET request to the server
    response = requests.get(url)
    response.raise_for_status()
    
    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    class_list = ['ClassLink', 'ProfLink', 'RaceLink']

    for class_name in class_list:
        # Find all divs
        div = soup.find_all('div', class_=class_name)

        print(f"\n{class_name}:")

        # Print the extracted titles
        for index, div in enumerate(div, start=1):
            print(f"{index}. {div.text.strip()}")


# URL of the page we want to scrape
url = 'https://warcraft.wiki.gg/'

# Call the functions
get_div(url)