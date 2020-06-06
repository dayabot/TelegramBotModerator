# -*- coding: utf-8 -*-
from telegram import Bot, Update, ParseMode

from moderator.util.logger import logger

TIP_TEMPLATE = "回复消息或at用户名"

HELP = f"""
强大的黑名单机器人，精准定位，全球封杀🔞：

*限管理员操作*（{TIP_TEMPLATE}触发）:
  - /help: 查看帮助
  - /ban <用户>: 封禁某个用户，自动踢出所有机器人所在群组(管理)
  - /unban <用户>: 解除封禁某个用户(管理)
  - /addManager <用户>: 增加管理员(管理)
  - /removeManager <用户>: 删除管理员(管理)
  - /id <用户>: 查询某用户当前状态(管理)
"""


def start(bot: Bot, update: Update):
    message = update.message
    chat_id = message.chat.id
    logger.info(f"hello, current_chat: {chat_id}")
    bot.send_message(chat_id, HELP, parse_mode=ParseMode.MARKDOWN)
