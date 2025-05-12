import pandas as pd
from sklearn.model_selection import train_test_split  #
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score # parodo proc kiek prognoze yra tiksli
import matplotlib.pyplot as plt

df = pd.read_csv('C:/Users/dovil/PycharmProjects/Baigiamasis_darbas/Nafta_nuo_2015_01_01_iki_2025_04_30.csv')
#print(df.head())

df['High Price'] = df['High'].apply(lambda x: 1 if x > 80 else 0)
# susikuriu kintamaji ir su apply ir lambda susikuriu fikrtyvia salyga, tikrins tik sita stulpeli

categorical_collumns = ['Date']
# pasirenku visus stulpelius kur yra tekstine reiksme, nes cia negali buti tekstiniu reiksmiu

label_encoder = {}
for col in categorical_collumns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoder[col] = le
# pavercia visus stulpelius i skaicius
X = df[categorical_collumns + ['Open']] # pasiima savybes
y = df['High Price'] # target bandysim atspeti ar atlyginimas yra aukstas ar zemas

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
#x,y train yra apmokomi modeliai, kurie uzima 80%
#test size 20% duomenu patikrinimui

# MODELIO KURIMAS
model = DecisionTreeClassifier(random_state=42, max_depth=5) # nurodom medzio gyli, kad butu galima ji koreguoti
model.fit(X_train, y_train) # atliekam mokymo funkcija is duomenu
y_pred = model.predict(X_test) #prognuozuoja ar atlyginimas yfra aukstas ar zemas

accuracy = accuracy_score(y_test, y_pred) # procentaliai ivertins kiek prognoziu buvo teisingu
# dalinam visas reiksmes lyginam savo reiksmes su turimom, grazina tiksluma

print(f'Tikslumas: {accuracy:.2f}')

plt.figure(figsize=[30,15])
plot_tree(model,feature_names=X.columns, class_names=['Zema', 'Auksta'], filled=True, rounded=True, fontsize=10)
plt.title('Sprendimu medis auksta ar zema naftos kaina')
plt.show()

