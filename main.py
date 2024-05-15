from crawler.generalCrawler import Crawler
import matplotlib.pyplot as plt

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