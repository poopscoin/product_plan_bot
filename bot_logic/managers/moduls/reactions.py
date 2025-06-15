from telegram import Update
from telegram.ext import ContextTypes
from mlangm import translate as _

from telegram import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonRequestUsers

from bot_logic.managers.moduls.profile import Profile
from bot_logic.managers.moduls.actions import ChatActions

class ReactionsManager(ChatActions):
    @classmethod
    async def r_write_plan(cls, update: Update, context: ContextTypes.DEFAULT_TYPE, profile: Profile):
        """React to user submitted values ​​for a new plan"""
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
        """Reacting to a user's response about returning to writing a previous unfinished plan"""
        return await cls.return_write(update, context, profile)

    @classmethod
    async def r_menu(cls, update: Update, context: ContextTypes.DEFAULT_TYPE, profile: Profile):
        """Respond to keyboard key presses for the main menu."""
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
        """Respond to keyboard key presses for plan redaction."""
        if update.message.text == _('buttons.new_plan.save', profile.language):
            if profile.get_plan(profile.last_plan_id-1) and profile.get_plan(profile.last_plan_id-1).products == profile.get_plan(profile.last_plan_id).products:
                # If the plan is the same as the previous one, do not save
                return await update.effective_chat.send_message(_('messages.new_plan.failed_save', profile.language))

            profile.new_plan(product_list=profile.get_plan(profile.last_plan_id).products)
            return await update.effective_chat.send_message(_('messages.new_plan.complete_save', profile.language))
        elif update.message.text == _('buttons.new_plan.new_product', profile.language):

            return await cls.write_plan(update, context, profile, True)

        elif update.message.text == _('buttons.new_plan.send', profile.language):

            return await cls.select_contact(update, context, profile)

        elif update.message.text == _('buttons.new_plan.go_new', profile.language):
            profile.new_plan_crash()

            return await cls.write_plan(update, context, profile, False)

    @classmethod
    async def r_select_contact(cls, update: Update, context: ContextTypes.DEFAULT_TYPE, profile: Profile):
        """Respond to keyboard key presses for selecting a contact."""
        if update.message.text == _('buttons.system.cancel', profile.language):
            return cls.BACK
        elif update.message.text in cls.NAVIGATIONS:
            profile.page = cls.NAVIGATIONS[update.message.text]
            return await cls.select_contact(update=update, context=context, profile=profile)
        elif update.message.users_shared:
            shared_user = update.message.users_shared.users[0]
            if profile.contacts.get(shared_user.user_id):
                return await update.effective_chat.send_message(
                    _('messages.contacts.already', profile.language, name=profile.contacts[shared_user.user_id]),
                    parse_mode="HTML"
                )

            last_name = shared_user.last_name if shared_user.last_name else ""

            profile.add_contact(shared_user.user_id, fr"{shared_user.first_name} {last_name}".strip())
            edit_message = _('messages.contacts.success_add', profile.language, name=fr"{shared_user.first_name} {last_name}".strip())
            return await cls.select_contact(update, context, profile, edit_message=edit_message)
            # try: chat = await context.bot.get_chat(shared_user.user_id)
            # except: chat = "Not acces"
            # print("[ACTIVE DEBUGER ~/.76]", update.message.users_shared.users[0]) # NOT WORKING YET
            # print("tewsst = ", chat)
        else:
            if not update.message.text or not update.message.text.strip():
                return await update.effective_chat.send_message(_('messages.contacts.wrong', profile.language))

            contact_num = ''.join(с for с in update.message.text if с.isdigit())
            if contact_num: contact_num = int(contact_num) - 1

            if contact_num is None:
                return await update.effective_chat.send_message(_('messages.contacts.wrong', profile.language))
            user_id = profile.get_contact(contact_num)
            if user_id is None:
                return await update.effective_chat.send_message(_('messages.contacts.no_contacts', profile.language))
            profile.keyboard_state = cls.REDACT_PLAN
            # return await profile.keyboard_state(cls, update, context, profile)
            result = await profile.send_plan(update=Update, context=context, index=contact_num)
            

    BACK = "back"

    reactions = {
        ChatActions.WRITE_PLAN: r_write_plan.__func__,
        ChatActions.RETURN_WRITE: r_return_write.__func__,
        ChatActions.REDACT_PLAN: r_redact_plan.__func__,
        ChatActions.SELECT_CONTACT: r_select_contact.__func__
    }

    @classmethod
    async def get_reaction(cls, update: Update, context: ContextTypes.DEFAULT_TYPE, profile: Profile):
        result = await cls.reactions.get(profile.keyboard_state, cls.r_menu.__func__)(cls, update, context, profile)
        # Not reliable, needs to be redone!
        if result == cls.BACK:
            return await profile.old_keyboard_state(cls, update, context, profile)
        # Not reliable, needs to be redone!
        return result



