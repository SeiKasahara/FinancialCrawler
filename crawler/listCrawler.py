import requests
import itertools
import time
import random as rd
import sqlite3
from crawler.generalCrawler import Crawler
from bs4 import BeautifulSoup
import concurrent.futures

class listCrawler(Crawler):

    def __init__(self):
        super().__init__()
        self.sitemap_urls = {}
        self.url_name_list = []
        self.text_dict = {}

    def get_url_list(self, urls:list):
        self.sitemap_urls = urls

    def fetch_data(self, table_name:str, filename:str):
        conn = sqlite3.connect(self.path_getter(filename))
        c = conn.cursor()
        c.execute(f"SELECT * FROM {table_name}")
        rows = c.fetchall()
        conn.close()
        return [row[0] for row in rows] #only return the first col data

    def sql_reader(self, filename:str):
        """
        tables:list
        """
        conn = sqlite3.connect(self.path_getter(filename))
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = c.fetchall()
        conn.close()
        self.url_name_list = [table_name[0] for table_name in tables]
    
    def sitemap_list_getter(self, filename:str):
        self.sql_reader(filename)
        # create a thread
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(self.fetch_data, self.url_name_list, [filename]*len(self.url_name_list))
        self.sitemap_urls = dict(zip(self.url_name_list, results))

    def get_words(self, controller:bool, test_range:int, return_controller:bool):
        text_dict = {}
        count = 1
        if controller:
            self.sitemap_urls = dict(itertools.islice(self.sitemap_urls.items(), test_range))
        for url_name, urls in self.sitemap_urls.items():
            time.sleep(rd.randint(1,3))
            if controller:
                urls = urls[:test_range]
            for url in urls:
                try:
                    response = requests.get(url, headers=self.headers)
                except:
                    raise TimeoutError
                soup = BeautifulSoup(response.content, 'lxml')
                text_dict[url_name + " " + str(count)] = soup.get_text()
                count += 1
        self.text_dict = text_dict
        if return_controller:
            return self.text_dict

"""
if __name__ == "__main__":
    c = listCrawler()
    c.sitemap_list_getter('sitemap.db')
    text_dict = c.get_words(True, 3, True)
    print(text_list)
"""