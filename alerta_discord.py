import pandas as pd
from datetime import datetime
import requests

def enviar_alerta_discord(fpath):
    today = datetime.now()
    hoy = datetime.strftime(today, '%d/%m/%Y')

    pd.set_option("display.max_colwidth", None)
    df_planilla = pd.read_excel(fpath)

    # Filtra el DataFrame en una sola línea
    df_filtrado = df_planilla[(df_planilla['var_perc'] < -20) & (df_planilla.eq(hoy).any(axis=1))]

    # Redondea la columna 'var_perc' en su lugar
    df_filtrado['var_perc'] = df_filtrado['var_perc'].round(2)

    # Crea un mensaje para cada fila
    mensajes = []
    for _, row in df_filtrado.iterrows():
        mensaje = f"oferta {row['fecha']} {row['titulo']} está con {row['var_perc']} % de descuento, en la web: {row['url']}"
        mensajes.append(mensaje)

    url = "https://discord.com/api/webhooks/1135358586025955339/yNZpxyaBPx37SUCbd3HaEFKOcKccCIWaudavJtCTNuxbXBNCAveDs3M9Ky-BamPb1drN"

    for mensaje in mensajes:
        data = {"username": "Gg", "content": mensaje}
        status_discord = requests.post(url, json=data)
        print(status_discord)

