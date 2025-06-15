from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, MessageHandler, filters
from mlangm import configure, translate as _
from os import getenv

from bot_logic.managers.chat_manager import ChatManager

configure(default_lang='en', translations_path='bot_logic/language')

app = ApplicationBuilder().token(getenv("TOKEN")).build()

app.bot_data['profile_list'] = {}

app.add_handlers(handlers={
    1: [
        MessageHandler((filters.TEXT | filters.StatusUpdate.USERS_SHARED) & ~filters.COMMAND & filters.ChatType.PRIVATE, ChatManager.action),
        CommandHandler("start", ChatManager.start, filters=filters.ChatType.PRIVATE),
        CallbackQueryHandler(ChatManager.inline_callback)
    ]
})

print("BOT INFO: Im ready") # DEBUG
app.run_polling()