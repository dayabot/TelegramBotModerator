# -*- coding: utf-8 -*-
import logging

from telegram import ParseMode

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def send_message(bot, chat_id, msg, parse_mode=ParseMode.MARKDOWN):
    logger.info(f"sending msg {chat_id}, {msg}")
    bot.send_message(chat_id, msg, parse_mode=parse_mode)
