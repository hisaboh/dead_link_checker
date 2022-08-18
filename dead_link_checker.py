import requests
from bs4 import BeautifulSoup
import argparse
import re
from urllib.parse import urljoin
import sys
import os
import cssutils

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
    content_type = ''
    parent = url
    logger.write(url+ '\t' + from_url + '\t' + tag + '\t')
    logger.flush()
    try:
        res = requests.get(url, timeout=(5.0, 15.0))
        checked[url] = res.status_code
        content_type = res.headers['content-type'].lower()
        logger.write(content_type + '\t' + str(res.status_code))
        text = res.text
        parent = res.url
    except KeyboardInterrupt:
        raise
    except:
        logger.write('ERROR' + '\t' + 'ERROR')
    logger.write('\n')
    logger.flush()

    # 外部サイトはこれ以上チェックしない
    if url.startswith(base) == False:
        return

    if content_type.startswith("application"):
        return

    if content_type.startswith('text/css'):
        css = cssutils.parseString(text)
        for rule in css:
            if rule.type == rule.STYLE_RULE:
                for prop in [p for p in rule.style if p.name == 'background-image']:
                    for value in cssutils.css.PropertyValue(prop.value):
                        if value.type == value.URI:
                            if value.uri.startswith("data:") == False:
                                src = urljoin(parent, value.uri)
                                check(src, url, 'css background-image')

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
os.makedirs("out", exist_ok=True)
logger = Logger("out/out.tsv")
logger.write('URL\tFROM URL\tTAG\tCONTENT-TYPE\tSTATUS\n')

checked = {}
base = args.url
check(base, 'NONE', 'NONE')
