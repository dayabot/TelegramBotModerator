# -*- coding: utf-8 -*-
from telegram import ParseMode


def send_message(bot, chat_id, msg):
    bot.send_message(chat_id, msg, parse_mode=ParseMode.MARKDOWN)
