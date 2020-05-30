# -*- coding: utf-8 -*-
from telegram import Update, Bot

from moderator.util import get_chat_id_and_user_ids


def start(bot: Bot, update: Update):
    update.message.reply_text('👋👋👋')


def ban(bot: Bot, update: Update):
    chat_id, user_ids = get_chat_id_and_user_ids(update)

    if not user_ids:
        update.message.reply_text('直接回复用户消息进行踢出～')

    for user_id in user_ids:
        try:
            bot.kick_chat_member(chat_id, user_id=user_id)
            update.message.reply_text('已将该用户永久踢出！')
        except Exception as e:
            update.message.reply_text(str(e))


def unban(bot: Bot, update: Update):
    bot, chat_id, user_ids = get_chat_id_and_user_ids(update)

    if not user_ids:
        update.message.reply_text('直接回复用户消息进行解冻')

    for user_id in user_ids:
        try:
            bot.unban_chat_member(chat_id, user_id=user_id)
            update.message.reply_text('知错能改，已将该用户解冻！')
        except Exception as e:
            update.message.reply_text(str(e))


def get_status(bot: Bot, update: Update):
    bot, chat_id, user_ids = get_chat_id_and_user_ids(update)

    for user_id in user_ids:
        try:
            # bot.get_chat_member(chat_id, user_id=user_id)
            update.message.reply_text('用户状态：正常')
        except Exception as e:
            update.message.reply_text(str(e))


def reply_handler(bot: Bot, update: Update):
    user = update.message.from_user
    pass
