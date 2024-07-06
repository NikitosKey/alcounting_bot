import logging
from subprocess import check_output

from telegram import Update
from telegram.ext import ContextTypes

from bot.database import Database


async def cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    # await update.message.reply_text(update.message.text)
    logging.getLogger(__name__).info(f'{update.message.from_user.id} wrote {update.message.text}')
    database = Database()
    tg_user = update.effective_user
    current_user = database.get_user_by_id(tg_user.id)
    if current_user.type == "admin":
        comand = (update.message.text).split(" ")
        try:  # если команда невыполняемая - check_output выдаст exception
            await update.message.reply_text(check_output(comand).decode())
        except:
            await update.message.reply_text("Invalid input")  # если команда некорректна
