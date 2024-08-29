from bs4 import BeautifulSoup


def analyze_page(response):
    page = BeautifulSoup(response.text, 'html.parser')
    h1 = page.h1.string if page.h1 else ''
    title = page.title.string if page.title else ''
    description = page.find('meta', {'name': 'description'})
    return {'status_code': response.status_code,
            'h1': h1,
            'title': title,
            'decription': description.get('content')[:255] if description else ''}
