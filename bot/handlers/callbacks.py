import logging

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CallbackContext

from bot.database import Database
from bot.users import Customer, Barman, Admin


async def callbacks(update: Update, context: CallbackContext) -> None:
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
