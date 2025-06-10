from re import sub, escape
from telegram.ext import ContextTypes
from telegram import Update
from mlangm import translate as _

from .profile import Profile
from .objects.keyboard import ReplyKeyboard, InLineKeyboard
from .objects.markups import *
from .objects.plan import Plan
from .objects.products import ProductBuilder, Product

def em(text: str) -> str: return sub(rf"([{escape(r"[]()>#+-=|{}.!\\")}])", r"\\\1", text)

def emoji_number(number: int) -> str:
    emoji = {
        '0': '0️⃣',
        '1': '1️⃣',
        '2': '2️⃣',
        '3': '3️⃣',
        '4': '4️⃣',
        '5': '5️⃣',
        '6': '6️⃣',
        '7': '7️⃣',
        '8': '8️⃣',
        '9': '9️⃣',
    }
    return ''.join(emoji[char] for char in str(number))
def smart_number(number: float | int) -> float | int:
    return int(number) if isinstance(number, float) and number.is_integer() else number

class ChatActions:
    # Query callbacks
    CHANGE_LANG = 'change_lang'

    # States

    # Static messages/variables
    @staticmethod
    def __first_choise_lang():
        return (
                f'*{em(_(key='start', lang='en'))}*\n'
                '\n'
                f'*{em(_(key='start', lang='ua'))}*'
            )

    @classmethod
    async def menu(cls, update: Update, context: ContextTypes.DEFAULT_TYPE, **kwargs):
        profile: Profile = context.user_data['profile']
        profile.keyboard_state = cls.MENU
        lang = profile.language

        keyboard = ReplyKeyboard(markup=MenuMarkup.main_menu(lang))
        if profile.notif:
            keyboard.append(key='notification', value=MenuMarkup.notification_button(lang))
        
        return await update.effective_chat.send_message(text=_('messages.menu', lang),reply_markup=keyboard())
    MENU = menu.__func__

    @classmethod
    async def change_lang(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):
        profile: Profile = context.user_data['profile']
        profile.keyboard_state = cls.MENU
        changed_lang = profile.change_lang()

        keyboard = ReplyKeyboard(markup=MenuMarkup.main_menu(changed_lang))
        if profile.notif:
            keyboard.append(key='notification', value=MenuMarkup.notification_button(changed_lang))

        return await update.effective_chat.send_message(text=_('messages.changed_lang', changed_lang), reply_markup=keyboard())
    CHANGE_LANG = change_lang.__func__

    @classmethod
    async def return_write(cls, update: Update, context: ContextTypes.DEFAULT_TYPE, profile: Profile):
        profile.keyboard_state = cls.RETURN_WRITE
        if update.message.text == _('buttons.new_plan.continue', profile.language):
            profile.keyboard_state = cls.WRITE_PLAN
            if profile.building_product:
                return await cls.watch_next(update=update, context=context, profile=profile, plan_present=True)
            else:
                return await cls.redact_plan(update=update, context=context, profile=profile)
        elif update.message.text == _('buttons.new_plan.go_new', profile.language):
            profile.new_plan_crash()
            return await cls.write_plan(update=update, context=context, profile=profile)
        else:
            # If the user has not finished filling out the previous plan
            profile.keyboard = ReplyKeyboard(markup=WritePlanMarkup.continue_plan(profile.language))

            message = _('messages.new_plan.continue', profile.language)

        return await update.effective_chat.send_message(
            text=message,
            reply_markup=profile.keyboard(),
            parse_mode="HTML"
        )
    RETURN_WRITE = return_write.__func__

    @classmethod
    async def write_plan(cls, update: Update, context: ContextTypes.DEFAULT_TYPE, profile: Profile, plan_present: bool = False):

        if profile.keyboard_state != cls.WRITE_PLAN and profile.building_product == None:
            keyboard = ReplyKeyboard(markup=WritePlanMarkup.get_next_markup(ProductBuilder.NAME, profile.language, plan_present,
                                                                            product_history=profile.product_history))
            message = _('messages.new_plan.'+ProductBuilder.NAME, profile.language)
        else:
            next_step, another_values = profile.building_plan(update.message.text)

            if next_step == ProductBuilder.COMPLETE:
                plan = profile.get_plan(profile.last_plan_id) if plan_present else profile.new_plan()
                plan.add_product(profile.building_product.product)
                profile.building_product = None

                return await cls.redact_plan(update=update, context=context, profile=profile, plan=plan)
            else:
                keyboard = ReplyKeyboard(markup=WritePlanMarkup.get_next_markup(next_step, profile.language, plan_present))
                message = _(f'messages.new_plan.{next_step}', profile.language, **another_values)
        profile.keyboard_state = cls.WRITE_PLAN

        return await update.effective_chat.send_message(
            text=message,
            reply_markup=keyboard(),
            parse_mode="HTML"
        )
    # Subfunction for write_plan, see next value
    @classmethod
    async def watch_next(cls, update: Update, context: ContextTypes.DEFAULT_TYPE, profile: Profile, plan_present: bool = False):
        plan_present = plan_present or profile.last_plan_id is not None
        next_step = profile.building_product.next()
        keyboard = ReplyKeyboard(markup=WritePlanMarkup.get_next_markup(next_step, profile.language, plan_present,
                                                                            product_history=profile.product_history))
        message = _(f'messages.new_plan.{next_step}', profile.language, **profile.building_product.values)
        return await update.effective_chat.send_message(
            text=message,
            reply_markup=keyboard(),
            parse_mode="HTML"
        )
    WRITE_PLAN = write_plan.__func__

    @classmethod
    async def redact_plan(cls, update: Update, context: ContextTypes.DEFAULT_TYPE, profile: Profile, plan: Plan = None):
        profile.keyboard_state = cls.REDACT_PLAN
        plan = plan or profile.get_plan(profile.last_plan_id)
        keyboard = ReplyKeyboard(markup=WritePlanMarkup.redact_plan(profile.language))
        
        message = f'{_('messages.new_plan.title_plan', profile.language, title_plan=plan.title)}\n\n'
        for i, product in plan.products.items():
            message += f'{emoji_number(i+1)} {product.name} {smart_number(product.count)}{product.type}\n'
        message += f'\n{_('messages.new_plan.footer_plan', profile.language, count=plan.count)}'

        return await update.effective_chat.send_message(
            text=message,
            reply_markup=keyboard(),
            parse_mode="HTML"
        )
    REDACT_PLAN = redact_plan.__func__

            




            


