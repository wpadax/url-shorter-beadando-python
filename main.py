from flask import Flask, render_template, redirect, url_for
from forms import ShortenUrlForm
import string
import random
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'

def generate_short_url():
    letters = string.ascii_lowercase + string.ascii_uppercase
    short_url = ''.join(random.choice(letters) for _ in range(6))
    return short_url

def read_data():
    with open('data.json', 'r') as f:
        data = json.load(f)
    return data

def write_data(data):
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = ShortenUrlForm()
    if form.validate_on_submit():
        url = form.url.data
        name = form.name.data or None
        short_url = generate_short_url()
        data = read_data()
        data[short_url] = {'url': url, 'name': name}
        write_data(data)
        return redirect('/')
    data = read_data()
    return render_template('index.html', form=form, urls=data)

@app.route('/<short_url>')
def redirect_to_url(short_url):
    data = read_data()
    url_data = data.get(short_url)
    if url_data:
        return redirect(url_data['url'])
    return 'Invalid short URL'

@app.route('/delete/<short_url>', methods=['POST'])
def delete_url(short_url):
    data = read_data()
    if short_url in data:
        del data[short_url]
        write_data(data)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)