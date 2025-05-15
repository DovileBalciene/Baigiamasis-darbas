import csv
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sqlalchemy.dialects.postgresql import psycopg2

db_config = {
    "dbname": "Naftos_kaina",
    "user": "postgres",
    "password": "123456A",
    "host": "localhost",
    "port": 5432
}


def fetch_page(url):
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        return response.text
    except requests.exceptions.HTTPError as err:
        print(f'Klaida: {err}')
    return None


def setup_driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    return driver


def gauti_lenteles_eilutes(dreiver, selector):
    table = WebDriverWait(dreiver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
    return table.find_elements(By.TAG_NAME, 'tr')

    naftos_kainos = []
    for row in table_rows:
        columns = row.find_elements(By.TAG_NAME, 'td')
        row_data = [column.text.strip() for column in columns]
        naftos_kainos.append(row_data)


def issaugoti_duomenu_bazeje(duomenys, db_config):
    try:
        with psycopg2.connect(**db_config) as conn:
            with conn.cursor() as cursor:

                cursor.executemany("""INSERT INTO kainos_naftos (open, close, high, low, volume, date)
                                      VALUES (%s, %s, %s, %s, %s, %s)
                                      ON CONFLICT (date) DO NOTHING

                                   """, duomenys)
            conn.commit()
        conn.close()

        print("Duomenys įrašyti į duomenų bazę")
    except:
        print("Klaida, įrašant duomenis į duomenų bazę")

        cursor.close()
        conn.close()


def main():
    url = 'https://markets.businessinsider.com/commodities/oil-price?type=wti?utm_source=feedly'

    page = fetch_page(url)
    if page:
        selector = 'table tr'
        driver = setup_driver()
        driver.get(url)
        table_rows = gauti_lenteles_eilutes(driver, selector)
        driver.quit()

        with open('Nafta_nuo_2015_01_iki_2025_04.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(table_rows)
            print(f"Duomenys įrašyti į csv: {csvfile.name}")

        issaugoti_duomenu_bazeje(table_rows, db_config)
#print

if __name__ == '__main__':
    main()
