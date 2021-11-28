from requests.api import head
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import urllib
from urllib.error import HTTPError, URLError
from typing import List


CHROME_EXECUTABLE_PATH = r"C:\Users\gridx\workspace\college_work\gitWork\link-scanner\chromedriver.exe"


def get_links(url: str) -> list:
    """Find all links on page at the given url.
    
    Args:
        url: website url

    Returns:
        a list of all unique hyperlinks on the page,
        without page fragments or query parameters.
    """

    service = Service(CHROME_EXECUTABLE_PATH)
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    browser = webdriver.Chrome(options=chrome_options, service=service)
    browser.get(url)
    hyperlink_list = browser.find_elements('tag name', 'a')
    out = []
    for a in hyperlink_list:
        url = a.get_attribute('href')
        if url is None:
            continue
        link = url.split('#')[0]
        link = link.split('?')[0]
        out.append(link)
    return list(set(out))
    

def is_valid_url(url: str) -> bool:
    """Validate url and return false if url is bad, else true

    Args:
        url: website url
    
    Returns:
        bool: False if url is bad

    """
    # bypass bot checker
    header = {'User-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5'} 
    request = urllib.request.Request(url, None, header)
    try:
        conn = urllib.request.urlopen(request)
        return True
    except HTTPError:
        return False
    except URLError:
        return False


def invalid_urls(url_list: List[str]) -> List[str]:
    """Validate the urls in urllist and return a new list containing
    the invalid or unreachable urls.

    Args:
        url_list: list of all url that got from get_url
    
    Return:
        invalid_url_out: list of invalid url check by use is_valid_url func
    """
    invalid_url_out = []
    for url in url_list:
        if not is_valid_url(url):
            invalid_url_out.append(url)
    return invalid_url_out


if __name__ == "__main__":
    import sys
    import os
    filename = os.path.basename(sys.argv[0])
    num_args = len(sys.argv)
    if num_args != 2:
        print(f"Usage:  python3 {filename} url\n\nTest all hyperlinks on the given url.")
        sys.exit()
    url = sys.argv[1]

    url_list = get_links(url)
    for url in url_list:
        print(url)
    print("\nBad Links:")
    for url in invalid_urls(url_list):
        print(url)
