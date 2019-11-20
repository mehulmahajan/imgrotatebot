import requests
from threading import Thread
from datetime import datetime,timedelta
from time import sleep
from PIL import Image
import os 

from flask import Flask,redirect, url_for,request,render_template
app = Flask(__name__)

domain='rotatebot'

print('Started')
@app.route('/')
def main():
    return f'''<html><head><title>Telegram Echobot</title></head><body>Telegram Echobot</body></html>'''
def alink(s,k=None):
    if not k:k=s
    return '<a href="{}">{}</a>'.format(s,k)


# ----------

import logging
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

TOKEN = 'Please enter your bot token here'
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          CallbackQueryHandler,ConversationHandler)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def photo(update, context):
    photo_file = update.message.photo[-1].get_file()
    photo_file.download(f'{update.effective_chat.id}.jpg')
    keyboard =  [[InlineKeyboardButton("Rotate Left", callback_data='Left')],
         [InlineKeyboardButton("Rotate Upsidedown", callback_data='Upsidedown')],
         [InlineKeyboardButton("Rotate Right", callback_data='Right')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(text="Please select an option.",reply_markup=reply_markup)
import logging
def rotate(update,context):
    query=update.callback_query
    eid=update.effective_chat.id
    img = Image.open(f'{eid}.jpg')
    if query.data == "Left":
        img = img.rotate(90)
    if query.data == "Upsidedown":
        img = img.rotate(180)
    if query.data == "Right":
        img = img.rotate(270)
    img.save("Any.jpg")
    context.bot.send_photo(chat_id=eid, photo=open('./Any.jpg', 'rb'))

def start(update, context):
    if update.message.text=='w':
        photo(update,context)
        update.message.reply_text('wW')
    else:
        update.message.reply_text('Please send me an image for rotate.')

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.photo, photo))
    dp.add_handler(MessageHandler(Filters.text, start))
    dp.add_handler(CallbackQueryHandler(rotate))
    dp.add_error_handler(error)
    updater.start_polling()
# ----------

def snt(f,a,b=None):
  try:
    Thread(None,f,None,a,b).start()
  except Exception as e:        
    return str(e)


def restart():
  requests.head(f'http://{domain}.herokuapp.com/gtcheck',timeout=50)
  while True:
    try:
      v=(datetime.utcnow()+timedelta(hours=5,minutes=30))
      if(1 or 5*60<v.hour*60+v.minute<21*60+30):
        requests.head(f'http://{domain}.herokuapp.com/up/pys',timeout=50)
      sleep(25*60)
    except Exception as e:
      exception(e)
      sleep(2*60)
      continue

# snt(restart,())
snt(main,())

if __name__ == '__main__':
    # app.run()
    pass

