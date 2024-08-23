import os
from flask import Flask, render_template, flash, request, redirect, url_for
from dotenv import load_dotenv
import validators
from urllib.parse import urlparse


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    return render_template('index.html')


def validate(url):
    if not url:
        return 'Заполните это поле'
    if not validators.url(url):
        return 'Некорректный URL'
    return 0


def normalize(url):
    parsed_url = urlparse(url)
    return f'{parsed_url.scheme}://{parsed_url.netloc}'


@app.post('/urls')
def add_url():
    url = request.form['url']
    errors = validate(url)
    if errors:
        flash(errors, 'error')
        return render_template('index.html', url=url), 422
    id = add_url(normalize(url))
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('url_page', id=id))


@app.route('/urls/<id>')
def url_page(id):
    pass


@app.post('/urls/<id>/checks')
def check_url(id):
    pass
