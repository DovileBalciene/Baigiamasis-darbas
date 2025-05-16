import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

#Šis kodas naudoja paprastą linijinę regresiją
# Įkeliame CSV failą
df = pd.read_csv("naftos_kainos.csv")

# Konvertuojame datą į datetime formatą ir nustatome kaip indeksą
df["Date"] = pd.to_datetime(df["Date"])
df.set_index("Date", inplace=True)

# Sukuriame papildomą laiko požymį (dienų skaičius nuo pirmos datos)
df["Days"] = (df.index - df.index[0]).days

# Pasirenkame požymius ir tikslinį kintamąjį
X = df[["Days"]]
y = df["Price"]

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
plt.scatter(X, y, color="blue", label="Istoriniai duomenys")
plt.plot(X, model.predict(X), color="red", label="Prognozė")
plt.axvline(future_days, color="green", linestyle="--", label="Po mėnesio")
plt.legend()
plt.xlabel("Dienos")
plt.ylabel("Naftos kaina")
plt.title("Naftos kainų prognozė")
plt.show()
