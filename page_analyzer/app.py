import os
from flask import Flask, render_template, flash, request, redirect, url_for
from dotenv import load_dotenv
import validators
from urllib.parse import urlparse
import requests
from page_analyzer import db


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
    return None


def normalize(url):
    parsed_url = urlparse(url)
    return f'{parsed_url.scheme}://{parsed_url.netloc}'


@app.post('/urls')
def add_url():
    url = request.form['url']
    errors = validate(url)
    print(errors)
    if errors:
        flash(errors, 'error')
        return render_template('index.html', url=url), 422
    id = db.add_url(normalize(url))
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('url_page', id=id))


@app.get('/urls')
def show_urls_list():
    urls = db.get_checked_urls()
    return render_template('urls_list.html', urls=urls)


@app.route('/urls/<int:id>')
def url_page(id):
    url_info = db.get_url(id)
    print(id)
    checked_url = db.get_checked_url(id)
    return render_template('check_url.html', url=url_info, checks=checked_url)


@app.post('/urls/<id>/checks')
def check_url(id):
    try:
        response = requests.get(db.find_url(id))
        response.raise_for_status()
    except requests.RequestException:
        flash('Произошла ошибка при проверке', 'danger')
    """ some process for url """
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('url_page', id=id))
