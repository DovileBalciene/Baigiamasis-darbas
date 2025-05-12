import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import os
from keras import Sequential
from tensorflow.keras import Input
from tensorflow.keras import Sequential
from tensorflow.keras. layers import Flatten, Dense

file_path = 'C:/Users/dovil/PycharmProjects/Baigiamasis_darbas/Nafta_nuo_2015_01_01_iki_2025_04_30.csv'

df = pd.read_csv(file_path)

data = df[['Open', 'Close']].copy()

data.columns = ['Open', 'Close']

data['Open_num'] = data ['Open'].map({'High':0, 'Volume':1})

X = data[['Open_num']].values.astype(float)
y = data[['Close']].values.astype(float)

model = Sequential([
    Input(shape=(1,)),
    Dense(4, activation='relu'),
    Dense(1)

])

model.compile(loss='mse', # vidutine kvadratine klaida
              optimizer='adam',
              metrics=["mae"] # mean apsolute erorr
              )
model.summary()

history = model.fit(X, y,
                    epochs=100,
                    validation_split=0.2,
                    verbose=2)

plt.figure(figsize = (6, 4))
plt.plot(history.history['loss'], label='loss')
plt.plot(history.history['val_loss'], label='val_loss')
plt.xlabel('Epoch')
plt.ylabel('MSE Nuostolis')
plt.title('Naftos kainos pokytis')
plt.legend()
plt.show()

pred_female = model.predict(X[[0]])[0, 0]
pred_male = model.predict(X[[1]])[0, 0]

print(f'{pred_female:.1f}')
print(f'{pred_male:.1f}')

# Kodas įkrauna naftos kainų duomenis iš CSV failo,
# apmoko paprastą dviejų sluoksnių neuroninį tinklą prognozuoti uždarymo kainą remiantis atidarymo kaina,
# ir pateikia prognozes dviem pirmam duomenų taškams.