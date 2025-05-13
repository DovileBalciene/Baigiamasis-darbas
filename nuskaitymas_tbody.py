import csv

from selenium import webdriver # Webdriveris narsykles automatizavimui
from selenium.common import ElementNotInteractableException, TimeoutException, NoSuchElementException


"""
- ElementNotInteractableException - klaida, kuri pasirodo kai programa bando paspausti arba įvesti tekstą į elementą, 
kurio tuo metu negalima pasiekti.

- TimeoutException - klaida, kuri pasirodo kai programa per ilgai laukia kažko įvykstant 
(pvz., elemento atsiradimo puslapyje).
"""
from selenium.webdriver.chrome.service import Service # Importuoja serveri kuris leidzia paleisti narsykle "Chrome"
from selenium.webdriver.common.by import By # Leidzia pasirinkti elementus pagal skirtingus kriterijus (ID, CSS_SELECTOR)
from selenium.webdriver.support.ui import WebDriverWait # Leidzia laukti iki kol bus pasiektas reikiamas elementas
from selenium.webdriver.support import expected_conditions as EC # Patikrina ar atlieka veiksma (pvz. paspaudzia mygtuka)
from webdriver_manager.chrome import ChromeDriverManager
"""
Ši eilutė įtraukia įrankį, kuris padeda valdyti Chrome naršyklę. 
ChromeDriverManager automatiškai suranda ir įdiegia reikiamą programinę įrangą, 
kad galėtume automatizuoti Chrome naršyklę. 
Nereikia nieko daryti rankiniu būdu - viskas sutvarkoma automatiškai.
"""
import time # Laiko tarpas per kuri spetu uzkrauti puslapi

options = webdriver.ChromeOptions()
# options.add_argument('--headless')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 20)  # Suteikia laukimo laika (10 sec) kol ivykdys nurodyta salyga
driver.maximize_window() # Atidarys pilnai langa

driver.get("https://markets.businessinsider.com/commodities/oil-price?type=wti?utm_source=feedly") # Atidaro svetaines puslapi kur yra katalogas
#base_url = "https://markets.businessinsider.com/commodities/oil-price?type=wti?utm_source=feedly" # nurodo pagrindine nuoroda (URL)


table_body = driver.find_element(By.CSS_SELECTOR, "tbody")

table_rows = table_body.find_elements(By.TAG_NAME, "tr")


for row in table_rows:
    table_data = row.find_elements(By.TAG_NAME, "td")
    row_data = []
    for data in table_data:
        row_data.append(data.text)
        print(row_data)


    # except (FileNotFoundError, NoSuchElementException, WebDriverException):
    #     print(" nerasta")
    #         break




print(f"Rasta {len(row_data)} duomenu.")
with open("C:/Users/Vartotojas/PycharmProjects/Baigiamasis-darbas/lentele.txt", "w") as file:
        for link in row_data:
            file.write(link + "/n")
driver.quit()
