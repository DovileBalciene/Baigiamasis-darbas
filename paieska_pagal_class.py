import csv
import requests
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import psycopg2




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


def gauti_lenteles_eilutes(url, driver=None):
    driver = webdriver.Chrome()
    driver.get(url)

    try:
        
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'April. 15 2025')]")))
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'May. 15 ')]")))

        # paspaudziam mygtukus
        driver.find_element(By.XPATH, "//buton[contains(text(), 'April. 15 2025')]").click()
        driver.find_element(By.XPATH, "//buton[contains(text(), 'May. 15 2025')]").click()

        #laukiam kol bus ikelta lentele
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "table--sortable")))

        #randam lentele pagal ID
        lenteles_elementas = driver.find_element(By.CLASS_NAME, "table--sortable")
        #naudojame slinkimui
        actions = ActionChains(driver)
        actions.move_to_element(lenteles_elementas).perform() #slinkti iki lenteles pabaigos





        #laukiam kol lentele pasirodys
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "table--sortable")))



        eilutes = lenteles_elementas.find_elements(By.TAG_NAME, 'tr')

        duomenys = []
        for eilute in lenteles_elementas:
            stulpeliai = eilute.find_elements(By.TAG_NAME, 'td')
            duomenys.append(stulpelis.text.strip() for stulpelis in stulpeliai)

        print("Duomenys nuskaityti sėkmingai")
        return duomenys #graziname duomenis kaip sarasa
    except Exception as e:
        print(f'Puslapis nenuskaitomas: {e}')
        return []
        driver.quit()

def irasyti_i_csv(pavadinimas, duomenys):
   try:
       with open('pavadinimas', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(duomenys)
       print(f"Duomenys įrašyti į csv: {pavadinimas}")

   except Exception as e:
       print(f"Duomenys neįrašyti į csv: {e}")

def issaugoti_duomenu_bazeje(duomenys, db_config):
    try:
        with psycopg2.connect(**db_config) as conn:
            with conn.cursor() as cursor:

                cursor.executemany("""INSERT INTO kainos_naftos (open, close, high, low, volume, date)
                                      VALUES (%s, %s, %s, %s, %s, %s)
                                      ON CONFLICT (date) DO NOTHING

                                   """, duomenys)
            conn.commit()

        print("Duomenys įrašyti į duomenų bazę")
    except psycopg2.OperationalError as e:
        print(f'Klaida: neprisijungta prie duomenų bazės : {e}')

    except psycopg2.Error as e:
        print(f'Klaida: duomenys į duomenų bazę neįrašyti  {e}')



def main():
    url = 'https://markets.businessinsider.com/commodities/oil-price?type=wti?utm_source=feedly'

    page = fetch_page(url)
    csv_failo_pavadinimas = 'Nafta_nuo_2015_01_iki_2025_04'
    duomenys = gauti_lenteles_eilutes(url)
    if duomenys:
            for eilute in duomenys:
                print(eilute)
    else:
        print("duomenys negauti")


        irasyti_i_csv(csv_failo_pavadinimas, duomenys)
        issaugoti_duomenu_bazeje(duomenys, db_config)


if __name__ == '__main__':
    main()
