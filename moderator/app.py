import os

import telegram
from flask import Flask, request
from telegram.ext import CommandHandler, MessageHandler, Filters, Dispatcher

from moderator.controller import start, ban, unban, get_status, reply_handler
from moderator.util import error

app = Flask(__name__)
TOKEN = os.environ['TELEGRAM_TOKEN']
bot = telegram.Bot(token=TOKEN)
dp = Dispatcher(bot, None)

# on different commands - answer in Telegram
dp.add_handler(CommandHandler("help", start))
dp.add_handler(CommandHandler("ban", ban))
dp.add_handler(CommandHandler("unban", unban))
dp.add_handler(CommandHandler("id", get_status))
dp.add_handler(MessageHandler(Filters.text, reply_handler))
# log all errors
dp.add_error_handler(error)


@app.route('/hook', methods=['POST'])
def webhook_handler():
    """Set route /hook with POST method will trigger this method."""
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)

        # Update dispatcher process that handler to process this message
        dp.process_update(update)

    return 'ok'


@app.route('/')
def index():
    return 'hello!'
