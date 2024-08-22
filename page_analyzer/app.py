import os
from flask import Flask, render_template, flash
from dotenv import load_dotenv
import psycopg2


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    return render_template('index.html')


def validate(url):
    return 0


@app.post('/urls')
def add_url():
    url = request.form['url']
    errors = validete(url)
    if errors:
        flash(errors, 'error')
        return render_template('index.html', url=url), 422