import requests
from bs4 import BeautifulSoup
import argparse
import re
from urllib.parse import urljoin
import sys
import os

class Logger:
    def __init__(self, filename: str):
        self.console = sys.stdout
        self.file = open(filename, 'w')
 
    def write(self, message: str):
        self.console.write(message)
        self.file.write(message)
 
    def flush(self):
        self.console.flush()
        self.file.flush()


def check(target_url: str, from_url: str, tag: str):
    url = ''.join(target_url.splitlines())
    if url in checked:
        return

    checked[url] = 0
    text = ''
    parent = url
    logger.write(url+ '\t' + from_url + '\t' + tag + '\t')
    logger.flush()
    try:
        res = requests.get(url)
        checked[url] = res.status_code
        logger.write(res.headers['content-type'] + '\t' + str(res.status_code))
        text = res.text
        parent = res.url
    except KeyboardInterrupt:
        raise
    except:
        logger.write('ERROR' + '\t' + 'ERROR')
    logger.write('\n')
    logger.flush()

    if url.startswith(base) == False:
        return

    soup = BeautifulSoup(text, 'html.parser')

    for script in soup.find_all('script'):
        src = script.get('src')
        if src is None:
            continue
        elif src.startswith('#'):
            continue
        src = urljoin(parent, src)
        check(src, url, '<script>')

    for link in soup.find_all('link'):
        href = link.get('href')
        if href is None:
            continue
        elif href.startswith('#'):
            continue
        href = urljoin(parent, href)
        check(href, url, '<link>')

    for img in soup.find_all('img'):
        src = img.get('src')
        if src is None:
            continue
        elif src.startswith('#'):
            continue
        src = urljoin(parent, src)
        check(src, url, '<img>')

    for link in soup.find_all('a'):
        child_url = link.get('href')
        if child_url is None:
            continue
        elif child_url.startswith('#'):
            continue
        child_url = urljoin(parent, child_url)
        check(child_url, url, '<a>')

parser = argparse.ArgumentParser()
parser.add_argument("url", help="url the url you want to check")
args = parser.parse_args()
os.makedirs("out")
logger = Logger("out/out.tsv")
logger.write('URL\tFROM URL\tTAG\tCONTENT-TYPE\tSTATUS\n')

checked = {}
base = args.url
check(base, 'NONE', 'NONE')
