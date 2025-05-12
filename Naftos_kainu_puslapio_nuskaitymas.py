import psycopg2
import requests
from bs4 import BeautifulSoup
from psycopg2.extras import execute_values
from selenium import webdriver
from selenium.common import ElementNotInteractableException, TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time


options = webdriver.ChromeOptions()
# options.add_argument('--headless')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install(), options=options))
wait = WebDriverWait(driver, 10)
driver.maximize_window()
driver.get("https://markets.businessinsider.com/commodities/oil-price?type=wti?utm_source=feedly")

base_url = 'https://markets.businessinsider.com'
# lenteliu_info = driver.find_elements(By.CSS_SELECTOR,'table table--fixed table--sortable table--scrollable table--suppresses-line-breaks' )

naftos_kainos_duomenys = []

while True:
    lenteliu_info= driver.find_elements(By.ID,'e92c0d0cb_88f1_48bc_963f_7ab2ef99deac' )
    for nafta in lenteliu_info:
        duomenys = nafta.get_attribute("table")
        if duomenys not in lenteliu_info:
            naftos_kainos_duomenys.append(duomenys)
    try:
        for i in range(5):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});")
        time.sleep(1)
    except(TimeoutException, ElementNotInteractableException):
        print(" No more loads or can't click")
        break

# print(f'Found {len(lenteliu_info)} nafta.')
# with open('naftos_duomenys.txt', 'w') as file:
#     for link in lenteliu_info:
#         file.write(link + "\n")
# driver.quit()

















# response = requests.get(url)
#
# response = requests.get(base_url)
# print(response.status_code)

# db_config = {
#     "dbname": "naftos_kaina",
#     "user": "postgres",
#     "password": "123456A",
#     "host": "localhost",
#     "port": 5432
# }

# def fetch_page(url):
#     try:
#         response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
#         response.raise_for_status()
#         return response.text
#     except requests.exceptions.HTTPError as err:
#         print(f'Klaida: {err}')
#     return None
#
# def parse_page(html):
#     soup = BeautifulSoup(html, 'html.parser')
# def parse_page(page):
#     soup = BeautifulSoup(page, 'html.parser')
#     nafta_data_info = soup.find_all('table',
#                                     class_='table table--fixed table--sortable')
#     print(nafta_data_info)
#
#     stulpeliu_duomenys = soup.find_all('tr')
#
#     naftos_kainos_duomenys = []
#     for row in stulpeliu_duomenys:  # pradeda nuo 1 nebutu tuscio []
#         row_data = row.find_all('td')
#         naftos_kainos = [data.text.strip() for data in row_data]
#         print(naftos_kainos)
#         naftos_kainos_duomenys.append(naftos_kainos)
#     return naftos_kainos_duomenys
#     naftos_kainos_duomenys.to_csv(r'C:\Users\Vartotojas\PycharmProjects\Baigiamasis-darbas')
#
# # def save_to_db(rows):
# #     if not rows:
# #         print('Saugojimas negalimas')
# #         return
# #     try:
# #         with psycopg2.connect(**db_config) as conn:
# #             with conn.cursor() as cursor:
# #                 sql = """
# #                     INSERT INTO naftos_kainos(data, kaina_pradzioje, kaina_pabaigoje, min_kaina, max_kaina)
# #                     VALUES %s;
# #                 """
# #                 execute_values(cursor, sql, rows)
# #                 print(f'Data saved: {len(rows)}')
# #     except psycopg2.Error as e:
# #         print(f'Error while connecting to PostgreSQL: {e}')
#
# def main():
#     gauti_naftos_duomenys = []
#
#     for duomenys in parse_page(fetch_page(base_url)):
#         url = base_url.format(duomenys)
#         page = fetch_page(url)
#         if page:
#             naftos_kainos_duomenys = parse_page(page)
#             if naftos_kainos_duomenys:
#                 gauti_naftos_duomenys.extend(naftos_kainos_duomenys)
#             else:
#                 print(f'Klaida: nepasiekiami duomenys')
#         else:
#             print(f'Klaida: puslapis nenuskaitomas')
#     # if (gauti_naftos_duomenys):
#     #     save_to_db(gauti_naftos_duomenys)
#
# if __name__ == '__main__':
#     main()
