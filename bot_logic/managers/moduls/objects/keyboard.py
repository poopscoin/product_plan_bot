from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from typing import Optional, Union, Dict, List
from abc import ABC, abstractmethod

class Keyboard(ABC):
    def __init__(self, *, markup: Optional[Union[List, Dict]] = None):
        # self._markup = markup if isinstance(markup, dict) else {"main": markup} if isinstance(markup, list) else {}
        self._markup: Dict[str, List]
        if isinstance(markup, dict):
            self._markup = markup
        elif isinstance(markup, list):
            self._markup = {"main": markup}
        else:
            self._markup = {}

    def check(self, *, key: str) -> bool:
        return key in self._markup

    def main(self, *, value: KeyboardButton | InlineKeyboardButton | list) -> dict:
        self._markup["main"] = value if isinstance(value, list) else [value]
        return self._markup

    def append(self, *, key: str, value: KeyboardButton | InlineKeyboardButton | list) -> dict:
        self._markup[key] = value if isinstance(value, list) else [value]
        return self._markup

    def pop(self, *, key: str) -> list | None:
        return self._markup.pop(key, None)

    def get(self, *, key: str) -> list | None:
        return self._markup.get(key, None)

    def take(self) -> dict:
        return self._markup

    def __call__(self) -> ReplyKeyboardMarkup | InlineKeyboardMarkup:
        return self._collect()

    @abstractmethod
    def _collect(self):
        pass

class ReplyKeyboard(Keyboard):
    keyboard_type = ReplyKeyboardMarkup
    
    def __init__(self, *, markup: Optional[Union[List, Dict]] = None):
        super().__init__(markup=markup)

    def _collect(self) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(keyboard=[row for markup in self._markup.values() for row in markup], resize_keyboard=True)

class InLineKeyboard(Keyboard):
    keyboard_type = InlineKeyboardMarkup

    def __init__(self, *, markup: Optional[Union[List, Dict]] = None):
        super().__init__(markup=markup)

    def _collect(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[row for markup in self._markup.values() for row in markup])