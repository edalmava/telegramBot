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

           text = data[0].get('numeroActo') + '<br>'
           text += str(data[0].get('lista').get('id')) + '<br>'
           text += data[0].get('fechaPublicacion') + '<br>'
           text += str(data[0].get('estadoPublicado')) + '<br>'
           text += str(data[0].get('lista').get('publicaElegible').get('id')) + '<br>'

           url = 'https://listadet.edalmava.workers.dev/'
           payload = {'id': data[0].get('lista').get('publicaElegible').get('id')}

           response = requests.post(url, json=payload)

           data = response.json()

           for i in data:
               text += i.get('identificacion') + '<br>'

           bot.sendMessage(chat_id=chat_id, text=text, reply_to_message_id=msg_id)
       except Exception:
           # if things went wrong
           bot.sendMessage(chat_id=chat_id, text="There was a problem in the name you used, please enter different name", reply_to_message_id=msg_id)

    return 'OK'
