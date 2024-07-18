""" Command handler for the admin to write commands to the server and monitor its status """

import logging
from subprocess import check_output

from telegram import Update

from bot.database import Database


async def cmd(update: Update):
    """Send the server administrator commands to the server and get the result"""
    logging.getLogger(__name__).info(
        update.message.from_user.id, "wrote", update.message.text
    )
    database = Database()
    tg_user = update.effective_user
    current_user = database.get_user_by_id(tg_user.id)
    if current_user.type == "admin":
        command = update.message.text.split(" ")
        try:  # если команда невыполняемая - check_output выдаст exception
            await update.message.reply_text(check_output(command).decode())
        except ValueError:
            await update.message.reply_text("Invalid input")  # если команда некорректна
