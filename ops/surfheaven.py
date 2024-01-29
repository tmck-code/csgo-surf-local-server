#!/usr/bin/env python3

import bz2
import glob
import json
import os
import re
import sys
import shutil
import time
from collections import Counter, defaultdict

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import tabulate

SERVER_LIST_URL = 'https://surfheaven.eu/servers'

# OTT pretty-printing code ----------------------
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalTrueColorFormatter as Formatter
from pygments.styles import get_style_by_name

def ppd(d, indent=None, style='material'):
    print(highlight(json.dumps(d, indent=indent), JsonLexer(), Formatter(style=get_style_by_name(style))).strip())

def wait_for_download(download_dir):
    time.sleep(2)
    pending_fpath = glob.glob('*.crdownload')[0]
    while True:
        if os.path.exists(pending_fpath):
            ppd({'msg': 'downloading', 'pending_fpath': pending_fpath})
            time.sleep(3)
            continue
        else:
            ppd({'msg': 'downloaded', 'pending_fpath': pending_fpath.removesuffix('.crdownload')})
            break
    return pending_fpath.removesuffix('.crdownload')

def get_map_info(soup):
    info = {}
    # {
    #   "Completions": 313,
    #   "Times Played": 295,
    #   "Tier": 3,
    #   "stage_type": "Staged",
    #   "Bonus": 4,
    #   "Stage": 12
    # }
    for i, el in enumerate(soup.find('table').find_all('td')):
        _, v, k = [e.get_text(strip=True) for e in el.contents]
        if k == '':
            info['stage_type'] = v
        else:
            info[k] = int(v)
    # {
    #   "author": "Spy Complex",
    #   "added": "2021-07-12"
    # }
    for el in soup.find('div', {'class': 'media'}).find('p').contents:
        row = el.get_text(strip=True)
        if row.startswith('Author:'):
            info['author'] = row.split('Author: ')[1]
        elif row.startswith('Added:'):
            info['added'] = row.split('Added: ')[1]
    return info


def download_map(driver, map_url):
    driver.get(map_url)
    ppd({'msg': 'fetching map URL', 'map_url': map_url})
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    info = get_map_info(soup)
    ppd(info, indent=2)

    # find the download button and click it
    map_download_url = soup.find('a', {'title': 'Download'})['href']
    xpath = '/html/body/div[2]/section/div/div[1]/div/div/div/div[1]/div/h2/a'
    driver.execute_script(
      'arguments[0].click();',
      WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, xpath))),
    )
    ppd({'msg': 'file download started', 'map_url': map_url})

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    heading = soup.find('h1')
    if heading is not None and heading.get_text() == '404 Not Found':
        print({'404 error': map_download_url})
    else:
        fpath = wait_for_download('.')
    return fpath

def list_current_servers(driver):
    driver.get(SERVER_LIST_URL)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    for row in soup.find('table', {'id': 'logsTable'}).find_all('tr'):
        img = row.find('img')
        if img is None or img.attrs['src'] != '/flags/au.svg':
            continue

        name, host, surf_map, *_ = row.find_all('td')
        tier, stage_type = re.match(r'\((\w+)\) (\w+)', surf_map.find('small').get_text(strip=True)).groups()
        yield {
            'name': name.text.split('Online Players')[0],
            'host': host.get_text(strip=True),
            'map': {
                'name':       surf_map.find('a').get_text(strip=True),
                'tier':       tier,
                'stage_type': stage_type,
                'url':        'https://surfheaven.eu'+surf_map.find('a')['href'],
            }
        }

def find_local_maps(csgo_map_dir):
    for fpath in glob.glob(os.path.join(csgo_map_dir, '*.bsp')):
        # yield the filename without the extension,
        # e.g. 'surf_utopia_njv.bsp' -> 'surf_utopia_njv
        yield os.path.basename(os.path.splitext(fpath)[0])

def bzip2_decompress(fpath):
    # files might not be compressed
    if not fpath.endswith('.bz2'):
        return fpath
    with bz2.open(fpath, 'rb') as istream, open(fpath.removesuffix('.bz2'), 'wb') as ostream:
        ostream.write(istream.read())
    return fpath.removesuffix('.bz2')

def init_browser():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option('prefs', {'download.default_directory': os.getcwd()})

    ppd({'msg': 'using download directory', 'directory': os.getcwd()})

    return webdriver.Chrome(options=options)


def server_to_row(server):
    return [
        server['name'],
        server['host'],
        server['map']['name'],
        server['map']['tier'],
        server['map']['stage_type'],
        server['map']['url'],
    ]

def create_table(servers):
    return tabulate.tabulate(
        [server_to_row(server) for server in servers],
        headers=['name', 'host', 'map', 'tier', 'stage_type', 'url'],
        tablefmt='fancy_grid',
    )

def run(csgo_map_dir):
    driver = init_browser()
    servers = list(list_current_servers(driver))
    local_maps = list(find_local_maps(csgo_map_dir))

    print(create_table(servers))

    todo = [server for server in servers if server['map']['name'] not in local_maps]
    input('press enter to download')


# count downloaded/exists
    counts = defaultdict(list)
    for i, server in enumerate(todo):
        ppd({'msg': 'checking server map', 'map': server['map']['name'], 'i': i, 'total': len(servers)})

        bzip_fpath = download_map(driver, server['map']['url'])
        fpath = bzip2_decompress(bzip_fpath)
        shutil.copy(fpath, csgo_map_dir)
        counts['downloaded'].append(server['map']['name'])
        ppd({'msg': 'downloaded map to CSGO maps dir', 'map': server['map']['name']})

        for fpath in {bzip_fpath, fpath}:
            os.remove(fpath)
    driver.close()

    ppd(counts, indent=2)



if __name__ == '__main__':
    run(csgo_map_dir=sys.argv[1])
