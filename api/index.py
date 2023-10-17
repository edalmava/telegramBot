import os
import re
import requests
from flask import Flask, request
import telegram

app = Flask(__name__)

@app.route('/')
def home():
    return '¡Bienvenido al Bot Opec!'

@app.route('/about')
def about():
    return 'Bot de Telegram de consulta de OPEC creado por Edalmava'

@app.route('/webhook', methods=['POST'])
def webhook():    
    bot = telegram.Bot(token=os.environ.get("TELEGRAM_TOKEN"))

    update = telegram.Update.de_json(request.get_json(force=True), bot)

    chat_id = update.message.chat.id
    msg_id = update.message.message_id

    text = update.message.text.encode('utf-8').decode()

    if text == "/start":
       # print the welcoming message
       bot_welcome = """
       Bienvenido al Bot de consulta de OPEC.
       """
       # send the welcoming message
       bot.sendMessage(chat_id=chat_id, text=bot_welcome, reply_to_message_id=msg_id)
    elif text == "/help":
       bot_welcome = """
       Envíe el número de la OPEC a consultar.
       """
       # send the welcoming message
       bot.sendMessage(chat_id=chat_id, text=bot_welcome, reply_to_message_id=msg_id)
    else:
       try:           
           #text = re.sub(r"\W", "_", text)           
           #url = "https://ui-avatars.com/api/?name={}&background=0D8ABC&color=fff&size=128".format(text.strip())           
           #bot.sendPhoto(chat_id=chat_id, photo=url, reply_to_message_id=msg_id)
           url = 'https://lista.edalmava.workers.dev/'
           payload = {'codigoEmpleo': text, 'codigoConvocatoria': "secretaría"}
           response = requests.post(url, json=payload)

           data = response.json()

           if len(data) == 0:
               bot.sendMessage(chat_id=chat_id, text='No hay lista disponible por el momento', parse_mode='HTML', reply_to_message_id=msg_id)
           else:
               text = f'<strong>{data[0].get("lista").get("empleoSimo").get("denominacion").get("nombre")}</strong>'
               text += f'<b>Nro. Resolución:</b> <a href="{data[0].get("urlActoAdministrativo")}">{data[0].get("numeroActo")}</a>\n'
               text += f'<b>Nro. Lista:</b> {str(data[0].get("lista").get("id"))}\n'
               text += f'<b>Fecha Publicación:</b> {data[0].get("fechaPublicacion")}\n'
               text += f'<b>Estado:</b> {str(data[0].get("estadoPublicado"))}\n\n'
               #text += str(data[0].get('lista').get('publicaElegible').get('id')) + '\n'

               url = 'https://listadet.edalmava.workers.dev/'
               payload = {'id': data[0].get('lista').get('publicaElegible').get('id')}

               response = requests.post(url, json=payload)

               data = response.json()

               for i in data:
                   text += f'<b>C.C:</b> {i.get("identificacion")}\n'

               bot.sendMessage(chat_id=chat_id, text=text, parse_mode='HTML', reply_to_message_id=msg_id)
       except Exception:
           # if things went wrong
           bot.sendMessage(chat_id=chat_id, text="There was a problem in the name you used, please enter different name", reply_to_message_id=msg_id)

    return 'OK'
