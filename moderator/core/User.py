# -*- coding: utf-8 -*-
from dataclasses import dataclass


@dataclass
class User:
    user_id: int
    username: str
    is_active: bool

    def mention(self):
        if self.user_id:
            return f"[@{self.username}](tg://user?id={self.user_id})"
        else:
            return self.username
