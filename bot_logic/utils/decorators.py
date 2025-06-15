from functools import wraps
from telegram.ext import ContextTypes
from telegram import Update, Message

def last_message(func):
    @wraps(func)
    async def wrapper(cls, update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        message = await func(cls, update=update, context=context, *args, **kwargs)
        if isinstance(message, Message):
            context.user_data['profile'].message = message
            print(f"[LOG]->|{context.user_data['profile'].id}|: {message.text}")
        return message
    return wrapper

# def reset_page(func):
#     @wraps(func)
#     async def wrapper(*args, **kwargs):
#         return await func(*args, **kwargs)
#     return wrapper




