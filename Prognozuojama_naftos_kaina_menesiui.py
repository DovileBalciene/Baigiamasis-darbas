import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

#Šis kodas naudoja paprastą linijinę regresiją

df = pd.read_csv("C:/Users/dovil/PycharmProjects/Baigiamasis_darbas/Nafta_nuo_2015_01_01_iki_2025_04_30.csv")

# Konvertuojame datą į datetime formatą ir nustatome kaip indeksą
df["Date"] = pd.to_datetime(df["Date"])
df.set_index("Date", inplace=True)

# Skaičiuojame dienų skaičių nuo pirmos eilutės indekso
df["Days"] = (df.index - df.index[0]).days

# Pasirenkame požymius ir tikslinį kintamąjį
X = df[["Days"]]
y = df["High"]

# Padalijame duomenis į mokymo ir testavimo rinkinius
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=False)

# Sukuriame regresijos modelį
model = LinearRegression()
model.fit(X_train, y_train)

# Prognozuojame kainą po mėnesio (30 dienų į priekį)
future_days = X.iloc[-1]["Days"] + 30
future_price = model.predict([[future_days]])

print(f"Prognozuojama naftos kaina po mėnesio: {future_price[0]:.2f}")

# Nubraižome grafiką
plt.scatter(X, y, color="green", label="Naftos kainos per laikotarpį 2015-2025")
plt.plot(X, model.predict(X), color="orange", label="Prognozuojama kaina")
plt.axvline(future_days, color="black", linestyle="-", label="Po mėnesio")
plt.legend()
plt.xlabel("Dienos")
plt.ylabel("Naftos kaina")
plt.title("Naftos kainų prognozė")
plt.show()
