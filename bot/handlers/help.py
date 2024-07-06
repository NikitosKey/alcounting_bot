import logging

from telegram import Update
from telegram.ext import ContextTypes


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    logging.getLogger(__name__).info(f'{update.message.from_user.id} use {update.message.text}')
    await update.message.reply_text("Пока не придумал, что сюда писать)")
