import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import logging
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder

file_path = 'C:/Users/dovil/PycharmProjects/Baigiamasis_darbas/Oil (WTI)_10_26_20-03_07_22.csv'
df = pd.read_csv(file_path)
# print(df)

# plt.figure(figsize=(12, 6))
# plt.plot(df_region["Date"].iloc[split_index:], y_test_exp, label="Tikros kainos", marker='o')
# plt.plot(df_region["Date"].iloc[split_index:], y_pred, label="Prognozuotos kainos", marker='x')
# plt.title(f"{region_to_plot} kainų prognozės (Random Forest)")
# plt.xlabel("Data")
# plt.ylabel("Kaina")
# plt.legend()
# plt.grid(True)
# # plt.show()

df['Year'] = pd.to_datetime(df['Date']).dt.year
print(df['Year'])

plt.figure(figsize=(12, 6))
plt.plot(df["Year"], df["High"], marker='o', linestyle='-')
plt.title(" Naftos kainu augimas pagal metu")
plt.xlabel("Metai")
plt.ylabel("Kainu augimas")
plt.grid(True)
plt.show()
