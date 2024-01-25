#!/usr/bin/env python3

import os
import re
import json

from bs4 import BeautifulSoup
from selenium import webdriver


SERVER_LIST_URL = 'https://surfheaven.eu/servers'

def list_current_servers(driver):
    driver.get(SERVER_LIST_URL)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    for row in soup.find('table', {'id': 'logsTable'}).find_all('tr'):
        img = row.find('img')
        if img is not None and img.attrs['src'] == '/flags/au.svg':
            name, host, surf_map, *_ = row.find_all('td')
            tier, stage_type = re.match(r'\((\w+)\) (\w+)', surf_map.find('small').get_text(strip=True)).groups()
            info = {
                'name': name.text.removesuffix('Online Players'),
                'host': host.get_text(strip=True),
                'map': {
                    'name':       surf_map.find('a').get_text(strip=True),
                    'tier':       tier,
                    'stage_type': stage_type,
                    'url':        'https://surfheaven.eu'+surf_map.find('a')['href'],
                }
            }
            yield info

def init_browser():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option('prefs', {'download.default_directory': os.getcwd()})

    return webdriver.Chrome(options=options)

if __name__ == '__main__':
    driver = init_browser()

    servers = list(list_current_servers(driver))
    driver.close()
    print(json.dumps(servers, indent=2))

