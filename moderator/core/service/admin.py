# -*- coding: utf-8 -*-

from telegram import Bot, Update

from moderator.core.service.welcome import TIP_TEMPLATE
from moderator.util.logger import logger
from moderator.util.message import send_message
from moderator.util.permision import admin
from moderator.util.util import get_chat_id_and_users


@admin
def promote(bot: Bot, update: Update):
    logger.info("promote user...")
    chat_id, users = get_chat_id_and_users(bot, update)
    if not users:
        send_message(bot, chat_id, TIP_TEMPLATE + '进行管理员添加操作')

    for user in users:
        user.promote(bot, chat_id)

    logger.info("promote user done!!")


@admin
def demote(bot: Bot, update: Update):
    logger.info("promote user...")
    chat_id, users = get_chat_id_and_users(bot, update)
    if not users:
        send_message(bot, chat_id, TIP_TEMPLATE + '进行管理员添加操作')

    for user in users:
        user.demote(bot, chat_id)

    logger.info("promote user done!!")


@admin
def is_admin(bot: Bot, update: Update):
    logger.info("checking user is manager...")
    chat_id, users = get_chat_id_and_users(bot, update)

    if not users:
        send_message(bot, chat_id, TIP_TEMPLATE + '进行管理员查询操作')

    for user in users:
        status = "管理员" if user.is_manager(bot, chat_id) else "普通用户"
        send_message(bot, chat_id, f'该用户的状态：{status}')

    logger.info("checking user is manager done!!")
