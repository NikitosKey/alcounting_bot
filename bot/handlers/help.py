""" Help handler. """

import logging

from telegram import Update
from telegram.ext import ContextTypes


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    logging.getLogger(__name__).info(
        "{} use {}".format(update.message.from_user.id, update.message.text)
    )
    await update.message.reply_text("Пока не придумал, что сюда писать)")
