import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from datetime import datetime
from append_df import append_to_excel
from alerta_discord import enviar_alerta_discord
from dolar_hoy import obtener_dolar_blue
from util import get_clean_text


# Parametros para scraper en diccionario
selectors_dict = {
    'mobilar': {
        'names_selector': ('h3'),
        'precios_selector': ('span.price.product-price.precio-list'),
        'links_selector': ('h3 > a'),
        'next_page_selector': ('li.next_page > a'),
        'home_page': ('https://www.mobilar.com.ar'),
        'cate' : ('https://www.mobilar.com.ar/t/tv-audio-y-video',
    'https://www.mobilar.com.ar/t/climatizacion',
    'https://www.mobilar.com.ar/t/tecnologia',
    'https://www.mobilar.com.ar/t/hogar',
    'https://www.mobilar.com.ar/t/pequenos-electrodomesticos',
    'https://www.mobilar.com.ar/t/hogar/homedeco')
    },
    'musimundo': {
        'names_selector': ('h3'),
        'precios_selector': ('span.mus-pro-price-number'),
        'links_selector': ('div.mus-pro-thumb > a'),
        'next_page_selector': ('li.next.square.not-border > a'),
        'home_page': ('https://www.musimundo.com'),
        'cate' : ('https://www.musimundo.com/climatizacion/c/2',
    'https://www.musimundo.com/audio-tv-video/c/3',
    'https://www.musimundo.com/electrohogar/c/7',
    'https://www.musimundo.com/telefonia/c/5',
    'https://www.musimundo.com/informatica/c/6',
    'https://www.musimundo.com/pequenos/c/8',
    'https://www.musimundo.com/gaming/c/1',
    'https://www.musimundo.com/cuidado-personal-y-salud/c/164',
    'https://www.musimundo.com/hogar-y-aire-libre/c/10',
    'https://www.musimundo.com/ninos/c/15',
    'https://www.musimundo.com/camaras/c/4',
    'https://www.musimundo.com/rodados/c/9')
    },
    # Define aquí selectores y demas para otras páginas si es necesario
}

locales = ['mobilar', 'musimundo'] # Agregar aqui mas locales
contador_locales = 0
file_name = 'scrape.xlsx'
page_name = locales[0]
dolar_blue = obtener_dolar_blue()
fechab = datetime.now().strftime('%d/%m/%Y')

if page_name in selectors_dict:
    selectors = selectors_dict[page_name]
    categoria = selectors['cate']
    url = categoria[0]
else:
    print(f"No se encontraron selectores para la página '{page_name}'.")

contador_bucle = 0
while contador_bucle < len(categoria):
    res = requests.get(url)
    res.raise_for_status()
    if res.status_code ==200:
        soup = bs(res.text, 'html.parser')

        #usando find_all
        selector_names = soup.find_all(selectors['names_selector'])
        names_products = [get_clean_text(names.text) for names in selector_names if "Filtrar por" not in names.text]

        #precios
        selector_precios = soup.select(selectors['precios_selector'])
        precios = [get_clean_text(precio.text) for precio in selector_precios]

        #usando selectores
        selector_links = soup.select(selectors['links_selector'])
        links = [link['href'] for link in selector_links]
        for i in range (len(links)):
          if links[i].startswith('/'):
            links[i] = selectors['home_page'] + links[i]

        #dataframe y crear o append excel
        df = pd.DataFrame({"fecha": fechab,
                           "titulo": names_products,
                           "precios": [float(precio) for precio in precios],
                           "dolar_hoy": [float(dolar_blue)] * len(names_products),  # Duplicar el valor para cada fila
                           "url": links})
        df['precio_dolar'] = df['precios'] / df['dolar_hoy']

        append_to_excel(file_name,df)

        next_page_link = soup.select_one(selectors['next_page_selector'])
        if next_page_link:
            url = selectors['home_page'] + next_page_link.get('href')
            print (url)
        else:
            contador_bucle += 1
            if contador_bucle < len(categoria):
                url = categoria[contador_bucle]
                print (url)
            else:
                contador_locales += 1
                if contador_locales < len(locales):
                    page_name = locales[contador_locales]
                    if page_name in selectors_dict:
                        selectors = selectors_dict[page_name]
                        categoria = selectors['cate']
                        url = categoria[0]
                        contador_bucle = 0
                else:
                    break


    else:
        print(f"La direccion {url} no respode. Intente mas tarde...")
        break

enviar_alerta_discord(file_name)