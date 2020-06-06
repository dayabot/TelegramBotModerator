# -*- coding: utf-8 -*-

from telegram import Bot, Update

from moderator.db.model import TelegramChat, TelegramUser
from moderator.util.logger import logger


def new_chat_members(bot: Bot, update: Update):
    logger.info("new chat members...")
    message = update.message
    for user in message.new_chat_members:
        if user.is_bot and user.id == bot.id:
            TelegramChat.add(message.chat.id, message.chat.title)

        TelegramUser.get_or_create(user.id, user.username)

    logger.info("new chat members... done!")


def left_chat_member(bot: Bot, update: Update):
    logger.info("left chat members...")
    message = update.message
    left_user = update.message.left_chat_member

    # 将机器人所在群组删除
    if left_user.is_bot and left_user.id == bot.id:
        removed = TelegramChat.remove(message.chat.id)
        logger.info(f"  find bot {left_user.full_name}, chat {message.chat.title} removed({removed})")

    logger.info(f"done!!")


def reply_handler(bot: Bot, update: Update):
    logger.info("handle user message...")
    t_user = update.message.from_user
    user, created = TelegramUser.get_or_create(t_user.id, t_user.username)
    logger.info(f"handle user done!! user: {user}, created: {created}")
