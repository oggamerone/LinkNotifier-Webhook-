import requests
import time
import json


#Link da webhook do seu canal, você pode adicionar varias webhook ex: webhook_url = "dkdksdsldksldkskdskdks", "WEbhook 2"
webhook_url = ''
notified_item_ids = set()


def send_discord_webhook(content):
  data = {'content': content}
  headers = {'Content-Type': 'application/json'}
  response = requests.post(webhook_url, data=json.dumps(data), headers=headers)
  if response.status_code != 204:
    print('Ocorreu um erro ao enviar o webhook do Discord.')


def check_for_new_items():
  url = 'https://catalog.roblox.com/v1/search/items/details'
  params = {
    'Category': '11',  # Categoria para itens limitados
    'salesTypeFilter': '1',  # Filtro de tipo de venda (1 = Todos)
    'SortType': '3',  # Tipo de classificação (3 = Mais recente)
    'IncludeNotForSale': 'True',  # Incluir itens não disponíveis para venda
    'Limit': '30'  # Limite de resultados
  }

  response = requests.get(url, params=params)
  if response.status_code == 200:
    data = response.json()
    for item in data['data']:
      item_id = item['id']
      if item_id not in notified_item_ids:
        item_name = item['name']
        item_price = item.get('price', 'Preço não disponível')
        item_url = f'https://www.roblox.com/catalog/{item_id}/'

        # Envia a notificação para o Discord
        content = f'Novo item limitado encontrado!\nNome: {item_name}\nPreço: {item_price}\nURL: {item_url}'
        send_discord_webhook(content)

        
        notified_item_ids.add(item_id)
  else:
    print(
      'Ocorreu um erro ao obter os detalhes dos itens do catálogo do Roblox.')


while True:
  check_for_new_items()

  time.sleep(5)  # Aguarda 5 segundos antes de verificar novamente, você alterar para qualquer temp
