import time
import os
import re
import requests
import random as rd
import yaml
from bs4 import BeautifulSoup
import sqlite3

class Crawler:

    def __init__(self) -> None:
        self.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'DNT': '1',
        'Connection': 'keep-alive',
        }
        self.__url_list = []
        self.__sitemap_sub_links = {} # sitemap of a site
        self.file = ""

    def get_file_and_read(self, file:str):
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', file)
        self.file = file_path
        self.read_yaml()

    def get_sitemap_links(self, flag:bool):
        """
        if flag = True, return the value. Default set flag = 0 \\
        But no matter how, this function will record the site and sitemap into a sql table.
        """
        for url in self.__url_list:
            time.sleep(rd.randint(1,6))
            try:
                response = requests.get(url, headers=self.headers)
                soup = BeautifulSoup(response.content, 'lxml')
                start = url.find("//") + 2
                end = url.find("/", start)
                hostname = url[start:end]
                hostname = hostname.replace(".", "_")
                self.__sitemap_sub_links[hostname] = [element.text for element in soup.find_all('loc')]
            except:
                print("error!")
                continue
        self.dict_to_insert_sql()
        if flag:
            return self.__sitemap_sub_links

    def read_yaml(self):
        try:
            with open(self.file, encoding='utf-8') as f:
                self.__url_list = yaml.load(f, Loader=yaml.FullLoader) # read yaml file
        except:
            print('yaml file doesn\'t exist!')
            raise FileNotFoundError('yaml file doesn\'t exist!')

    def dict_to_insert_sql(self):
        if len(self.__sitemap_sub_links) == 0:
            return
        database_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'database')
        os.makedirs(database_path, exist_ok=True)
        conn = sqlite3.connect(os.path.join(database_path, 'sitemap.db'))
        c = conn.cursor()
        # Create Table
        for site, urls in self.__sitemap_sub_links.items():
            c.execute(f'''
            CREATE TABLE IF NOT EXISTS {site} (
                link TEXT
                )
            ''')
            for url in urls:
                c.execute(f'INSERT INTO {site} VALUES (?)', (url,))
        # Commit the transaction after the loop
        conn.commit()
        conn.close()

    