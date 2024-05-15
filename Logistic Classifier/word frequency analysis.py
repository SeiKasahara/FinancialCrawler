import re
import os
import sqlite3
from crawler.generalCrawler import Crawler
from nltk.corpus import stopwords
import concurrent.futures

regular = r" |▮|,|\.|'|!|@|#|\$|%|\^|&|\*|\n|\r|\t|-|–|’|：|……|（|）|\[|\]|《|》|\||！|，|。|；|\/|”|“|？|:|;|\\"
regular_2 = "\\【.*?】+|\\《.*?》+|\\#.*?#+|[.!/_,$&%^*()<>+""'?@|:~{}#]+|[——！\\\，。=？、：“”‘’￥……（）《》【】]\n\r\t"

def remove_numbers_from_string(s):
    return re.sub(r'\d+', '', s)

def calculate(word_list:list):
    word_dict = {}
    for word in word_list:
        word = word.lower()
        if word in word_dict:
            word_dict[word] += 1
        else:
            word_dict[word] = 1
    word_dict = sorted(word_dict.items(), key= lambda item:item[1], reverse=True) #sort
    return word_dict

def list_refine(ls, regular:str, regular_2:str):
    ls = re.split(regular, ls)
    ls = [re.sub(regular_2, '', words) for words in ls]
    ls = [remove_numbers_from_string(s) for s in ls]
    ls = [w for w in ls if w not in stopwords.words('english')]
    ls = [item for item in ls if item.strip() or len(item) > 1]
    return ls

def path_getter(filename:str):
    database_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'database')
    os.makedirs(database_path, exist_ok=True)
    return os.path.join(database_path, filename)

def fetch_data(table_name, filename):
    conn = sqlite3.connect(path_getter(filename))
    c = conn.cursor()
    c.execute(f"SELECT * FROM {table_name}")
    rows = c.fetchall()
    conn.close()
    return [row[0] for row in rows] #only return the first col data

def sql_reader(filename:str):
    conn = sqlite3.connect(path_getter(filename))
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = c.fetchall()
    conn.close()
    return tables

def main():
    filename = 'sitemap.db'
    tables = sql_reader(filename)
    # create a thread
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(fetch_data, [table_name[0] for table_name in tables], [filename]*len(tables))
    for result in results:
        print(result)

def sql_saver():
    pass

if __name__ == '__main__':
    main()