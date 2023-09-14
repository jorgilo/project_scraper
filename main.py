import requests
from bs4 import BeautifulSoup as bs
from append_df import append_to_excel
from alerta_discord import enviar_alerta_discord
from scraper import scrape_page


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

locales = ['mobilar', 'musimundo']
contador_locales = 0
file_name = 'scryther.xlsx'
page_name = locales[0]

if page_name in selectors_dict:
    selectors = selectors_dict[page_name]
    categoria = selectors['cate']
    url = categoria[0]
else:
    print(f"No se encontraron selectores para la página '{page_name}'.")

contador_bucle = 0
while contador_bucle < len(categoria):
    
    df_resultado = scrape_page(url, selectors)    
    append_to_excel(file_name, df_resultado)
    res = requests.get(url)
    res.raise_for_status()    
    if res.status_code == 200:
        soup = bs(res.text, 'html.parser')
        soup = bs(res.text, 'html.parser')
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

enviar_alerta_discord(file_name)   
