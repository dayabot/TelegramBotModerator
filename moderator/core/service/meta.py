# -*- coding: utf-8 -*-
from telegram import Update, Bot

from moderator.db.model import AllChats
from moderator.util.logger import logger
from moderator.util.permision import admin


@admin
def groups(bot: Bot, update: Update):
    logger.info("querying all groups...")
    chat_id = update.message.chat.id
    bot.send_message(chat_id, ", ".join(AllChats.get_chat_names()), parse_mode=None)
    logger.info("done")
