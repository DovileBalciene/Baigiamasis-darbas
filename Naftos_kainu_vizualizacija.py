import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder

file_path = 'C:/Users/dovil/PycharmProjects/Baigiamasis_darbas/Oil (WTI)_10_26_20-03_07_22.csv'
df = pd.read_csv(file_path)
# print(df)


# df['Year'] = pd.to_datetime(df['Date']).dt.year
# print(df['Year'])


# plt.figure(figsize=(12, 6))
# plt.plot(df["Year"], df["High"], marker='o', linestyle='-')
# plt.title(" Naftos kainu augimas pagal metu")
# plt.xlabel("Metai")
# plt.ylabel("Kainu augimas")
# plt.grid(True)
# plt.show()




