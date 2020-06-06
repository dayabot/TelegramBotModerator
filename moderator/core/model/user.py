# -*- coding: utf-8 -*-
import logging
from dataclasses import dataclass

from telegram import Bot, ChatMember

from moderator.util.message import send_message
from moderator.util.permision import telegram_atom

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

CHAT_STATUS_D = {
    ChatMember.ADMINISTRATOR: '群管理员',
    ChatMember.CREATOR: '群主',
    ChatMember.KICKED: '被踢出该群，无法自行加入',
    ChatMember.LEFT: '不在该群中',
    ChatMember.MEMBER: '群成员',
    ChatMember.RESTRICTED: '被限制'
}


@dataclass
class User:
    user_id: int
    username: str
    is_active: bool

    @telegram_atom
    def promote(self, bot: Bot, chat_id):
        bot.promote_chat_member(
            chat_id,
            self.user_id,
            can_change_info=True,
            # can_post_messages=False,
            # can_edit_messages=False,
            can_delete_messages=True,
            can_invite_users=True,
            can_restrict_members=True,
            can_pin_messages=True,
            can_promote_members=True
        )

        send_message(bot, chat_id, f'已将该用户 {self.mention()} 设置为管理员')

    @telegram_atom
    def demote(self, bot: Bot, chat_id):
        bot.promote_chat_member(chat_id, self.user_id, can_change_info=False, can_post_messages=False,
                                can_edit_messages=False, can_delete_messages=False, can_invite_users=False,
                                can_restrict_members=False, can_pin_messages=False, can_promote_members=False)
        send_message(bot, chat_id, f'已将该用户 {self.mention()} 设置为普通用户')

    @telegram_atom
    def ban(self, bot: Bot, chat_id):
        bot.kick_chat_member(chat_id, user_id=self.user_id)
        send_message(bot, chat_id, f'将该用户 {self.mention()} 全球封杀({self.status_cn(bot, chat_id)})')

    @telegram_atom
    def unban(self, bot: Bot, chat_id):
        # 只有当 kicked 的情况才做解封
        if self.status(bot, chat_id) == ChatMember.KICKED:
            bot.unban_chat_member(chat_id, user_id=self.user_id)
        send_message(bot, chat_id, f'已将该用户 {self.mention()} 从全局黑名单中移除({self.status_cn(bot, chat_id)})。')

    def is_manager(self, bot: Bot, chat_id: int):
        return self.user_id in User.get_chat_admin_ids(bot, chat_id)

    @staticmethod
    def get_chat_admin_ids(bot: Bot, chat_id):
        try:
            user_ids = [t_bot.id for t_bot in bot.get_chat_administrators(chat_id)]
            logger.info(f"Fetch admins for chat({chat_id}): {user_ids}")
            return user_ids
        except Exception as e:
            logger.error(e, f"{str(e)}")
            return []

    def mention(self):
        if self.user_id:
            return f"[@{self.username}](tg://user?id={self.user_id})"
        else:
            return self.username

    @classmethod
    def build_user_from_db(cls, user):
        return cls(user_id=user.user_id, username=user.username, is_active=user.status)

    def status(self, bot: Bot, chat_id):
        chat_member = bot.get_chat_member(chat_id, self.user_id)
        return chat_member.status

    def status_cn(self, bot: Bot, chat_id):
        return CHAT_STATUS_D[self.status(bot, chat_id)]

    def __str__(self):
        return f"<User {self.user_id}, {self.username}, {self.is_active}>"
