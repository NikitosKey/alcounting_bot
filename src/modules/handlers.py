import logging

from subprocess import check_output

from .customer import Customer
from .barman import Barman
from .admin import Admin
from .database import Database
from .user import User
from telegram import ForceReply, Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.constants import ParseMode
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
    database.create_tables()
    new_user = User(user.id, user.name, "customer")
    database.insert_user(new_user)
    await update.message.reply_text('Привет! Я бот Алкоучёт, жмакай на меню команд, чтобы увидеть доступные команды.')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    logging.getLogger(__name__).info(f'{update.message.from_user.id} use {update.message.text}')
    await update.message.reply_text("Пока не придумал, что сюда писать)")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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


async def menu(update: Update, context: CallbackContext) -> None:
    """
    This handler sends a menu with the inline buttons we pre-assigned above
    """
    logging.getLogger(__name__).info(f'{update.message.from_user.id} use {update.message.text}')

    database = Database()
    tg_user = update.effective_user
    current_user = database.get_user_by_id(tg_user.id)

    if current_user.type == "customer":
        await context.bot.send_message(
            update.message.from_user.id,
            Customer.CUSTOMER_MENU_TEXT,
            parse_mode=ParseMode.HTML,
            reply_markup=Customer.build_customer_menu(Customer)
        )

    elif current_user.type == "barman":
        await context.bot.send_message(
            update.message.from_user.id,
            Customer.CUSTOMER_MENU_TEXT,
            parse_mode=ParseMode.HTML,
            reply_markup=Barman.build_barman_menu(Barman)
        )

    elif current_user.type == "admin":
        await context.bot.send_message(
            update.message.from_user.id,
            Admin.ADMIN_MENU_TEXT,
            parse_mode=ParseMode.HTML,
            reply_markup=Admin.build_admin_menu(Admin)
        )
        pass
    else:
        logging.getLogger(__name__).error("incorrect user type")


async def button_callbacks(update: Update, context: CallbackContext) -> None:
    """
    This handler processes the inline buttons on the menu
    """

    database = Database()
    tg_user = update.effective_user
    current_user = database.get_user_by_id(tg_user.id)

    data = update.callback_query.data
    text = ''
    markup = None

    # Переписать под try except

    if current_user.type == "customer":
        text, markup = Customer.on_button_tap(Customer, data, tg_user.id)
        if markup is None:
            text, markup = Customer.back_to_customer_menu(Customer, data, tg_user.id)
    elif current_user.type == "barman":
        text, markup = Barman.on_button_tap(Barman, data, tg_user.id)
        if markup is None:
            text, markup = Barman.back_to_barman_menu(Barman, data, tg_user.id)
    elif current_user.type == "admin":
        text, markup = Admin.on_button_tap(Admin, data, tg_user.id)
        if markup is None:
            text, markup = Admin.back_to_admin_menu(Admin, data, tg_user.id)
    else:
        logging.getLogger(__name__).error("incorrect user type")

    logging.getLogger(__name__).info(f'{update.effective_user.id} Callbackdata: {data}')

    # Close the query to end the client-side loading animation
    await update.callback_query.answer()

    # Update message content with corresponding menu section
    await update.callback_query.edit_message_text(
        text,
        ParseMode.HTML,
        reply_markup=markup
    )
