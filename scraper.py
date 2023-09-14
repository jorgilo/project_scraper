import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from datetime import datetime
from dolar_hoy import obtener_dolar_blue
from util import get_clean_text

def scrape_page(url, selectors):
    try:
        dolar_blue = obtener_dolar_blue()
        fechab = datetime.now().strftime('%d/%m/%Y')

        res = requests.get(url)
        res.raise_for_status()

        if res.status_code == 200:
            soup = bs(res.text, 'html.parser')

            #names_selector, precios_selector, links_selector, home_page, cate = selectors.values()

            # Usando find_all
            selector_names = soup.find_all(selectors['names_selector'])
            names_products = [get_clean_text(names.text) for names in selector_names if "Filtrar por" not in names.text]

            # Precios
            selector_precios = soup.select(selectors['precios_selector'])
            precios = [get_clean_text(precio.text) for precio in selector_precios]

            # Usando selectores
            selector_links = soup.select(selectors['links_selector'])
            links = [link['href'] for link in selector_links]
            for i in range(len(links)):
                if links[i].startswith('/'):
                    links[i] = selectors['home_page'] + links[i]

            # DataFrame y crear o append Excel
            df = pd.DataFrame({"fecha": [fechab] * len(names_products),
                               "titulo": names_products,
                               "precios": [float(precio) for precio in precios],
                               "dolar_hoy": [float(dolar_blue)] * len(names_products),  # Duplicar el valor para cada fila
                               "url": links})
            df['precio_dolar'] = df['precios'] / df['dolar_hoy']

            return df

        else:
            print(f"La dirección {url} no responde. Intente más tarde...")
            return None

    except Exception as e:
        print(f"Error al procesar la URL {url}: {e}")
        return None