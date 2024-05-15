import requests
import bs4 as BeautifulSoup
import yaml

def find_sitemap(url:str):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    sitemap_tag = soup.find("link", {"rel" : "sitemap"})
    
    if sitemap_tag:
        return sitemap_tag.get('href')
    else:
        return None

def find_sitemap_in_robots_txt(url:str):
    response = requests.get(url + '/robots.txt')
    for line in response.text.splitlines():
        if line.startswith('Sitemap:'):
            return line.split(': ')[1]
    return None

def find_sitemap_in_common_locations(url:str):
    common_locations = ['/sitemap.xml', '/sitemap_index.xml']
    for location in common_locations:
        response = requests.get(url + location)
        if response.status_code == 200:
            return url + location
    return None

def find_sitemap_final(url:str):
    if find_sitemap(url) != None:
        url = find_sitemap(url)
        return url
    elif find_sitemap_in_robots_txt(url) != None:
        url = find_sitemap(url)
        return url
    elif find_sitemap_in_common_locations(url) != None:
        url = find_sitemap_in_common_locations(url)
        return url
    else:
        return

def get_domain_without_parse(url:str):
    protocol_end = url.find("//") + 2
    domain_end = url.find("/", protocol_end)
    if domain_end == -1:
        return url
    else:
        return url[:domain_end]

def site_map_finder(file:str):
    sitemap = []
    try:
        with open('searchsite.yaml', 'r') as file:
            urls = yaml.safe_load(file)
    except IOError:
        print("file searchsite.yaml not found")
        return
    for url in urls:
        url = get_domain_without_parse(url)
        if find_sitemap_final(url) != None:
            sitemap.append(find_sitemap_final(url))
        else:
            print("Cannot find sitemap")
            return
    try:
        with open('website.yaml', 'r') as file:
            yaml.safe_dump(sitemap, file)
    except IOError:
        print("file website.yaml is not found!")
        return
