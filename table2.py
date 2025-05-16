import csv
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

URL = "https://markets.businessinsider.com/commodities/oil-price?type=wti?utm_source=feedly"

# Paleidžiame naršyklę
driver = webdriver.Chrome()
driver.get(URL)

time.sleep(5)  # Palaukiame, kol puslapis pilnai užsikraus

try:
    # Laukiame, kol lentelė bus pasiekiama
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//table[contains(@class, 'table--fixed table--sortable')]"))
    )

    # Randame lentelę
    table = driver.find_element(By.XPATH, "//table[contains(@class, 'table--fixed table--sortable')]")
    rows = table.find_elements(By.TAG_NAME, "tr")

    print("\n🔹 Įrašome duomenis į CSV failą 'oil_prices_filtered.csv'")

    # Sukuriame CSV failą
    with open("oil_prices_filtered.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Open", "Close", "High", "Low"])  # Antraštės

        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            data = [col.text.strip() for col in cols]

            if len(data) == 5:  # Patikriname, ar yra visi stulpeliai
                try:
                    row_date = datetime.datetime.strptime(data[0], "%m/%d/%y")
                    start_date = datetime.datetime(2015, 1, 1)
                    end_date = datetime.datetime(2025, 4, 30)

                    if start_date <= row_date <= end_date:
                        writer.writerow(data)  # Įrašome į CSV
                except ValueError:
                    continue  # Jei datos formatas netinkamas, praleidžiame eilutę

        print("✅ Duomenys nuo 2015-01-01 iki 2025-04-30 sėkmingai įrašyti į 'oil_prices_filtered.csv'!")

finally:
    driver.quit()  # Uždaro naršyklę po vykdymo
