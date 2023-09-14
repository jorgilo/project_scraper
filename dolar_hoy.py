import requests
from bs4 import BeautifulSoup as bs


def obtener_dolar_blue():
    url = 'https://dolarhoy.com'

    try:
        res_dolar = requests.get(url)
        res_dolar.raise_for_status()
        soup_dolar = bs(res_dolar.text, 'html.parser')

        # Busca directamente el elemento deseado
        dolar_blue = soup_dolar.find("div", class_="venta").find("div", class_="val").text.strip('$')

        return float(dolar_blue)

    except requests.exceptions.RequestException as e:
        print(f"Error al obtener el valor del dólar blue: {e}")
        return None