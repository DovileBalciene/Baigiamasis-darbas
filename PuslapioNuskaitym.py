import csv
import time
import json
import csv
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import psycopg2
from psycopg2 import OperationalError
import db_config  #duomenų nuskaitymas iš failo



def fetch_page(url):
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        return response.text
    except requests.exceptions.HTTPError as err:
        print(f'Klaida: {err}')
    return None


# def gauti_lenteles_eilutes(url):
#     """Naudoja Selenium ir JavaScript, kad nuskaitytų 'Historical Prices for Oil (WTI)' duomenis."""
#
#     options = webdriver.ChromeOptions()
#     options.add_argument("--headless")  # Naudojame „headless“ režimą, kad naršyklė nebūtų rodoma
#     driver = webdriver.Chrome(options=options)
#     driver.get(url)
#
#     try:
#         # Naudojame JavaScript, kad gautume `window.historicalPrices.configs`
#         historical_prices = driver.execute_script("return window.historicalPrices.configs;")
#
#         # Patikriname, ar gauti duomenys
#         if not historical_prices or not historical_prices[0].get("historicalPrices"):
#             print("Nepavyko gauti duomenų iš `window.historicalPrices.configs`.")
#             return []
#
#         # Ištraukiame duomenis iš JSON
#         model_data = historical_prices[0]["historicalPrices"]["model"]
#         return model_data
#
#     except Exception as e:
#         print(f"Klaida: {e}")
#         return []
#
#     finally:
#         driver.quit()  # Uždarome naršyklę
#
# def irasyti_csv(duomenys, failo_pavadinimas):
#     """Įrašo nuskaitytus 'Historical Prices for Oil (WTI)' duomenis į CSV."""
#
#     if not duomenys:
#         print("Nėra duomenų įrašymui į CSV.")
#         return
#
#     with open(failo_pavadinimas, "w", newline="", encoding="utf-8") as csvfile:
#         writer = csv.writer(csvfile)
#         writer.writerow(["Date", "Open", "Close", "High", "Low"])  # Stulpelių pavadinimai
#         for item in duomenys:
#             writer.writerow([item.get("Date", ""), item.get("Open", ""), item.get("Close", ""), item.get("High", ""),
#                              item.get("Low", "")])
#
#     print(f"Duomenys sėkmingai įrašyti į {failo_pavadinimas}")
#
#
#
#
#
# def irasyti_i_csv(pavadinimas, duomenys):
#    try:
#        with open('pavadinimas', 'w', newline='', encoding='utf-8') as f:
#             writer = csv.writer(f)
#             writer.writerows(duomenys)
#        print(f"Duomenys įrašyti į csv: {pavadinimas}")
#
#    except Exception as e:
#        print(f"Duomenys neįrašyti į csv: {e}")
#

 # Import database configuration from db_config.py
def nuskaityti_duomenis(url):
    """Naudoja Selenium ir JavaScript, kad nuskaitytų 'Historical Prices for Oil (WTI)' duomenis."""

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Naudojame „headless“ režimą, kad naršyklė nebūtų rodoma
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    try:
        # Naudojame JavaScript, kad gautume `window.historicalPrices.configs`
        historical_prices = driver.execute_script("return window.historicalPrices.configs;")

        # Patikriname, ar gauti duomenys
        if not historical_prices or not historical_prices[0].get("historicalPrices"):
            print("Nepavyko gauti duomenų iš `window.historicalPrices.configs`.")
            return []

        # Ištraukiame duomenis iš JSON
        model_data = historical_prices[0]["historicalPrices"]["model"]
        return model_data

    except Exception as e:
        print(f"Klaida: {e}")
        return []

    finally:
        driver.quit()  # Uždarome naršyklę


def irasyti_csv(duomenys, failo_pavadinimas):
    """Įrašo nuskaitytus 'Historical Prices for Oil (WTI)' duomenis į CSV."""

    if not duomenys:
        print("Nėra duomenų įrašymui į CSV.")
        return

    with open(failo_pavadinimas, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["date", "open", "close", "high", "low", "volume"])  # Stulpelių pavadinimai
        for item in duomenys:
            writer.writerow([item.get("Date", ""), item.get("Open", ""), item.get("Close", ""), item.get("High", ""),
                             item.get("Low", ""), item.get("Volume", "")])

    print(f"Duomenys sėkmingai įrašyti į {failo_pavadinimas}")




def issaugoti_duomenu_bazeje(duomenys):
    """Inserts 'Historical Prices for Oil (WTI)' data into the existing PostgreSQL table 'kainos_naftos'."""

    if not duomenys:
        print("No data available for database insertion.")
        return

    try:
        # Connect to PostgreSQL database
        conn = psycopg2.connect(
            database=db_config.DB_NAME,
            user=db_config.DB_USER,
            password=db_config.DB_PASSWORD,
            host=db_config.DB_HOST,
            port=db_config.DB_PORT

        )

        cursor = conn.cursor()

        # Insert data into the existing table, avoiding duplicates
        for item in duomenys:
            cursor.execute("""
                           INSERT INTO kainos_naftos (date, open, close, high, low, volume)
                           VALUES (%s, %s, %s, %s, %s, %s)
                           """, (item.get("Date", ""), item.get("Open", 0), item.get("Close", 0), item.get("High", 0),
                                 item.get("Low", 0), item.get("Volume", 0)))

        conn.commit()  # Save changes
        print(f"Duomenys įrašyti į duomenų bazę `{db_config.DB_NAME}`")

    except psycopg2.Error as e:
        print(f"PostgreSQL error: {e}")

    finally:
        if conn:
            conn.close()  # Close connection






def main():
    url = "https://markets.businessinsider.com/commodities/oil-price?type=wti?utm_source=feedly"
    page = fetch_page(url)#pataisyti tikrinima


    failo_pavadinimas = "Naftos_kainų_duomenys.csv"

    duomenys = nuskaityti_duomenis(url)
    irasyti_csv(duomenys, failo_pavadinimas)

    issaugoti_duomenu_bazeje(duomenys)


if __name__ == '__main__':
    main()
