
import pandas as pd
from sqlalchemy import create_engine



db_config = {
    "user": "postgres",
    "password": "123456A",
    "host": "localhost",
    "port": 5432,
    "dbname": "Naftos_kaina"
}

# Prisijungimas prie duomenų bazės
connection = (f'postgresql://{db_config["user"]}:{db_config["password"]}@{db_config["host"]}:{db_config["port"]}/{db_config["dbname"]}')

engine = create_engine(connection)


# Užklausos

rikiavimas_pagal_data = ("SELECT * FROM kainos ORDER BY date DESC LIMIT 5;")

verte_nuo = ("SELECT * FROM kainos WHERE open>60 LIMIT 5;")

didziausios_kainos = ("SELECT * FROM kainos ORDER BY high DESC LIMIT 5;")

kainos_tarp = ("SELECT * FROM kainos WHERE high >= 100 AND high <= 130 ORDER BY date ASC LIMIT 5;")

maziausios_kainos = ("SELECT * FROM kainos WHERE low BETWEEN 40 AND 60 LIMIT 5;")

rik = pd.read_sql(rikiavimas_pagal_data,  engine)
print(f'Rikiavimas pagal data:{rik}')
vert = pd.read_sql(verte_nuo, engine)
print(f'Naftos kainos nuo 60 :{vert}')
did = pd.read_sql(didziausios_kainos, engine)
print(f'Didziausios naftos kainos: {did}')
tarp = pd.read_sql(kainos_tarp, engine)
print(f'Kainos tarp nurodyto intervalo: {tarp}')
maz = pd.read_sql(maziausios_kainos, engine)
print(f'Maziausios kainos: {maz}')
