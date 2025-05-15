from telegram.helpers import escape_markdown
from telegram.ext import ContextTypes
from telegram import Update
from mlangm import translate as _

from ..objects.keyboard import *

def em(text: str, entity_type: str = None, version: int = 2) -> str: return escape_markdown(text=text, version=version, entity_type=entity_type)

class ChatActions:
    ...


class ChatManager(ChatActions):

    @classmethod
    def start(cls, *, context: ContextTypes.DEFAULT_TYPE, bot_update: Update):
        
        return bot_update.message.reply_text(
            text=(
                f'*{em(_(key='start', lang='en'))}*\n'
                '\n'
                f'*{em(_(key='start', lang='ua'))}*'
            ),
            reply_markup=TechnicalKeyboard.choise_lang(),
            parse_mode="MarkdownV2"
        )

    @classmethod
    async def action(cls, *, context: ContextTypes.DEFAULT_TYPE, bot_update: Update):
        user = context.user_data

