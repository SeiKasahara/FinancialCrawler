import requests
import yaml
import random as rd
import time
import re
from crawler.generalCrawler import Crawler
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from nltk.corpus import stopwords


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


def visualize(tuple_list:list, rang:int):
    plt.scatter(*zip(*tuple_list[:rang]))
    plt.xlabel('words')
    plt.ylabel('frequency')
    plt.xticks(rotation=45)
    plt.show()

if __name__ == "__main__": 
    c = Crawler()
    c.get_file_and_read('website.yaml')
    result = c.get_sitemap_links(True)
    print(result)