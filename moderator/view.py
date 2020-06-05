# -*- coding: utf-8 -*-
from telegram import Update, Bot, ParseMode

from moderator.model.model import TelegramUser, TelegramChat
from moderator.permision import admin
from moderator.util import get_chat_id_and_users, logger, send_message

TIP_TEMPLATE = "回复消息或at用户名"

HELP = f"""
强大的黑名单机器人，精准定位，全球封杀🔞：

*限管理员操作*（{TIP_TEMPLATE}触发）:
 - /help: 查看帮助
 - /ban <用户>: 封禁某个用户，自动踢出所有机器人所在群组(管理)
 - /unban <用户>: 解除封禁某个用户(管理)
 - /id <用户>: 查询某用户封禁状态(管理)
"""


def start(bot: Bot, update: Update):
    message = update.message
    chat_id = message.chat.id
    bot.send_message(chat_id, HELP, parse_mode=ParseMode.MARKDOWN)


@admin
def ban(bot: Bot, update: Update):
    logger.info("ban user...")
    chat_id, users = get_chat_id_and_users(update)

    if not users:
        send_message(bot, chat_id, TIP_TEMPLATE + '进行踢出～')

    for user in users:
        try:
            if not user.user_id:
                send_message(bot, chat_id, '用户尚未发言，暂时无法踢出。')
                continue

            bot.kick_chat_member(chat_id, user_id=user.user_id)
            TelegramUser.set_status(user.user_id, False)
            send_message(bot, chat_id, f'已将该用户 {user.mention()} 全球封杀')
        except Exception as e:
            send_message(bot, chat_id, str(e))
    logger.info("ban user done!!!")


@admin
def unban(bot: Bot, update: Update):
    logger.info("unban user...")
    chat_id, users = get_chat_id_and_users(update)
    if not users:
        send_message(bot, chat_id, TIP_TEMPLATE + '进行解冻')
    for user in users:
        try:
            if not user.user_id:
                send_message(bot, chat_id, '未找到该用户，请联系管理员排查')
                continue
            bot.unban_chat_member(chat_id, user_id=user.user_id)
            TelegramUser.set_status(user.user_id, True)
            send_message(bot, chat_id, '知错能改，已将该用户解封！')
        except Exception as e:
            send_message(bot, chat_id, str(e))
    logger.info("unban user done!!!")


@admin
def get_status(bot: Bot, update: Update):
    logger.info("get_status user...")
    chat_id, users = get_chat_id_and_users(update)

    if not users:
        send_message(bot, chat_id, TIP_TEMPLATE + '进行用户状态查看')

    for user in users:
        status = "正常👏👏" if user.is_active else "封印中🔞🔞"
        send_message(bot, chat_id, f'该用户的状态：{status}')

    logger.info("get_status done!!")


def reply_handler(bot: Bot, update: Update):
    logger.info("handle user message...")
    t_user = update.message.from_user
    user, created = TelegramUser.get_or_create(t_user.id, t_user.username)
    logger.info(f"handle user done!! user: {user}, created: {created}")


def new_chat_members(bot: Bot, update: Update):
    logger.info("new chat members...")
    message = update.message
    for user in message.new_chat_members:
        if user.is_bot and user.id == bot.id:
            TelegramChat.add(message.chat.id, message.chat.title)
            logger.info(f"  find bot {user.full_name}, chat {message.chat.title} added")

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
