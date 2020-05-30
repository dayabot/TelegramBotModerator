import os

from flask import Flask

import telegram
from telegram.ext import CommandHandler, Updater, MessageHandler, Filters

from moderator.controller import start, ban, unban, get_status, reply_handler
from moderator.util import error

app = Flask(__name__)
TOKEN = os.environ['TELEGRAM_TOKEN']
bot = telegram.Bot(token=TOKEN)
updater = Updater(TOKEN, use_context=True)

# Get the dispatcher to register handlers
dp = updater.dispatcher

# on different commands - answer in Telegram
dp.add_handler(CommandHandler("help", start))
dp.add_handler(CommandHandler("ban", ban))
dp.add_handler(CommandHandler("unban", unban))
dp.add_handler(CommandHandler("id", get_status))
dp.add_handler(MessageHandler(Filters.text, reply_handler))
# log all errors
dp.add_error_handler(error)

updater.start_polling()


@app.route('/hook', methods=['POST'])
def hello_world():
    return 'Hello World!'
