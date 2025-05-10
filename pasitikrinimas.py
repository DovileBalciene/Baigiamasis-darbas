import requests
from bs4 import BeautifulSoup
import pandas as pd


base_url = 'https://markets.businessinsider.com/commodities/oil-price?type=wti?utm_source=feedly'
response = requests.get(base_url)

# print(response.status_code)

soup = BeautifulSoup(response.text, 'html.parser')

naftos_info = soup.find_all('table')
antrastes = soup.find_all('th') # ieskom stulpeliu antrasciu
lenteles_antrastes = [title.text.strip()for title in antrastes]

print(naftos_info)