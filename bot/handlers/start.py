import logging
import os.path

from telegram import Update
from telegram.ext import ContextTypes

from bot.database.database import Database, User


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    logging.getLogger(__name__).info(f'{update.message.from_user.id} use {update.message.text}')
    user = update.effective_user
    Db = Database()

    if not os.path.exists(Db.database_folder):
        os.makedirs(Db.database_path, exist_ok=True)

    database = Database()
    database.create_tables()

    new_user = User(user.id, user.name, "customer")
    database.insert_user(new_user)

    await update.message.reply_text('Привет! Я бот Алкоучёт, жмакай на меню команд, чтобы увидеть доступные команды.')