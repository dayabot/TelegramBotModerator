# -*- coding: utf-8 -*-
import logging

# Enable logging
from telegram import Update, MessageEntity
from telegram.ext import CallbackContext

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def handle_context(update: Update, context: CallbackContext):
    bot = context.bot
    message = update.message
    chat_id = message.chat.id

    user_ids = []

    # 1. 直接回复的情况
    reply_user_id = id_from_reply(message)
    if reply_user_id:
        user_ids.append(reply_user_id)

    # 2. at 对应的人
    mentioned_usernames = ids_from_mentions(message)
    if mentioned_usernames:
        user_ids += mentioned_usernames

    return bot, chat_id, user_ids


def id_from_reply(message):
    prev_message = message.reply_to_message
    if not prev_message:
        return
    user_id = prev_message.from_user.id
    return user_id


def ids_from_mentions(message):
    ids = []
    entities = list(message.parse_entities([MessageEntity.TEXT_MENTION, MessageEntity.MENTION]))

    for ent in entities:
        user_id = None
        if ent.type == MessageEntity.TEXT_MENTION:
            user_id = ent.user.id
        elif ent.type == MessageEntity.MENTION:
            username = message.text[ent.offset:ent.offset + ent.length]
            if username and username.startswith("@"):
                user_id = username[1:]

        user_id and ids.append(user_id)

    return ids
