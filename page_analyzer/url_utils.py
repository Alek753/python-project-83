import validators
from urllib.parse import urlparse


def validate(url):
    if not url:
        return 'Заполните это поле'
    if not validators.url(url):
        return 'Некорректный URL'
    return None


def normalize(url):
    parsed_url = urlparse(url)
    return f'{parsed_url.scheme}://{parsed_url.netloc}'
