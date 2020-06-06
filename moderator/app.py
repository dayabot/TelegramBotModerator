import os

from flask import Flask, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

import telegram
from telegram.ext import CommandHandler, MessageHandler, Filters, Dispatcher

TOKEN = os.environ['TELEGRAM_TOKEN']
bot = telegram.Bot(token=TOKEN)

from moderator.view import start, ban, unban, get_status, reply_handler, new_chat_members, left_chat_member, promote, \
    demote, is_admin

dp = Dispatcher(bot, None, workers=10)
# on different commands - answer in Telegram
dp.add_handler(CommandHandler("help", start))
dp.add_handler(CommandHandler("ban", ban))
dp.add_handler(CommandHandler("unban", unban))
dp.add_handler(CommandHandler("id", get_status))
dp.add_handler(CommandHandler("addmanager", promote))
dp.add_handler(CommandHandler("removemanager", demote))
dp.add_handler(CommandHandler("manager", is_admin))
dp.add_handler(MessageHandler(Filters.text, reply_handler))
dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, new_chat_members))
dp.add_handler(MessageHandler(Filters.status_update.left_chat_member, left_chat_member))


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
