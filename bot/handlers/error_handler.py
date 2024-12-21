"""
This module contains the error handler for the bot.
"""

import logging
from telegram import Update
from telegram.ext import CallbackContext


async def error_handler(update: Update, context: CallbackContext) -> None:
    """
    Log the error caused by an update.
    """
    logging.error(
        msg="Exception while handling an update:" + str(update.effective_user.id if update else "None"),
        exc_info=context.error,
    )
