from flask import Flask, request, render_template
import time
import re
from googlesearch import search
import yaml

# css file: static/styles.css
# index.html file: templates/index.html

app = Flask(__name__)

def is_sitemap_url(url:str):
    if url == "":
        return False
    pattern = r'https?://[\w\.-]+/[\w\.-]*sitemap[\w\.-]*\.xml'
    if re.match(pattern, url):
        return True
    return False

def que(query:str, num_results:int):
    """
    display (num) results from google search
    """
    url_list = []
    for url in search(query, num_results=num_results):
        url_list.append(url)
    return url_list

def alert_and_redirect(message:str):
    return f'''
    <script>
        alert('{message}');
        window.location.href = '/';
    </script>
    '''

@app.route('/', methods=['GET', 'POST'])
def home():
    result = []
    if request.method == 'POST':
        query = request.form.get('query')
        url = request.form.get('url')

        if query:
            analyse_result = que(query, 100)
            result = analyse_result[:10]
            try:
                with open('searchsite.yaml', 'w') as file:
                    yaml.safe_dump(analyse_result, file)
            except IOError:
                return alert_and_redirect('Failed to write to file')
            return alert_and_redirect('Sites added successfully!')

        if url:
            if not is_sitemap_url(url):
                return alert_and_redirect('URL is not match for sitemaps!')

            try:
                with open('website.yaml', 'r') as file:
                    urls = yaml.safe_load(file)
            except IOError:
                urls = []

            if urls is None:
                urls = []

            if url in urls:
                return alert_and_redirect('URL already exists')
            
            urls.append(url)

            try:
                with open('website.yaml', 'w') as file:
                    yaml.safe_dump(urls, file)
            except IOError:
                return alert_and_redirect('Failed to write to file')

            return alert_and_redirect('URL added successfully!')

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)