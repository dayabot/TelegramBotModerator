# -*- coding: utf-8 -*-

from telegram.chatmember import ChatMember

from moderator.model.model import TelegramChat, AllChats


def admin(f):
    def wrapper(bot, update):
        message = update.message
        chat_id = message.chat.id
        user_id = message.from_user.id
        chat_member = bot.get_chat_member(chat_id, user_id)

        # 增加当前用户组至数据库
        if chat_id not in AllChats.get_chat_ids():
            TelegramChat.add(message.chat.id, message.chat.title)

        if chat_member.status not in (ChatMember.CREATOR, ChatMember.ADMINISTRATOR):
            update.message.reply_text("对不起, 您无管理员权限")
            return

        f(bot, update)

    return wrapper
