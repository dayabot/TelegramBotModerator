import os

import telegram
from flask import Flask, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from telegram.ext import CommandHandler, MessageHandler, Filters, Dispatcher

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

from moderator.controller import start, ban, unban, get_status, reply_handler

migrate = Migrate(app, db)

TOKEN = os.environ['TELEGRAM_TOKEN']
bot = telegram.Bot(token=TOKEN)
dp = Dispatcher(bot, None, workers=10)

# on different commands - answer in Telegram
dp.add_handler(CommandHandler("help", start))
dp.add_handler(CommandHandler("ban", ban))
dp.add_handler(CommandHandler("unban", unban))
dp.add_handler(CommandHandler("id", get_status))
dp.add_handler(MessageHandler(Filters.text, reply_handler))


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
