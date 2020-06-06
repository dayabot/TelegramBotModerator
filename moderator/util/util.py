# -*- coding: utf-8 -*-

# Enable logging
from telegram import Update, MessageEntity, Bot

from moderator.core.model.user import User
from moderator.db.model import TelegramUser


def get_chat_id_and_users(bot: Bot, update: Update):
    """ 用户主动输入做操作的场景 """
    all_users = []

    message = update.message
    chat_id = message.chat.id

    # 1. 直接回复的情况
    replay_user_id, replay_username = id_from_reply(message)
    if replay_user_id and replay_username:
        user, __ = TelegramUser.get_or_create(replay_user_id, replay_username)
        all_users.append(User.build_user_from_db(user))

    # 2. at 对应的人
    mentioned_usernames = ids_from_mentions(message)
    for mentioned_username in mentioned_usernames:
        user = TelegramUser.get_by_username(mentioned_username)
        if user:
            all_users.append(User.build_user_from_db(user))

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

