from bs4 import BeautifulSoup


def analyze_page(status_code, body):
    page = BeautifulSoup(body, 'html.parser')
    h1 = page.find('h1')
    title = page.find('title')
    description = page.find('meta', {'name': 'description'})
    return {'status_code': status_code,
            'h1': h1.text if h1 else '',
            'title': title.text if title else '',
            'description': description.get('content') if description else ''}
