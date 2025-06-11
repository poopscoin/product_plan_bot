from telegram import Update
from telegram.ext import ContextTypes
from mlangm import translate as _

from bot_logic.managers.moduls.profile import Profile
from bot_logic.managers.moduls.actions import ChatActions

class ReactionsManager(ChatActions):
    @classmethod
    async def r_write_plan(cls, update: Update, context: ContextTypes.DEFAULT_TYPE, profile: Profile):
        if update.message.text == _('buttons.new_plan.history_placeholder', profile.language):
            # Reaction to pressing the product list plug
            return await update.effective_chat.send_message(_('messages.system.history_placeholder_press', profile.language))
        elif update.message.text == _('buttons.new_plan.go_plan', profile.language):
            profile.building_product = None
            return await cls.redact_plan(update, context, profile)
        elif update.message.text == _('buttons.system.cancel', profile.language):
            profile.building_product.step_back()
            return await cls.watch_next(update, context, profile)
        else:
            return await cls.write_plan(update, context, profile, profile.last_plan_id is not None)

    @classmethod
    async def r_return_write(cls, update, context, profile):
        return await cls.return_write(update, context, profile)

    @classmethod
    async def r_menu(cls, update: Update, context: ContextTypes.DEFAULT_TYPE, profile: Profile):
        change_lang = {'ua': 'en', 'en': 'ua'}
        if update.message.text == _('buttons.menu.change_lang', change_lang[profile.language]):
            return await cls.change_lang(update, context)
        elif update.message.text == _('buttons.menu.new_list', profile.language):
            if profile.last_plan_id is not None:
                return await cls.return_write(update, context, profile)
            else:
                if profile.building_product:
                    profile.building_product = None
                return await cls.write_plan(update, context, profile, profile.last_plan_id is not None)

    @classmethod
    async def r_redact_plan(cls, update: Update, context: ContextTypes.DEFAULT_TYPE, profile: Profile):
        if update.message.text == _('buttons.new_plan.save', profile.language):
            if profile.get_plan(profile.last_plan_id-1) and profile.get_plan(profile.last_plan_id-1).products == profile.get_plan(profile.last_plan_id).products:
                # If the plan is the same as the previous one, do not save
                return await update.effective_chat.send_message(_('messages.new_plan.failed_save', profile.language))

            profile.new_plan(product_list=profile.get_plan(profile.last_plan_id).products)
            return await update.effective_chat.send_message(_('messages.new_plan.complete_save', profile.language))
        elif update.message.text == _('buttons.new_plan.new_product', profile.language):

            return await cls.write_plan(update, context, profile, True)

        elif update.message.text == _('buttons.new_plan.send', profile.language):
            ...

        elif update.message.text == _('buttons.new_plan.go_new', profile.language):
            profile.new_plan_crash()
            return await cls.write_plan(update, context, profile, False)
        else:
            # Dont understand user command
            ...

    reactions = {
        ChatActions.WRITE_PLAN: r_write_plan.__func__,
        ChatActions.RETURN_WRITE: r_return_write.__func__,
        ChatActions.REDACT_PLAN: r_redact_plan.__func__
    }

    @classmethod
    async def get_reaction(cls, update: Update, context: ContextTypes.DEFAULT_TYPE, profile: Profile): # type: ignore
        return await cls.reactions.get(profile.keyboard_state, cls.r_menu.__func__)(cls, update, context, profile)