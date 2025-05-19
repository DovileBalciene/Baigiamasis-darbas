import csv
import requests
from selenium import webdriver
import psycopg2
import db_config



def gauti_svetaines_turini(url):
    """Nuskaito svetainės turinį"""
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        return response.text
    except requests.exceptions.HTTPError as err:
        print(f'Klaida: {err}')
    return None

#nuskaityti duomenis
def nuskaityti_duomenis(url):
    """Nuskaito duomenis"""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    """ Naudojame „headless“ režimą, kad naršyklė nebūtų rodoma"""
    driver = webdriver.Chrome(options=options)
    """ Funkcija sukuria Chrome naršyklės valdiklį, leidžiantį automatizuoti naršyklės veiksmus"""
    driver.get(url)

    try:
        """ Naudojame Selenium ir JavaScript, kad gautume `window.historicalPrices.configs`"""
        historical_prices = driver.execute_script("return window.historicalPrices.configs;")

        """ Patikriname, ar gauti duomenys"""
        if not historical_prices or not historical_prices[0].get("historicalPrices"):
            print("Nepavyko gauti duomenų iš `window.historicalPrices.configs`.")
            return []

        """ Ištraukiame duomenis iš JSON"""
        model_data = historical_prices[0]["historicalPrices"]["model"]
        return model_data

    except Exception as e:
        print(f"Klaida: {e}")
        return []

    finally:
        driver.quit()


def irasyti_csv(duomenys, failo_pavadinimas):
    """Įrašo nuskaitytus 'Historical Prices for Oil (WTI)' duomenis į csv failą"""

    if not duomenys:
        print("Duomenų įrašymui į CSV nerasta")
        return

    with open(failo_pavadinimas, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["date", "open", "close", "high", "low", "volume"])  # Stulpelių pavadinimai
        for item in duomenys:
            writer.writerow([item.get("Date", ""), item.get("Open", ""), item.get("Close", ""), item.get("High", ""),
                             item.get("Low", ""), item.get("Volume", "")])

    print(f"Duomenys sėkmingai įrašyti į {failo_pavadinimas}")




def issaugoti_duomenu_bazeje(duomenys):
    """Įterpia duomenis į PostgreSQL duomenų bazės lentelę"""

    if not duomenys:
        print("No data available for database insertion.")
        return

    try:
        """Jungiamasi prie duomenų bazės.Prisijungimo duomenys db_config.py"""
        conn = psycopg2.connect(
            database=db_config.DB_NAME,
            user=db_config.DB_USER,
            password=db_config.DB_PASSWORD,
            host=db_config.DB_HOST,
            port=db_config.DB_PORT

        )

        cursor = conn.cursor()

        """Įterpiame duomenis į duomenų bazės lentelę"""
        for elementas in duomenys:
            """ get() naudojama: jei nėra rakto datai grąžinama tuščia reikšmė, skaičiams 0"""
            cursor.execute("""
                           INSERT INTO kainos_naftos (date, open, close, high, low, volume)
                           VALUES (%s, %s, %s, %s, %s, %s)
                           """, (elementas.get("Date", ""), elementas.get("Open", 0), elementas.get("Close", 0),
                                 elementas.get("High", 0),
                                 elementas.get("Low", 0), elementas.get("Volume", 0)))

        conn.commit()  # Išsaugoti
        print(f"Duomenys įrašyti į duomenų bazę `{db_config.DB_NAME}`")


    except psycopg2.OperationalError as e:
        print(f'Klaida: neprisijungta prie duomenų bazės : {e}')

    except psycopg2.Error as e:
        print(f'Klaida: duomenys į duomenų bazę neįrašyti  {e}')

    finally:
        if conn:
            conn.close()


def main():
    url = "https://markets.businessinsider.com/commodities/oil-price?type=wti?utm_source=feedly"
    puslapis = gauti_svetaines_turini(url)

    if puslapis is None:
        return

    failo_pavadinimas = "Naftos_kainų_duomenys.csv"
    duomenys = nuskaityti_duomenis(url)

    irasyti_csv(duomenys, failo_pavadinimas)
    issaugoti_duomenu_bazeje(duomenys)


if __name__ == '__main__':
    main()
