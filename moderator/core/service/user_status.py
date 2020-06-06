# -*- coding: utf-8 -*-
from telegram import Bot, Update

from moderator.core.service.welcome import TIP_TEMPLATE
from moderator.util.logger import logger
from moderator.util.message import send_message
from moderator.util.permision import admin
from moderator.util.util import get_chat_id_and_users


@admin
def get_status(bot: Bot, update: Update):
    logger.info("get_status user...")
    chat_id, users = get_chat_id_and_users(bot, update)

    if not users:
        send_message(bot, chat_id, TIP_TEMPLATE + '进行用户状态查看')

    for user in users:
        memo = "状态正常" if user.is_active else "已被全球拉黑"
        send_message(bot, chat_id, f'该用户 {user.mention()} {memo}({user.status_cn(bot, chat_id)})')

    logger.info("get_status done!!")
