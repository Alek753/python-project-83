import os
from flask import Flask, render_template, flash, request
from dotenv import load_dotenv
import validators


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    return render_template('index.html')


def validate(url):
    if not url:
        return 'Заполните это поле'
    if not validate.url(url):
        return 'Некорректный URL'
    return 0


@app.post('/urls')
def add_url():
    url = request.form['url']
    errors = validate(url)
    if errors:
        flash(errors, 'error')
        return render_template('index.html', url=url), 422
    


@app.post('/urls/<id>/checks')
def check_url(id):
    pass
 