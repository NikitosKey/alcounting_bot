# общие функции, чтобы не засорять мэйн
import logging

from modules.customer import Customer
from modules.barman import Barman
from modules.admin import Admin
from modules.database import Database
from modules.user import User
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackContext


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
    database = Database()
    new_user = User(user.id, user.first_name, "customer")
    database.insert_user(new_user)
    await update.message.reply_text('Привет! Я бот. Нажимай на кнопку "/help" для получения подсказок по командам.')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    logging.getLogger(__name__).info(f'{update.message.from_user.id} use {update.message.text}')
    await update.message.reply_text("Помощь.")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)
    logging.getLogger(__name__).info(f'{update.message.from_user.id} wrote {update.message.text}')


async def menu(update: Update, context: CallbackContext) -> None:
    """
    This handler sends a menu with the inline buttons we pre-assigned above
    """
    logging.getLogger(__name__).info(f'{update.message.from_user.id} use {update.message.text}')

    database = Database()
    tg_user = update.effective_user
    current_user = database.get_user_by_id(tg_user.id)

    if current_user.type == "customer":
        await Customer.home_page(update, context)
    elif current_user.type == "barman":
        await Barman.home_page(update, context)
    elif current_user.type == "admin":
        await Admin.home_page(update, context)
    else:
        logging.getLogger(__name__).error("incorrect user type")
