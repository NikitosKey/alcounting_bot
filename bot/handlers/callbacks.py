""" Callbacks handler. """

import logging
from datetime import datetime

from telegram import Update, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import CallbackContext

from bot.database import Database, User, Product, Order
from bot.users import Customer, Barman, Admin


async def callbacks(update: Update, context: CallbackContext) -> None:
    """
    This handler processes the inline buttons on the menu
    """

    db = Database()
    tg_user = update.effective_user
    current_user = db.get_user_by_id(tg_user.id)

    data = update.callback_query.data
    text = ""
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

    # Обработка кнопок Барной карты
    customer.show_products_menu(data, tg_user_id)

    if data[6:] in product_names and data[:6] == "shown_":
        logging.getLogger(__name__).info(f"{tg_user_id} watch for the {data[6:]}")
        db = Database()
        product = db.get_product_by_name(data[6:])
        text = f"{product.name}\nОписание:\n{product.description}\nЦена:\n{product.price}руб."
        markup = Customer.build_show_product_info_menu(Customer, (data[1:]))

    # Обработка кнопок для создания заказа
    if data == customer.MAKE_ORDER_BUTTON:
        logging.getLogger(__name__).info(
            f"{tg_user_id} press the MAKE_ORDER_BUTTON or return to MAKE_ORDER menu"
        )
        text = Customer.MAKE_ORDER_TEXT
        markup = Customer.build_make_orders_menu(customer)

    if (data[6:] in product_names and data[:6] == "chose_") or (
        data[5:] in product_names and data[:5] == "hown_"
    ):
        if data[:5] == "hown_":
            data = "s" + data
        logging.getLogger(__name__).info(f"{tg_user_id} chosen the {data}")
        text = f"Выбран {data[6:]}.\nПодтвердите ваш заказ."
        print(str("next" + data)[:10])
        markup = Customer.build_pre_approve_order_menu(customer, str("next" + data))

    if data[10:] in product_names and (
        data[:10] == "nextchose_" or data[:10] == "nextshown_"
    ):
        order = Order(
            str(datetime.datetime.now()), data[10:], tg_user_id, None, "размещён"
        )
        db = Database()
        db.insert_order(order)
        text = f"Заказ оформлен!\nВремя заказа: {order.date[:-7]}\nПродукт:\n{order.product}\nId покупателя:\n{order.customer_id}"
        markup = customer.build_approve_order_menu(data[4:])

    # Обработка кнопок просмотра заказов
    if data == Customer.SHOW_ORDERS_BUTTON:
        logging.getLogger(__name__).info(
            f"{tg_user_id} press the SHOW_ORDERS_BUTTON or return to SHOW_ORDERS menu"
        )
        text = Customer.SHOW_ORDERS_TEXT
        markup = customer.build_show_orders_menu(tg_user_id)

    if data[6:] in order_dates and data[:6] == "shown_":
        logging.getLogger(__name__).info(f"{tg_user_id} watch for the {data}")
        db = Database()
        order = db.get_order_by_date(data[6:])
        user = db.get_user_by_id(order.customer_id)
        bar = db.get_user_by_id(order.barman_id)
        if bar is None:
            bar = User(None, None, "barman")
        text = f"""Заказ от: {order.date[:-7]}\nПродукт: {order.product}\nИмя покупателя: {user.name}\nИмя бармена: {bar.name}\nСтатус: {order.status}"""
        markup = customer.build_show_order_info_menu()

    if data == barman.QUEUE_BUTTON:
        logging.getLogger(__name__).info(
            f"{tg_user_id} press the QUEUE_BUTTON or return to the QUEUE menu"
        )
        text = f"{barman.QUEUE_BUTTON}"
        markup = barman.build_queue_menu()

    if data[6:] in order_dates and data[:6] == "chose_":
        logging.getLogger(__name__).info(f"{tg_user_id} watch for the {data}")
        db = Database()
        order = db.get_order_by_date(data[6:])
        user = db.get_user_by_id(order.customer_id)
        bar = db.get_user_by_id(order.barman_id)
        if bar is None:
            bar = User(None, None, "barman")
        text = f"""
        Заказ от: {order.date[:-7]}\nПродукт: {order.product}\nИмя покупателя: {user.name}\nИмя бармена: {bar.name}\nСтатус: {order.status}"""
        markup = barman.build_pre_complete_order_menu(str("next" + data))

    if data[10:] in order_dates and data[:10] == "nextchose_":
        db = Database()
        order = db.get_order_by_date(data[10:])
        order.set_order_barman_id(tg_user_id)
        order.set_order_status("завершён")
        db.update_order(order)
        user = db.get_user_by_id(order.customer_id)
        bar = db.get_user_by_id(order.barman_id)
        if bar is None:
            bar = User(None, None, "barman")
        text = f"""Заказ завершён!!!\nОт: {order.date[:-7]}\nПродукт: {order.product}\nИмя покупателя: {user.name}\nИмя бармена: {bar.name}\nСтатус: {order.status}"""
        markup = barman.build_complete_order_menu()

    if data == admin.TO_CUSTOMER_MENU_BUTTON_TEXT:
        logging.getLogger(__name__).info(
            f"{tg_user_id} press the TO_CUSTOMER_MENU_BUTTON"
        )
        text = admin.CUSTOMER_MENU_TEXT
        markup = admin.build_customer_menu()

    if data == admin.TO_BARMAN_MENU_BUTTON_TEXT:
        logging.getLogger(__name__).info(
            f"{tg_user_id} press the TO_BARMAN_MENU_BUTTON"
        )
        text = admin.CUSTOMER_MENU_TEXT
        markup = admin.build_barman_menu(admin)

    if data == admin.USERS_TABLE_BUTTON_TEXT:
        logging.getLogger(__name__).info(f"{tg_user_id} press the USERS_TABLE_BUTTON")
        text = admin.USERS_TABLE_TEXT
        markup = admin.build_users_table_menu(admin)

    if data == admin.MENU_TABLE_BUTTON_TEXT:
        logging.getLogger(__name__).info(f"{tg_user_id} press the MENU_TABLE_BUTTON")
        text = admin.MENU_TABLE_BUTTON_TEXT
        markup = admin.build_products_table_menu(admin)

    if data == admin.ORDERS_TABLE_BUTTON_TEXT:
        logging.getLogger(__name__).info(f"{tg_user_id} press the ORDERS_TABLE_BUTTON")
        text = admin.ORDERS_TABLE_BUTTON_TEXT
        markup = admin.build_orders_table_menu("admin")

    if db.get_user_by_id(data) != None:
        logging.getLogger(__name__).info(f"{tg_user_id} press the {data}")

    return text, markup
