import requests
from bs4 import BeautifulSoup
import argparse
import re
from urllib.parse import urljoin
import sys

class Logger:
    def __init__(self, filename: str):
        self.console = sys.stdout
        self.file = open(filename, 'w')
 
    def write(self, message: str):
        self.console.write(message + '\n')
        self.file.write(message + '\n')
 
    def flush(self):
        self.console.flush()
        self.file.flush()


def check(url: str, from_url: str):
    if url in checked:
        return

    checked[url] = 0
    text = ''
    try:
        res = requests.get(url)
        checked[url] = res.status_code
        logger.write(res.headers['content-type'] + '\t' + str(res.status_code) + '\t' + url+ '\t' + from_url)
        logger.flush()
        text = res.text
    except:
        logger.write('ERROR' + '\t' + 'ERROR' + '\t' + url+ '\t' + from_url)
        logger.flush()

    if url.startswith(base) == False:
        return

    soup = BeautifulSoup(text, 'html.parser')

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
logger = Logger("out.tsv")

checked = {}
base = args.url
check(base, '')

