import logging

from bot.users.customer import Customer
from bot.users.barman import Barman
from bot.users.admin import Admin
from bot.database.database import Database

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CallbackContext


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
