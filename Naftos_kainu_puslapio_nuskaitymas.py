import csv

import pandas as pd
import psycopg2
import requests
from bs4 import BeautifulSoup
from psycopg2.extras import execute_values
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from sqlalchemy import create_engine
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 20)  # Suteikia laukimo laika (10 sec) kol ivykdys nurodyta salyga
driver.maximize_window()  # Atidarys pilnai langa

driver.get("https://markets.businessinsider.com/commodities/oil-price?type=wti?utm_source=feedly")

url = "https://markets.businessinsider.com/commodities/oil-price?type=wti?utm_source=feedly"

db_config = {
    "user": "postgres",
    "password": "123145A",
    "host": "localhost",
    "port": 5432,
    "dbname": "Naftos_kaina"
}


def fetch_page(url):
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as err:
        print(f'Klaida kraunant puslapį {url}: {err}')
        return None


def parse_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    table_body = driver.find_element(By.CSS_SELECTOR, "tbody")
    table_rows = table_body.find_elements(By.TAG_NAME, "tr")

    with open("movie_data.csv", "w", newline="") as file:
        writer = csv.writer(file)
    for row in table_rows:
        table_data = row.find_elements(By.TAG_NAME, "td")

    row_data = []
    for data in table_data:
        row_data.append(data.text)
    print(row_data)
    if not row_data:
        print("Duomenų nerasta")

    return row_data


def save_page(rows):
    if not rows:
        print("Duomenų nerasta")
        return

    try:
        with psycopg2.connect(**db_config) as conn:
            with conn.cursor() as cur:
                sql = """
                      INSERT INTO kainos (open, close, high, low, volume, date) \
                      VALUES (%s, %s, %s, %s, %s, %s)

                      ON CONFLICT (open, close, high, low, volume, date) DO NOTHING; \
                      """
                # siekiama isvengti klaidu
                execute_values(cur, sql, rows)
                print(f"Successfully inserted {len(rows)} rows into the database.")
    except psycopg2.Error as e:
        print(f"Database error: {e}")


def main():
    all_data = []

    page = fetch_page(url)
    if page:
        naftos_kainos_duomenys = parse_page(page)
        if naftos_kainos_duomenys:
            all_data.extend(naftos_kainos_duomenys)
        else:
            print(f"Duomenų iš puslapio gauti nepavyko")

        if all_data:
            save_page(all_data)


if __name__ == '__main__':
    main()