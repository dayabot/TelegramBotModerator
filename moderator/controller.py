# -*- coding: utf-8 -*-
from telegram import Update
from telegram.ext import CallbackContext

from moderator.util import handle_context


def start(update, context):
    update.message.reply_text('👋👋👋')


def ban(update: Update, context: CallbackContext):
    bot, chat_id, user_ids = handle_context(update, context)

    if not user_ids:
        update.message.reply_text('直接回复用户消息进行踢出～')

    for user_id in user_ids:
        try:
            bot.kick_chat_member(chat_id, user_id=user_id)
            update.message.reply_text('已将该用户永久踢出！')
        except Exception as e:
            update.message.reply_text(str(e))


def unban(update: Update, context: CallbackContext):
    bot, chat_id, user_ids = handle_context(update, context)

    if not user_ids:
        update.message.reply_text('直接回复用户消息进行解冻')

    for user_id in user_ids:
        try:
            bot.unban_chat_member(chat_id, user_id=user_id)
            update.message.reply_text('知错能改，已将该用户解冻！')
        except Exception as e:
            update.message.reply_text(str(e))


def get_status(update: Update, context: CallbackContext):
    bot, chat_id, user_ids = handle_context(update, context)

    for user_id in user_ids:
        try:
            # bot.get_chat_member(chat_id, user_id=user_id)
            update.message.reply_text(f'用户状态：正常')
        except Exception as e:
            update.message.reply_text(str(e))


def reply_handler(update: Update, context: CallbackContext):
    user = update.message.from_user
    pass
