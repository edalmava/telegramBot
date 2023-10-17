import requests

url = 'https://lista.edalmava.workers.dev/'
payload = {'codigoEmpleo': '185139', 'codigoConvocatoria': "secretaría"}
response = requests.post(url, json=payload)

data = response.json()

text = data[0].get('numeroActo')
text += str(data[0].get('lista').get('id'))
text += data[0].get('fechaPublicacion')
text += str(data[0].get('estadoPublicado'))
text += str(data[0].get('lista').get('publicaElegible').get('id'))

url = 'https://listadet.edalmava.workers.dev/'
payload = {'id': data[0].get('lista').get('publicaElegible').get('id')}

response = requests.post(url, json=payload)

data = response.json()

for i in data:
    text += i.get('identificacion')

print(text)