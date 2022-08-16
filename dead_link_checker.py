import requests
from bs4 import BeautifulSoup
import argparse
import re
from urllib.parse import urljoin

def check(url: str, from_url: str):
    if url in checked:
        return

    checked[url] = 0
    resp = requests.get(url)
    checked[url] = resp.status_code
    print(str(resp.status_code) + '\t' + url+ '\t' + from_url)

    if url.startswith(base) == False:
        return

    soup = BeautifulSoup(resp.text, 'html.parser')

    for img in soup.find_all('img'):
        src = img.get('src')
        if src is None:
            continue
        elif src.startswith('#'):
            continue
        src = urljoin(url, src)
        check(src, url)

    for link in soup.find_all('a'):
        child_url = link.get('href')
        if child_url is None:
            continue
        elif child_url.startswith('#'):
            continue
        child_url = urljoin(url, child_url)
        check(child_url, url)

parser = argparse.ArgumentParser()
parser.add_argument("url", help="url the url you want to check")
args = parser.parse_args()

checked = {}
base = args.url
check(base, '')

