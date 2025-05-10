import requests
from bs4 import BeautifulSoup

base_url = 'https://markets.businessinsider.com/commodities/oil-price?type=wti?utm_source=feedly'
# response = requests.get(url)
#
# print(response.status_code)
def fetch_page(url):
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        return response.text
    except requests.exceptions.HTTPError as err:
        print(f'Klaida: {err}')
    return None

def parse_page(html):
    soup = BeautifulSoup(html, 'html.parser')
