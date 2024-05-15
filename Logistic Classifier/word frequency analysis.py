import sys
import os

current_path = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.dirname(current_path)
sys.path.append(root_path)

import re
from crawler.listCrawler import listCrawler
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
    word_tuple_list = sorted(word_dict.items(), key= lambda item:item[1], reverse=True) #sort
    return word_tuple_list

def list_refine(ls, regular:str, regular_2:str):
    ls = re.split(regular, ls)
    ls = [re.sub(regular_2, '', words) for words in ls]
    ls = [remove_numbers_from_string(s) for s in ls]
    ls = [w for w in ls if w not in stopwords.words('english')]
    ls = [item for item in ls if item.strip() or len(item) > 1]
    return ls

def dict_cleaning_calculate(text_dict:dict, regular:str, regular_2:str):
    new_dict = {}
    for url_name, text in text_dict.items():
        text = text.strip()
        text = list_refine(text, regular, regular_2)
        text = calculate(text)
        new_dict[url_name] = text
    return new_dict

def main(regular, regular_2):
    craw = listCrawler()
    craw.sitemap_list_getter('sitemap.db')
    text_dict = craw.get_words(True, 3, True)
    text_dict = dict_cleaning_calculate(text_dict, regular, regular_2)
    print(text_dict)

if __name__ == '__main__':
    main(regular, regular_2)