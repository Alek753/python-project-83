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


def find_url(id):
    query = """SELECT name FROM urls
                WHERE id = %s;"""
    with db_connect() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (id,))
            name = cur.fetchone()
    conn.commit()
    conn.close()
    return name


def get_url(id):
    query = """SELECT * FROM urls
                WHERE id = %s;"""
    with db_connect() as conn:
        with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
            cur.execute(query, (id,))
            url_info = cur.fetchone()
    conn.commit()
    conn.close()
    return url_info


def get_checked_url(id):
    pass


def get_checked_urls():
    pass
