# -*- coding: utf-8 -*-
import logging

from sqlalchemy import Column
from telegram.error import BadRequest

from ..app import db
from ..message import send_message

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


class AllChats:
    # 实时的最新群组列表
    available_chats = None

    @staticmethod
    def get_chats():
        session = db.session
        if not AllChats.available_chats:
            AllChats.available_chats = session.query(TelegramChat).all()
        return AllChats.available_chats

    @staticmethod
    def get_chat_ids():
        session = db.session
        if not AllChats.available_chats:
            AllChats.available_chats = session.query(TelegramChat).all()
        return [chat.chat_id for chat in AllChats.available_chats]

    @staticmethod
    def refresh_chats():
        session = db.session
        AllChats.available_chats = session.query(TelegramChat).all()

    @staticmethod
    def ban(bot, current_chat_id, user):
        for chat in AllChats.get_chats():
            chat_id = chat.chat_id
            try:
                if not user.user_id:
                    # 只有当前群组回复
                    chat_id == current_chat_id and send_message(bot, chat_id, '用户尚未发言，暂时无法踢出。')
                    continue

                logger.info(f"chat_id: {chat_id}, banning: {user}")
                bot.kick_chat_member(chat_id, user_id=user.user_id)
                TelegramUser.set_status(user.user_id, False)
                send_message(bot, chat_id, f'已将该用户 {user.mention()} 全球封杀')
            except BadRequest as e:
                logger.error(e, "bad chat id does not exist !!!!!")
            except Exception as e:
                send_message(bot, chat_id, str(e))

    @staticmethod
    def unban(bot, current_chat_id, user):
        for chat in AllChats.get_chats():
            chat_id = chat.chat_id
            try:
                if not user.user_id:
                    chat_id == current_chat_id and send_message(bot, chat_id, '未找到该用户，请联系管理员排查')
                    continue
                bot.unban_chat_member(chat_id, user_id=user.user_id)
                TelegramUser.set_status(user.user_id, True)
                send_message(bot, chat_id, '知错能改，已将该用户解封！')
            except Exception as e:
                send_message(bot, chat_id, str(e))


class TelegramUser(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, unique=True, nullable=False)
    username = db.Column(db.String(128), unique=True, nullable=False)
    status = Column(db.Boolean(), default=True)

    @classmethod
    def get_or_create(cls, user_id, username) -> ("TelegramUser", bool):
        session = db.session
        instance = session.query(cls).filter_by(user_id=user_id, username=username).first()
        if instance:
            return instance, False
        else:
            session.add(cls(user_id=user_id, username=username))
            session.commit()
            logger.info(f"User {user_id} {username} created!!!")
            return instance, True

    @classmethod
    def get(cls, user_id, username):
        instance = db.session.query(cls).filter_by(user_id=user_id, username=username).first()
        return instance

    @classmethod
    def get_by_username(cls, username):
        instance = db.session.query(cls).filter_by(username=username).first()
        return instance

    @staticmethod
    def is_active(username):
        instance = db.session.query(TelegramUser).filter_by(username=username).first()
        return instance and instance.status is True

    @staticmethod
    def set_status(user_id, status):
        user = TelegramUser.query.filter_by(user_id=user_id).first()
        if user:
            user.status = status
            db.session.commit()
            logger.info(f"{user} status updated to {user.status}")

    def __repr__(self):
        return f'<User {self.user_id}, {self.username}, {self.status}>'


class TelegramChat(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chat_id = db.Column(db.BigInteger, unique=True, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    status = Column(db.Boolean(), default=True)

    @classmethod
    def add(cls, chat_id, chat_name) -> ("TelegramChat", bool):
        session = db.session
        instance = session.query(cls).filter_by(chat_id=chat_id).first()
        if instance:
            result = instance, False
        else:
            instance = session.add(cls(chat_id=chat_id, name=chat_name, status=True))
            session.commit()
            result = instance, True
            logger.info(f"chat({chat_id},{chat_name}) added!")

        # 更新所有的listener
        AllChats.refresh_chats()

        return result

    @staticmethod
    def remove(chat_id) -> bool:
        # 查询所有机器人所在群组
        session = db.session
        session.query(TelegramChat).filter(TelegramChat.chat_id == chat_id).delete()
        session.commit()

        # 更新所有的listener
        AllChats.refresh_chats()

        return True
