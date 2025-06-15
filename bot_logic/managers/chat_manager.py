from telegram.ext import ContextTypes
from telegram import Update
from mlangm import translate as _

from bot_logic.utils.decorators import last_message
from .moduls.profile import Profile
from .moduls.actions import ChatActions
from .moduls.reactions import ReactionsManager

class ChatManager(ChatActions):

    @classmethod
    def get_another_profile(cls, context: ContextTypes.DEFAULT_TYPE, user_id: int) -> Profile:
        profile_list = context.bot_data['profile_list']
        to_profile = profile_list.get(user_id)
        if not to_profile:
            profile_list[user_id] = Profile(id=user_id)
        return profile_list[user_id]

    @classmethod
    async def start(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):
        profile_list = context.bot_data['profile_list']
        if not context.user_data.get('profile'):
            context.user_data['profile'] = cls.get_another_profile(context=context, user_id=update.effective_user.id)
            profile = context.user_data['profile']
            profile_list[update.effective_user.id] = profile
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