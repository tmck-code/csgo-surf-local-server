#!/usr/bin/env python3

from collections import namedtuple
from itertools import count
import os
import time
from typing import Iterable, List
import urllib

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import tabulate

BASE_URL = 'https://surfheaven.eu'

from surf_heaven import init_browser, download_map, find_local_maps, parse_args, ppd

MapSearchResult = namedtuple('MapSearchResult', ['name', 'url', 'map_type', 'map_tier'])

def get_results_table(soup) -> Iterable[MapSearchResult]:
    results_table = soup.find('table', {'id': 'DataTables_Table_1'})
    for row in results_table.find('tbody').find_all('tr'):
        link, map_type, map_tier = row.find_all('td')

        yield MapSearchResult(
            name     = link.text,
            url      = BASE_URL+link.find('a').attrs['href'],
            map_type = map_type.text,
            map_tier = map_tier.text,
        )

def search_maps(driver, search_url):
    driver.get(search_url)

    ppd({'msg': 'fetched search results page', 'url': search_url})

    current_page = []

    for page_num in count(1):
        ppd({'msg': f'fetching page {page_num}'})
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        previous_page = current_page
        current_page = list(get_results_table(soup))

        if current_page == previous_page:
            ppd({'msg': 'reached end of results'})
            break
        yield from current_page

        driver.find_element(By.XPATH, '//*[@id="DataTables_Table_1_next"]/a').click()


def map_search_result_to_row(result):
    'Converts a map search result to a row for the table'
    return [
        result.name,
        result.url,
        result.map_type,
        result.map_tier,
    ]


def create_results_table(search_results: List[MapSearchResult]):
    'Creates a table from the server list'
    return tabulate.tabulate(
        # sort entries alphabetically by name
        sorted(list(map(map_search_result_to_row, search_results)), key=lambda s: s[0]),
        headers=['name', 'URL', 'type', 'tier'],
        tablefmt='rounded_grid',
    )


def run(search_url, csgo_map_dir, download_dir='.', interactive=True) -> Iterable[MapSearchResult]:
    driver = init_browser(download_dir=os.getcwd())

    ppd({'msg': 'fetching search results', 'url': search_url})

    results = list(search_maps(driver, search_url))
    ppd({'msg': f'found maps', 'n': len(results)})

    local_maps = list(find_local_maps(csgo_map_dir))
    ppd({'msg': f'found local maps', 'n': len(results)})

    todo = [map for map in results if map.name not in local_maps]
    print(create_results_table(todo))
    ppd({'msg': f'fetching maps', 'n': len(todo)})

    for i, map in enumerate(todo):
        try:
            download_map(
                driver       = driver,
                map_url      = map.url,
            )
        except urllib.error.HTTPError as e:
            ppd({
                'msg': 'file download failed',
                'map_url': map.url,
                'error': {'class': type(e), 'message': str(e)}
            })


if __name__ == '__main__':
    run(**parse_args()|{'search_url': 'https://surfheaven.eu/search/tier%202'})
