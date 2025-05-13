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
7. Apibendrinimas

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
https://github.com/DovileBalciene/Baigiamasi-darbas
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
from Selenium 
```
2. Puslapio URL nuskaitymas<br>
```
https://markets.businessinsider.com/commodities/oil-price?type=wti?utm_source=feedly
```
3. Postgres duomenų bazės sukūrimas<br>
```
init_db(Naftos_kaina)
```
4. Rezultatų gavimas<br>

---

### Duomenų analizė

1. Bibliotekų įkėlimas<br>
```
import pandas as pd
```
2. Duomenų failo įkėlimas<br>
```

```

3. Duomenų valymas 
   - Nereikalingų simbolių, reikšmių sutvarkymas 
   - Datos formato pakeitimas
   - Tekstinių stulpelių transformavimas į skaičius

4. Analizės atlikimas 
   - Vidutinės kainos suradymas, panaudojant funkciją mean()
   - Aukščiausios kainos grupavimas, pagal datą
   - Kainų skirtumas tarp mažiausios ir didžiausios naftos kainos
   - Naujos kategorijos: aukšta, vidutinė, žema sukūrimas
   
### Vizualizacijos
![Image](https://github.com/user-attachments/assets/a007ba92-5066-4790-ac50-3e7e126c3eb1)



