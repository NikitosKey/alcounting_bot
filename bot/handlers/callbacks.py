""" Callbacks handler. """

import logging
from datetime import datetime

from telegram import Update, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import CallbackContext

from bot.database import Database, User, Product, Order
from bot.users import Customer, Barman, Admin


async def callback_handler(update: Update, context: CallbackContext) -> None:
    """
    This handler processes the inline buttons on the menu
    """

    db = Database()
    tg_user = update.effective_user
    current_user = db.get_user_by_id(tg_user.id)

    data = update.callback_query.data
    text = "Err0r: message text is empty."
    markup = None

    on_button_tap(data, tg_user.id)

    logging.getLogger(__name__).info(
        "{} Callbackdata: {}".format(update.effective_user.id, data)
    )

    # Close the query to end the client-side loading animation
    await update.callback_query.answer()

    # Update message content with corresponding menu section
    await update.callback_query.edit_message_text(
        text, ParseMode.HTML, reply_markup=markup
    )


def on_button_tap(data, tg_user_id) -> (str, InlineKeyboardMarkup):
    text = ""
    markup = None

    db = Database()
    my_products: list[Product] = db.get_all_products()
    product_names = [Product.get_name() for Product in my_products]

    my_orders: list[Order] = db.get_all_orders()
    order_dates = [str(Order.get_order_date()) for Order in my_orders]

    customer = Customer()
    barman = Barman()
    admin = Admin()

    return text, markup
