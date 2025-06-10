from functools import wraps
from telegram.ext import ContextTypes
from telegram import Update, Message
from mlangm import translate as _

from .moduls.profile import Profile
from .moduls.actions import ChatActions
from .moduls.reactions import ReactionsManager

def last_message(func):
    @wraps(func)
    async def wrapper(cls, update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        message = await func(cls, update=update, context=context, *args, **kwargs)
        if isinstance(message, Message):
            context.user_data['profile'].message = message
            print(f"[LOG]->|{context.user_data['profile'].id}|: {message.text}")
        return message
    return wrapper

class ChatManager(ChatActions):

    @classmethod
    async def start(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not context.user_data.get('profile'):
            context.user_data['profile'] = Profile(id=update.effective_user.id)
            profile = context.user_data['profile']
            profile.language = update.effective_user.language_code

            await update.effective_chat.send_message(_('start', profile.language))
            profile.message = await cls.menu(update, context)
            return profile.message
        else:
            return await cls.action(update, context)

    @classmethod
    @last_message
    async def action(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):
        profile: Profile = context.user_data.get('profile', False)
        if not profile:
            return await cls.start(update, context)

        if update.message.text == _('buttons.system.back', profile.language) and profile.keyboard_state != ChatActions.MENU:
            return await cls.menu(update, context)
        
        return await ReactionsManager.get_reaction(update, context, profile)

    @classmethod
    async def inline_callback(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):
        print(update.callback_query.data)