import  sqlite3
import pandas as pd

df = pd.read_csv('Nafta_nuo_2015_01_01_iki_2025_04_30.csv')

df.columns = df.columns.str.strip()
connection = sqlite3.connect("Naftos_kaina.db")
df.to_sql('housing_developments', connection, if_exists='replace')
connection.close()

