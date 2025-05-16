import csv
import json
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

# Laukiame, kol puslapis pilnai užsikraus ir `historicalPrices` objektas bus prieinamas
WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.ID, "historicPrices"))
)

time.sleep(5)  # Papildomas laukimas, jei duomenys kraunami lėtai

try:
    # Naudojame JavaScript, kad gautume istorinius duomenis
    script = """
    return window.historicalPrices && window.historicalPrices.configs 
           ? window.historicalPrices.configs.find(c => c.regionSelector === '#historicPrices').historicalPrices.model
           : null;
    """
    data = driver.execute_script(script)

    if not data:
        print("Nepavyko rasti istorinių duomenų! Patikrink puslapio struktūrą.")
    else:
        print("\n įrašome duomenis į CSV failą 'oil_prices_filtered.csv'")

        # Filtruojame datas nuo 2015-01-01 iki 2025-04-30
        start_date = datetime.datetime(2015, 1, 1)
        end_date = datetime.datetime(2025, 5, 15)

        filtered_data = []
        for row in data:
            try:
                row_date = datetime.datetime.strptime(row["Date"], "%m/%d/%y")
                if row_date >= start_date and row_date <= end_date:
                    filtered_data.append(row)
            except ValueError:
                continue  # Jei datos formatas netinkamas, praleidžiame eilutę

        # Įrašome filtruotus duomenis į CSV failą
        with open("oil_prices_filtered.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Open", "Close", "High", "Low"])  # Antraštės

            for row in filtered_data:
                writer.writerow([row["Date"], row["Open"], row["Close"], row["High"], row["Low"]])

        print("Duomenys įrašyti i 'oil_prices_filtered.csv'!")

finally:
    driver.quit()  # Uždaro naršyklę po vykdymo
