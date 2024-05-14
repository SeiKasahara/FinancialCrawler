from flask import Flask, request, render_template
import re
import yaml

app = Flask(__name__)

def is_sitemap_url(url):
    pattern = r'https?://[\w\.-]+/[\w\.-]*sitemap[\w\.-]*\.xml'
    if re.match(pattern, url):
        return True
    return False

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        url = request.form.get('url')
        if is_sitemap_url(url) == False:
            return '''
            <script>
                alert('URL is not match for sitemaps!');
                window.location.href = '/';
            </script>
        '''
        with open('website.yaml', 'r') as file:
            urls = yaml.safe_load(file)
        if urls is None:
            urls = []

        if url not in urls:
            urls.append(url)
        else:
            return '''
            <script>
                alert('URL already exists');
                window.location.href = '/';
            </script>
        '''
        with open('website.yaml', 'w') as file:
            yaml.safe_dump(urls, file)
        return '''
            <script>
                alert('URL added successfully!');
                window.location.href = '/';
            </script>
        '''
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)