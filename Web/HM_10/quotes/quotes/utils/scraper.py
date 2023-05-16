import logging
import csv
import json
import re
from time import time, sleep

import requests
from bs4 import BeautifulSoup as BS

from .logger import get_logger

logger = get_logger(__name__)

URL = "http://127.0.0.1:8000/"


def write_to_csv(quote, author, tags):
    """Write quotes to csv file"""
    try:
        with open('quotes/utils/data/items.csv', 'a', newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([quote, author, [tag for tag in tags]])
            logger.info(f"|Write to csv: {quote}, {author}, {[tag for tag in tags]}")
    except Exception as err:
        logger.error(f'[ERROR] {err}')


def get_info(urls):
    """Get info: quote, author, tags"""
    try:
        num_of_quotes = 0
        json_quotes = []
        for url in urls:
            try:
                link = requests.get(url)
                soup = BS(link.text, "html.parser")
                class_quotes = soup.find('div', class_='col-md-8 themed-gris-col')

                for bloc_quote in class_quotes.find_all('div', class_='quote'):
                    quote, author, tags = "", "", []
                    quote_ = bloc_quote.find('span', class_='text')
                    author_ = bloc_quote.find('small', class_='author')
                    tags_cl = bloc_quote.find('div', class_='tags')

                    if quote_:
                        quote = quote_.text.strip()
                    if author_:
                        author = author_.text.strip()
                    if tags_cl:
                        for a in tags_cl.find_all('a', class_='tag'):
                            tags.append(a.text.strip())

                    if quote and author:
                        num_of_quotes += 1
                        write_to_csv(quote, author, tags)
                        json_quotes.append({"Quote": quote, "Author": author, "Tags": tags})

            except Exception as err:
                logger.error(f'[ERROR] {err}')

        return json_quotes, num_of_quotes

    except Exception as err:
        logger.error(f'[ERROR] {err}')


def all_urls(pages: int, main_url):
    """Get all urls"""
    try:
        pack_urls = []
        prefix = "/?page="
        for num in range(1, pages + 1):
            url = main_url + prefix + str(num)
            pack_urls.append(url)
        return pack_urls
    except Exception as err:
        logger.error(f'[ERROR] {err}')


def get_all_pages(url):
    """Get all pages with quotes"""
    try:
        link = requests.get(url)
        soup = BS(link.text, "html.parser")
        paginator = soup.find('span', class_='current').text
        '''Find last digit'''
        num_of_pages = re.search(r'.+([0-9])[^0-9]*$', paginator).group(1)
        return int(num_of_pages)
    except Exception as err:
        logger.error(f'[ERROR] {err}')


def start_parse():
    timer = time()
    logger.log(level=logging.DEBUG, msg=f"Start")
    num_pages = get_all_pages(URL)
    urls = all_urls(num_pages, URL)
    json_quotes, num_of_quotes = get_info(urls)
    sleep(1)
    logger.info(f"|{num_of_quotes} items were processed")
    print(f'Work time {round(time() - timer, 2)} sec')
    return json_quotes


