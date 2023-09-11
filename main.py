import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
from datetime import datetime
from append_df import append_to_excel
from alerta_discord import enviar_alerta_discord
from dolar_hoy import obtener_dolar_blue

#limpiador texto andres
def get_clean_text(texto):
    return texto.replace('\n','').replace('\t','').replace('.','').replace(',','.').replace('$','')

dolar_blue = obtener_dolar_blue()
fechab = datetime.now().strftime('%d/%m/%Y')

file_name = 'mobilar.xlsx'
cate = ['https://www.mobilar.com.ar/t/tv-audio-y-video',
        'https://www.mobilar.com.ar/t/climatizacion',
        'https://www.mobilar.com.ar/t/tecnologia',
        'https://www.mobilar.com.ar/t/hogar',
        'https://www.mobilar.com.ar/t/pequenos-electrodomesticos',
        'https://www.mobilar.com.ar/t/hogar/homedeco']

url ='https://www.mobilar.com.ar/t/tv-audio-y-video'

total_categorias = len(cate)
contador_bucle = 0
while contador_bucle < total_categorias:
    res = requests.get(url)    
    res.raise_for_status()
    if res.status_code ==200:
        soup = bs(res.text, 'html.parser')

        #usando find_all
        selector_names = soup.find_all("h3")
        names_products = [get_clean_text(names.text) for names in selector_names if "Filtrar por" not in names.text]
        
        #precios 
        selector_precios = soup.find_all('span', class_="price product-price precio-list")
        precios = [get_clean_text(precio.text) for precio in selector_precios]

        #usando selectores
        selector_links = soup.select("h3 > a")
        links = [link['href'] for link in selector_links]        

        #dataframe y crear o append excel
        df = pd.DataFrame({"fecha": fechab,
                           "titulo": names_products,
                           "precios": [float(precio) for precio in precios],
                           "dolar_hoy": [float(dolar_blue)] * len(names_products),  # Duplicar el valor para cada fila 
                           "url": links})
        df['precio_dolar'] = df['precios'] / df['dolar_hoy']
        
        append_to_excel(file_name,df)
        
        next_page = len(soup.select('li.next_page > a'))
        if next_page != 0:
            next_page = soup.select('li.next_page > a')[0]
            url = 'https://www.mobilar.com.ar' + next_page.get('href')            
        else:
            contador_bucle += 1
            if contador_bucle != total_categorias:
                url = cate[0+contador_bucle]
                print (url)
            else:
                break
        
    
    else:
        print(f"La direccion {url} no respode. Intente mas tarde...")
        break

enviar_alerta_discord(file_name)