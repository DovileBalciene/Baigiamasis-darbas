import psycopg2
import requests
from bs4 import BeautifulSoup
from psycopg2.extras import execute_values

base_url = 'https://markets.businessinsider.com/commodities/oil-price?type=wti?utm_source=feedly'
# response = requests.get(base_url)
# print(response.status_code)

db_config = {
    "dbname": "naftos_kaina",
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

def parse_page(page):
    soup = BeautifulSoup(page, 'html.parser')
    nafta_data_info = soup.find_all('table',
                                    class_='table table--fixed table--sortable')
    print(nafta_data_info)

    stulpeliu_duomenys = soup.find_all('tr')

    naftos_kainos_duomenys = []
    for row in stulpeliu_duomenys:  # pradeda nuo 1 nebutu tuscio []
        row_data = row.find_all('td')
        naftos_kainos = [data.text.strip() for data in row_data]
        print(naftos_kainos)
        naftos_kainos_duomenys.append(naftos_kainos)
    return naftos_kainos_duomenys
    naftos_kainos_duomenys.to_csv(r'C:\Users\Vartotojas\PycharmProjects\Baigiamasis-darbas')

def save_to_db(rows):
    if not rows:
        print('Saugojimas negalimas')
        return
    try:
        with psycopg2.connect(**db_config) as conn:
            with conn.cursor() as cursor:
                sql = """
                    INSERT INTO naftos_kainos(data, kaina_pradzioje, kaina_pabaigoje, min_kaina, max_kaina)
                    VALUES %s;
                """
                execute_values(cursor, sql, rows)
                print(f'Data saved: {len(rows)}')
    except psycopg2.Error as e:
        print(f'Error while connecting to PostgreSQL: {e}')

def main():
    gauti_naftos_duomenys = []

    for duomenys in parse_page(fetch_page(base_url)):
        url = base_url.format(duomenys)
        page = fetch_page(url)
        if page:
            naftos_kainos_duomenys = parse_page(page)
            if naftos_kainos_duomenys:
                gauti_naftos_duomenys.extend(naftos_kainos_duomenys)
            else:
                print(f'Klaida: nepasiekiami duomenys')
        else:
            print(f'Klaida: puslapis nenuskaitomas')
    if (gauti_naftos_duomenys):
        save_to_db(gauti_naftos_duomenys)

if __name__ == '__main__':
    main()






