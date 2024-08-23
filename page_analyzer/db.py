import os
from psycopg2 import connect
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
            id = cur.fetchone()
    conn.commit()
    conn.close()
    return id


def find_url(url):
    query = """SELECT name FROM urls
                WHERE name = %s;"""
    with db_connect() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (url,))
            name = cur.fetchone()
    conn.commit()
    conn.close()
    return name
