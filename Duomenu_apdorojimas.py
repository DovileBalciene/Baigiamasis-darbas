import pandas as pd

file_path = 'C:/Users/dovil/PycharmProjects/Baigiamasis_darbas/Nafta_nuo_2015_01_01_iki_2025_04_30.csv'
df = pd.read_csv(file_path)


""" Sutvarkome datos formata"""
df['Date'] = pd.to_datetime(df['Date'], format='mixed')

""" Atliekamas duomenų apdorojimas (Pandas) """

vidutine_kaina_nuo_pradines_reiksmes = df["Open"].mean().round(2)
print(f'Vidutine kaina {vidutine_kaina_nuo_pradines_reiksmes}')

auksciausia_kaina_pagal_data = df.groupby(['High']).max().head(5)
print(f'Aukščiausia kaina {auksciausia_kaina_pagal_data}')


maziausia_kaina = df.groupby('Date')['Low'].min().head(10)
print(maziausia_kaina)

df['kainu_skirtumas_nuo_pradines'] = df['Close'] - df['Open']
print(df['kainu_skirtumas_nuo_pradines'])

procentinis_pasiskirstymas = df.groupby('Open')['kainu_skirtumas_nuo_pradines'].apply(lambda x: x / 100).head(5)
print(procentinis_pasiskirstymas)

def karegorija(kaina):
    if kaina > 100:
        return 'Per didele'
    elif kaina < 70:
        return 'Zema kaina'
    else:
        return 'Vidutine'

df['kategorija'] = df['Close'].apply(karegorija)
print(df['kategorija'].value_counts())
print(df[['Close', 'Date', 'kategorija']])