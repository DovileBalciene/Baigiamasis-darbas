import psycopg2
from psycopg2 import sql

# Apsibreziam savo duomenis/konfiguracija
PG_USER = 'postgres'
PG_PASSWORD = '369963369'
PG_HOST = 'localhost'
PG_PORT = 5432

# Nusakome duomenu bazes pavadinima, stulpelius ir sukuriam pacia lentele
DB_NAME = 'naftos_kaina'
TABLE_SQL = """
    CREATE TABLE IF NOT EXISTS naftos_kainos(
        id SERIAL PRIMARY KEY,
        data DATE NOT NULL,
        kaina_pradzioje decimal NOT NULL,
        kaina_pabaigoje decimal NOT NULL,
        min_kaina decimal NOT NULL,
        max_kaina decimal NOT NULL 
    );
"""

# Prijungia prie DEFAULT duomenu bazes
conn = psycopg2.connect(
    dbname='postgres',
    user=PG_USER,
    password=PG_PASSWORD,
    host=PG_HOST,
    port=PG_PORT,
)
# Nustato automatini patvirtinima
conn.autocommit = True
cursor = conn.cursor()
cursor.execute(
    "SELECT 1 FROM pg_database WHERE datname = %s;", (DB_NAME,)
)
# Tikrina ar musu duomenu baze egzistuoja
if not cursor.fetchone(): # fetchone() grazina tik viena irasa
    cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME)))
    print(f"Sukurta duomenu baze `{DB_NAME}`")
else:
    print(f"Duomenu baze `{DB_NAME}` yra sukurta")

# Uzdarome duomenu bazes rysi
cursor.close()
conn.close()

# Kuria lentele
def create_table():
    try:
        with psycopg2.connect(
            dbname=DB_NAME,
            user=PG_USER,
            password=PG_PASSWORD,
            host=PG_HOST,
            port=PG_PORT
        ) as conn:
            with conn.cursor() as cursor:
                cursor.execute(TABLE_SQL)
                conn.commit()
                print("Table created")
    except psycopg2.Error as e:
        print(f"Database error: {e}")

if __name__ == "__main__":
    create_table()
