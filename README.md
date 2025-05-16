# BAIGIAMASIS DARBAS

# Užduotis:
Naftos kainų svyravimo analizė ir prognozė

---

# Tikslas:
Stebėti naftos kainų svyravimus ir prognozuoti jų pokyčius, remiantis istoriniais duomenimis bei aktualijomis.

---

# Reikalavimai:
- bs4: Surinkti duomenis iš tinklalapių tokių kaip oilprice.com, nasdaq.com 
- pandas: Apdoroti duomenis (valymas, grupavimas, transformavimas)
- matplotlib/plotly: Vizualizuoti naftos kainų svyravimus laike
- Neuroninis tinklas: Prognozuoti naftos kainas (pvz., kitą savaitę ar mėnesį)
- SQL: Saugoti duomenis ir modelio prognozes, atlikti bent 4-6 užklausas

---

## Turinys

1. Projekto apžvalga
2. Diegimo ir paleidimo instrukcijos
3. Puslapio nuskaitymas
4. Duomenų analizė
5. Vizualizacijos
6. Prognozės modelis
7. SQL
8. Apibendrinimas

---

### Projekto apžvalga

Vykdomas projektas leidžia stebėti ir analizuoti naftos kainų pokyčius. 
Naudojant Selenium metodą, nuskaitoma puslapio informacija. 
Naudojant Pandas vykdoma duomenų analizė. 
Pasitelkiant vizualizacijas, 
grafiškai atvaizduojame naftos kainų pokyčius. 

---

### Diegimas ir paleidimas

1. Saugyklos klonavimas iš GitHub<br>

```
https://github.com/DovileBalciene/Baigiamasis-darbas
```
```
cd Baigiamasis-darbas
```
2. Virtualios aplinkos sukūrimas<br>
```
python -m venv 
```
3. Priklausomybių įdiegimas<br>
```
pip install -r requirements.txt
```
4. Programos paleidimas<br>
```
python main.py
```

---

### Puslapio nuskaitymas

1. Naudojamų bibliotekų importavimas<br>
```
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from webdriver_manager.chrome import ChromeDriverManager
import time
```
2. Puslapio URL nuskaitymas, nuskaitoma naftos kainų lentelė<br>
```
https://markets.businessinsider.com/commodities/oil-price?type=wti?utm_source=feedly
```
![Image](https://github.com/user-attachments/assets/186fd680-f5cd-4afe-b22a-4cea1c217cba)


3. Rezultatų gavimas<br>
   - Naudojant selenium bibliotekas, nuskaitomas pasirinktas puslapis
   - Surandama pagrindinė klasė, apjungianti pagrindinę informaciją
   - Nuskaitomi reikalingi duomenys iš lentelės
   - Gaunami puslapio nuskaitymo rezultatai
   - Sukuriama duomenų bazė
   
---

### Duomenų analizė

1. Bibliotekų įkėlimas<br>
```
import pandas as pd
```
2. Duomenų failo įkėlimas<br>
```
Nafta_nuo_2015_01_01_iki_2025_04_30.csv
```

3. Duomenų valymas 
   - Nereikalingų simbolių, reikšmių sutvarkymas 
   - Datos formato pakeitimas
   - Tekstinių stulpelių transformavimas į skaičius

4. Analizės atlikimas 
   - Vidutinės kainos suradimas, panaudojant funkciją mean()
   - Aukščiausios kainos grupavimas, pagal datą
   - Kainų skirtumas tarp mažiausios ir didžiausios naftos kainos
   - Naujos kategorijos: aukšta, vidutinė, žema sukūrimas

---

### Vizualizacijos
![Image](https://github.com/user-attachments/assets/a007ba92-5066-4790-ac50-3e7e126c3eb1)

---

   - Naudojama Matplotlib pyplot biblioteka
   - Sukuriamas naujas stulpelio kintamasis (Year)
   - Piešiama PLOT vizualizacija, atvaizduojanti naftos kainų augimą, pagal metus
   - Pagal grafiką matoma, jog aukščiausia naftos kaina buvo 2022 metais
   - Mažiausia naftos kaina buvo fiksuojama 2018 metais

---

![Image](https://github.com/user-attachments/assets/7e3291fd-63bf-4402-912b-ac1aa8f15359)
   - Naudojamos bibliotekos<br>
```
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
```
   - Naudojamas tiesinės progresijos modelis,
leidžiantis prognozuoti naftos kainą pasirinktam laikotarpiui,
šiuo atmeju 1 mėnesiui.
   - Pagal prognozės modelį matome, jog prognozuojama naftos kaina po mėnėsio yra 40.89
   - Stebint istorinių duomenų pasiskirstymą matome, kad ilgą laiką 

---
### Prognozės modelis
---

![Image](https://github.com/user-attachments/assets/1831615c-eec5-409a-bc5a-ee959cd7a592)
   - Naudojamos bibliotekos
```
import pandas as pd
from sklearn.model_selection import train_test_split  
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score 
import matplotlib.pyplot as plt
```
   - Naftos kainų prognozė, naudojant neuroninį tinklą
   - Pasitelkiamas DecisionTreeClassifier modelis
   - Modeliui naudojami aukščiausios kainos ir datos kriterijai
   - Naudojama 'lambda' funkcija, kuri suteikia aukštos ir žemos klasės kriterijų, 
pagal nurodytą reikšmę if x > 80, naudojama reikšmė 1, o klasė Aukšta, 
kitu atveju 0 ir klasė Žema
   - Naudojamas modelis yra 0.98 tikslumo


---

### SQL
---
   - Naudojamos bibliotekos
```
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
```

   - Įkeliami duomenų bazę su "db_config"
   - Prisijungiame prie jos, naudodami "engine"
   - Kuriame SQL užklausas
   - Spausdiname rezultatus

---

### Apibendrinimas
   - Atlikus puslapio skenavimą, gauname rezultatus apie naftos kainą,
iš kurių galime kurti csv failą.
   - Pagal sukurtą failą, naudojame "pandas" atlikti duomenų analizei
   - Naudodami, neuroninius tinklus ir prognozės modelį, sukuriame vizualizacijas, atspindinčias duomenis
   - Sukurę "postgres" duomenų bazę, atliekame "sql" užklausas
   - Pagal surinktus duomenis matome, kad aukščiausią kainą nafta pasiekė 2022 metais
