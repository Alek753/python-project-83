import os
from psycopg2 import connect, extras
from dotenv import load_dotenv


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def db_connect():
    return connect(DATABASE_URL)


def add_url(url):
    query = """INSERT INTO urls (name)
                VALUES (%s)
                RETURNING id;"""
    with db_connect() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (url,))
            id = cur.fetchone()[0]
    conn.commit()
    conn.close()
    return id


def add_checked_url(url_data):
    query = """INSERT INTO url_checks
                (url_id, status_code, h1, title, description)
                VALUES (%s, %s, %s, %s, %s);"""
    with db_connect() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(query, list(url_data.values()))
            except Exception as error:
                print(error, '\n', type(error))
    conn.commit()
    conn.close()


def exec_get_url(query, attr):
    with db_connect() as conn:
        with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
            cur.execute(query, (attr,))
            url_data = cur.fetchone()
    conn.commit()
    conn.close()
    return url_data


def get_url_by_name(name):
    query = """SELECT * FROM urls
                WHERE name = %s;"""
    return exec_get_url(query, name)


def get_url_by_id(id):
    query = """SELECT * FROM urls
                WHERE id = %s;"""
    return exec_get_url(query, id)


def get_url_checks(id):
    query = """SELECT * FROM url_checks
                WHERE url_id = %s
                ORDER BY id DESC;"""
    with db_connect() as conn:
        with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
            cur.execute(query, (id,))
            check_data = cur.fetchall()
    conn.commit()
    conn.close()
    return check_data


def get_checked_urls():
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
    with db_connect() as conn:
        with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
            cur.execute(query)
            checked_urls = cur.fetchall()
    conn.commit()
    conn.close()
    return checked_urls
