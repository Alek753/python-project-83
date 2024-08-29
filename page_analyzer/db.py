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
    print(list(url_data.values()))
    query = """INSERT INTO url_checks
                (url_id, status_code, h1, title, description)
                VALUES (%s, %s, %s, %s, %s);"""
    with db_connect() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(query, list(url_data.values()))
            except Exception as error:
                print(error, '/n', type(error))
    conn.commit()
    conn.close()


def get_url(attr):
    if isinstance(attr, str):
        search_for = 'name'
    else:
        search_for = 'id'
    query = f"""SELECT * FROM urls
                WHERE {search_for} = %s;"""
    with db_connect() as conn:
        with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
            cur.execute(query, (attr,))
            url_data = cur.fetchone()
    conn.commit()
    conn.close()
    return url_data


def get_url_checks(id):
    query = """SELECT * FROM url_checks
                WHERE url_id = %s;"""
    with db_connect() as conn:
        with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
            cur.execute(query, (id,))
            check_data = cur.fetchall()
    conn.commit()
    conn.close()
    return check_data


def get_checked_urls():
    query = """SELECT name,
                        urls.id AS id,
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
