import requests
import yaml
import random as rd
import time
import re
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from nltk.corpus import stopwords


regular = r" |▮|,|\.|'|!|@|#|\$|%|\^|&|\*|\n|\r|\t|-|–|’|：|……|（|）|\[|\]|《|》|\||！|，|。|；|\/|”|“|？|:|;|\\"
regular_2 = "\\【.*?】+|\\《.*?》+|\\#.*?#+|[.!/_,$&%^*()<>+""'?@|:~{}#]+|[——！\\\，。=？、：“”‘’￥……（）《》【】]\n\r\t"
url_list = []
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'DNT': '1',
    'Connection': 'keep-alive',
}

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

def request(url_list:list, headers:dict):
    bs_text_list = []
    for url in url_list:
        time.sleep(rd.randint(1,5))
        try:
            content = requests.get(url, headers=headers)
        except Exception as e:
            print(f"Error when requesting {url}: {e}")
            return None
        bs = BeautifulSoup(content.text, "html.parser")
        text = bs.get_text()
        bs_text_list.append(text)
    return bs_text_list

def get_sitemap_links(sitemap_url:list, headers:dict):
    for sitemaps in sitemap_url:
        time.sleep(rd.randint(1,6))
        response = requests.get(sitemaps, headers=headers)
        soup = BeautifulSoup(response.content, 'lxml')
        links = [element.text for element in soup.find_all('loc')]
    return links

def visualize(tuple_list:list, rang:int):
    plt.scatter(*zip(*tuple_list[:rang]))
    plt.xlabel('words')
    plt.ylabel('frequency')
    plt.xticks(rotation=45)
    plt.show()

def read_yaml(file:str):
    with open(file,encoding='utf-8') as file1:
        data = yaml.load(file1,Loader=yaml.FullLoader) # read yaml file
    return data

if __name__ == "__main__": 
    sitemap_list = read_yaml('website.yaml')
    links = get_sitemap_links(sitemap_list, headers)
    url_list += links[:3]
    texts = request(url_list, headers)
    for text in texts:
        words = list_refine(text, regular, regular_2)
        word_freq = calculate(words)
        visualize(word_freq, 20)
        print(word_freq[:20])