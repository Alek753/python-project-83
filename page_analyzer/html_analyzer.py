from bs4 import BeautifulSoup


def analyze_page(response):
    page = BeautifulSoup(response.text)
    page_data = {}
    page_data['title'] = page.title
