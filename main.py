from telegram import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonRequestUsers, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, MessageHandler, ContextTypes, filters
from mlangm import configure, translate as _
from os import getenv

from bot_logic.objects.user import User
from bot_logic.moduls.chat_manager import ChatManager


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_chat.id
    if context.user_data.get("user") is None:
        context.user_data["user"] = User(user_id=user)
        context.user_data["key_state"] = None
    await ChatManager.start(context=context, bot_update=update)
    

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ...

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ...

configure(default_lang='en', translations_path='bot_logic/language')

app = ApplicationBuilder().token(getenv("TOKEN")).build()

app.add_handlers(handlers={
    1: [
        MessageHandler(filters.TEXT & ~filters.COMMAND & filters.ChatType.PRIVATE, echo),
        CommandHandler("start", start, filters=filters.ChatType.PRIVATE),
        CallbackQueryHandler(button_callback)
    ]
})

print("BOT INFO: Im ready") # DEBUG
app.run_polling()