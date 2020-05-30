# -*- coding: utf-8 -*-
import logging

# Enable logging
from telegram import Update, MessageEntity, ParseMode

from moderator.core.User import User
from moderator.model.model import TelegramUser

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.error('Update "%s" caused error "%s"', update, error)


def build_user(d_user):
    return User(d_user.user_id, d_user.username, d_user.status)


def get_chat_id_and_users(update: Update):
    message = update.message
    chat_id = message.chat.id

    all_users = []

    # 1. 直接回复的情况
    replay_user_id, replay_username = id_from_reply(message)
    if replay_user_id and replay_username:
        d_user, __ = TelegramUser.get_or_create(replay_user_id, replay_username)
        all_users.append(build_user(d_user))

    # 2. at 对应的人
    mentioned_usernames = ids_from_mentions(message)
    for mentioned_username in mentioned_usernames:
        d_user = TelegramUser.get_by_username(mentioned_username)
        if d_user:
            all_users.append(build_user(d_user))
        else:
            all_users.append(User(username=mentioned_username, user_id=0, is_active=True))

    return chat_id, all_users


def id_from_reply(message):
    prev_message = message.reply_to_message
    if not prev_message:
        return None, None

    from_user = prev_message.from_user
    return from_user.id, from_user.username


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


def reply(update, msg):
    update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
