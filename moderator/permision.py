# -*- coding: utf-8 -*-

from telegram.chatmember import ChatMember


def admin(f):
    def wrapper(bot, update):
        message = update.message
        chat_id = message.chat.id
        user_id = message.from_user.id
        chat_member = bot.get_chat_member(chat_id, user_id)

        if chat_member.status not in (ChatMember.CREATOR, ChatMember.ADMINISTRATOR):
            update.message.reply_text("对不起, 您无管理员权限")
            return

        f(bot, update)

    return wrapper
