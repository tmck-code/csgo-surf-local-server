#!/usr/bin/env python3
'''
Visits the SurfHeaven server page, looks at the AU servers, finds any maps that are not
already in the local maps dir and downloads/unzips/copies them to the local dir.

Usage:
./ops/scripts/surfheaven.py \
    /some/location/SteamLibrary/steamapps/common/Counter-Strike\ Global\ Offensive/csgo/maps/
'''

from argparse import ArgumentParser
import bz2, json
import os, sys, glob, shutil, re
import time
from datetime import datetime

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import tabulate

SERVER_LIST_URL = 'https://surfheaven.eu/servers'

# OTT pretty-printing code ----------------------
from pygments import lexers, formatters, styles, highlight
def ppd(d, indent=None, style='material'):
    'pretty-prints a dictionary, used for simple logs'
    print(highlight(json.dumps(d, indent=indent), lexers.JsonLexer(), formatters.TerminalTrueColorFormatter(style=styles.get_style_by_name(style))).strip())

def wait_for_download(download_dir):
    'finds the first .crdownload file and waits for it to finish downloading (aka disappear)'
    start_time = datetime.now()
    time.sleep(0.1)
    pending_fpath = glob.glob('*.crdownload')[0]
    while True:
        if os.path.exists(pending_fpath):
            ppd({'msg': 'downloading', 'pending_fpath': pending_fpath, 'elapsed': str(datetime.now() - start_time), 'size': f'{os.path.getsize(pending_fpath)/(1024*1024):.02f} MB'}, style='paraiso-dark')
            time.sleep(3)
            continue
        else:
            ppd({'msg': 'downloaded', 'downloaded_fpath': pending_fpath.removesuffix('.crdownload')})
            break
    return pending_fpath.removesuffix('.crdownload')

def parse_map_info(soup):
    'Parse the surfheaven map page html into a dictionary'
    info = {}
    # { "Completions": 313, "Times Played": 295, "Tier": 3, "stage_type": "Staged", "Bonus": 4, "Stage": 12 }
    for i, el in enumerate(soup.find('table').find_all('td')):
        _, v, k = [e.get_text(strip=True) for e in el.contents]
        if k == '':
            info['stage_type'] = v
        else:
            info[k.lower()] = int(v)
    # { "author": "Spy Complex", "added": "2021-07-12" }
    for el in soup.find('div', {'class': 'media'}).find('p').contents:
        row = el.get_text(strip=True)
        if row.startswith('Author:'):
            info['author'] = row.split('Author: ')[1]
        elif row.startswith('Added:'):
            info['added'] = row.split('Added: ')[1]
    return info


def get_map_info(driver, map_url):
    'Visits the map page and returns the map info'
    driver.get(map_url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    info = parse_map_info(soup)
    return info


def download_map(driver, map_url):
    'Visits the map page, clicks the download button and waits for the file to download'
    driver.get(map_url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

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
        return
    else:
        fpath = wait_for_download('.')
    return fpath

def list_current_servers(driver):
    'Visits the server list page and parses the info of the AU servers'
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
    'Yields the names of the maps in the CSGO maps directory'
    for fpath in glob.glob(os.path.join(csgo_map_dir, '*.bsp')):
        # yield the filename without the extension,
        # e.g. 'surf_utopia_njv.bsp' -> 'surf_utopia_njv
        yield os.path.basename(os.path.splitext(fpath)[0])

def bzip2_decompress(fpath):
    'Decompresses a .bz2 file and returns the path to the decompressed file'
    # files might not be compressed
    if not fpath.endswith('.bz2'):
        return fpath
    with bz2.open(fpath, 'rb') as istream, open(fpath.removesuffix('.bz2'), 'wb') as ostream:
        ostream.write(istream.read())
    return fpath.removesuffix('.bz2')

def init_browser(download_dir):
    'Initialises a headless chrome browser'
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option('prefs', {'download.default_directory': download_dir})

    return webdriver.Chrome(options=options)


def server_to_row(server):
    'Converts a server dictionary to a row for the table'
    return [
        server['name'],
        server['host'],
        server['map']['name'],
        server['map']['tier'],
        server['map']['stage_type'],
        server['map']['url'],
        f"{server['map']['completions']:,d}",
        f"{server['map']['times played']:,d}",
        server['map']['author'],
        server['map']['added'],
        server['local']
    ]

def create_table(servers):
    'Creates a table from the server list'
    return tabulate.tabulate(
        list(map(server_to_row, servers)),
        headers=['name', 'host', 'map', 'tier', 'stage_type', 'url', 'completions', 'times played', 'author', 'added', 'local'],
        tablefmt='rounded_grid',
    )

def run(csgo_map_dir, download_dir='.', interactive=True):
    'Visits the server list page, fetches the map info, downloads any maps that are not already in the local dir'

    ppd({'msg': 'initialising browser', 'download_dir': download_dir, 'csgo_map_dir': csgo_map_dir, 'interactive': interactive})
    driver = init_browser(download_dir=os.getcwd())

    local_maps = list(find_local_maps(csgo_map_dir))
    ppd({'msg': 'found local maps', 'n_maps': len(local_maps), 'map_dir': csgo_map_dir})

    ppd({'msg': 'fetching current server list', 'url': SERVER_LIST_URL})
    servers = list(list_current_servers(driver))


    ppd({'msg': 'fetching map info for server maps', 'n_servers': len(servers), 'maps': [s['map']['name'] for s in servers]})

    for server in servers:
        info = {'map': server['map']['name']} | get_map_info(driver, server['map']['url'])
        server['map'].update(info)
        if server['map']['name'] in local_maps:
            server['local'] = '✓'
        else:
            server['local'] = '✗'
        ppd(info, style='paraiso-dark')

    print('-> ALL SERVERS')
    print(create_table(servers))

    todo = [s for s in servers if s['local'] == '✗']
    if not todo:
        ppd({'msg': 'No maps to download! exiting'})
        return
    print('-> MAPS TO DOWNLOAD')
    print(create_table(todo))

    if interactive:
        input('press enter to download...')

    # count downloaded/exists
    downloaded = []
    for i, server in enumerate(servers):
        if server['local'] == '✓':
            continue
        ppd({'msg': 'downloading map to CSGO maps dir', 'i': i+1, 'total': len(servers), 'map': server['map']['name']})
        bzip_fpath = download_map(driver, server['map']['url'])

        if bzip_fpath is None:
            continue
        # unzip, copy to csgo maps dir, remove temp/downloaded files
        fpath = bzip2_decompress(bzip_fpath)
        shutil.copy(fpath, csgo_map_dir)
        downloaded.append(server['map']['name'])
        for fpath in {bzip_fpath, fpath}:
            os.remove(fpath)
        ppd({'msg': 'downloaded map to CSGO maps dir', 'i': i+1, 'total': len(servers), 'map': server['map']['name']})

    driver.close()

    ppd({'downloaded': downloaded}, indent=2)

def parse_args():
    'Parses the command line arguments'
    parser = ArgumentParser(description='SurfHeaven map downloader')
    parser.add_argument('-c', '--csgo-map-dir', help='path to the CSGO maps directory')
    parser.add_argument('-d', '--download-dir', help='path to the download directory', default='.', required=False)
    parser.add_argument('-n', '--no-interactive', action='store_false', dest='interactive', help='do not prompt for download confirmation')

    return parser.parse_args().__dict__

if __name__ == '__main__':
    run(**parse_args())
