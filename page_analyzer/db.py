import os
from psycopg2 import connect, extras
from dotenv import load_dotenv


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def set_connection(factory):
    def wrapper(func):
        def inner(*args):
            with connect(DATABASE_URL) as conn:
                with conn.cursor(cursor_factory=factory) as cur:
                    res = func(cur, *args)
            conn.commit()
            conn.close()
            return res
        return inner
    return wrapper


@set_connection(extras.DictCursor)
def add_url(cur, url):
    query = """INSERT INTO urls (name)
                VALUES (%s)
                RETURNING id;"""
    cur.execute(query, (url,))
    id = cur.fetchone()[0]
    return id


@set_connection(extras.DictCursor)
def add_checked_url(cur, url_data):
    query = """INSERT INTO url_checks
                (url_id, status_code, h1, title, description)
                VALUES (%s, %s, %s, %s, %s);"""
    cur.execute(query, list(url_data.values()))


@set_connection(extras.RealDictCursor)
def get_url_by_name(cur, name):
    query = """SELECT * FROM urls
                WHERE name = %s;"""
    cur.execute(query, (name,))
    url_data = cur.fetchone()
    return url_data


@set_connection(extras.RealDictCursor)
def get_url_by_id(cur, id):
    query = """SELECT * FROM urls
                WHERE id = %s;"""
    cur.execute(query, (id,))
    url_data = cur.fetchone()
    return url_data


@set_connection(extras.RealDictCursor)
def get_url_checks(cur, id):
    query = """SELECT * FROM url_checks
                WHERE url_id = %s
                ORDER BY id DESC;"""
    cur.execute(query, (id,))
    check_data = cur.fetchall()
    return check_data


@set_connection(extras.RealDictCursor)
def get_checked_urls(cur):
    query = """SELECT DISTINCT ON (urls.id)
                        urls.id AS id,
                        name,
                        name,
                        status_code,
                        url_checks.created_at
                FROM urls
                LEFT JOIN url_checks ON
                    urls.id = url_checks.url_id
                ORDER BY id DESC"""
    cur.execute(query)
    checked_urls = cur.fetchall()
    return checked_urls
