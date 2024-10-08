import os
import requests
from flask import Flask, render_template, flash, request, redirect, url_for
from dotenv import load_dotenv
from page_analyzer import db
from page_analyzer import html_analyzer
from page_analyzer import url_utils


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    return render_template('index.html')


@app.post('/urls')
def add_url():
    url = request.form['url']
    errors = url_utils.validate(url)
    if errors:
        flash(errors, 'error')
        return render_template('index.html', url=url), 422
    norm_url = url_utils.normalize(url)
    url_data = db.get_url_by_name(norm_url)
    if url_data:
        flash('Страница уже существует', 'warning')
        id = url_data['id']
    else:
        id = db.add_url(norm_url)
        flash('Страница успешно добавлена', 'success')
    return redirect(url_for('show_url_page', id=id))


@app.get('/urls')
def show_urls_list():
    urls = db.get_checked_urls()
    return render_template('urls_list.html', urls=urls)


@app.route('/urls/<int:id>')
def show_url_page(id):
    url_info = db.get_url_by_id(id)
    url_checks = db.get_url_checks(id)
    return render_template('check_url.html', url=url_info, checks=url_checks)


@app.post('/urls/<int:id>/checks')
def check_url(id):
    url = db.get_url_by_id(id)
    try:
        response = requests.get(url['name'])
        response.raise_for_status()
    except requests.RequestException:
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('show_url_page', id=id))
    else:
        html_data = {'url_id': id}
        html_data.update(html_analyzer.analyze_page(response.status_code, response.text))
        db.add_checked_url(html_data)
        flash('Страница успешно проверена', 'success')
        return redirect(url_for('show_url_page', id=id))
