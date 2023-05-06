import requests

# Tu clave de API de CoinMarketCap
API_KEY = '0ac237d7-f290-473b-9ab8-eb607987a937'

# Hacer una solicitud GET a la API de CoinMarketCap para obtener los datos de ETH
url = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?id=1027&convert=MXN'
headers = {'X-CMC_PRO_API_KEY': API_KEY}
response = requests.get(url, headers=headers)

# Analizar la respuesta JSON y obtener el precio actual de ETH
data = response.json()
eth_price = data['data']['1027']['quote']['MXN']['price']

# Imprimir el precio actual de ETH en USD
print(f'El precio actual de ETH es: {eth_price} MXN')


def py():
    return eth_price
