import re
import sqlite3
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

