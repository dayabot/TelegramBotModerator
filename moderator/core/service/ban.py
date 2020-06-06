# -*- coding: utf-8 -*-
from telegram import Bot, Update

from moderator.core.service.welcome import TIP_TEMPLATE
from moderator.db.model import AllChats
from moderator.util.logger import logger
from moderator.util.message import send_message
from moderator.util.permision import admin
from moderator.util.util import get_chat_id_and_users


@admin
def ban(bot: Bot, update: Update):
    logger.info("ban user...")
    chat_id, users = get_chat_id_and_users(bot, update)
    if not users:
        send_message(bot, chat_id, TIP_TEMPLATE + '进行踢出～')

    for user in users:
        AllChats.ban(bot, chat_id, user)

    logger.info("ban user done!!!")


@admin
def unban(bot: Bot, update: Update):
    logger.info("unban user...")
    chat_id, users = get_chat_id_and_users(bot, update)
    if not users:
        send_message(bot, chat_id, TIP_TEMPLATE + '进行解冻')

    for user in users:
        AllChats.unban(bot, chat_id, user)

    logger.info("unban user done!!!")
