# -*- coding: utf-8 -*-
import logging

from sqlalchemy import Column

from ..app import db

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


class TelegramUser(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
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
            return instance, True

    @classmethod
    def get(cls, user_id, username):
        instance = db.session.query(cls).filter_by(user_id=user_id, username=username).first()
        return instance

    @classmethod
    def get_by_username(cls, username):
        instance = db.session.query(cls).filter_by(username=username).first()
        return instance

    @classmethod
    def delete(cls, user_id, username):
        session = db.session
        session.query(cls).filter(user_id=user_id, username=username).delete()
        session.commit()
        return True

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
        return '<User %r>' % self.username
