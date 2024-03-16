# общие функции, чтобы не засорять мэйн
import logging

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    logging.getLogger(__name__).info(f'{update.message.from_user.id} use {update.message.text}')
    user = update.effective_user
    """await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )"""
    await update.message.reply_text('Привет! Я бот. Нажимай на кнопку "/help" для получения подсказок по командам.')



async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    logging.getLogger(__name__).info(f'{update.message.from_user.id} use {update.message.text}')
    await update.message.reply_text("Помощь.")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)
    logging.getLogger(__name__).info(f'{update.message.from_user.id} wrote {update.message.text}')
