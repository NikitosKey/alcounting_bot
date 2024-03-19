# Покупатель (Заказывающий) может заказать коктейль из списка.
# При заказе должно быть окно подтверждения или отмены заказа, после этого заказ попадает в очередь к бармену.
# MVP готов, осталось навести марафет, какие-то новые фичи и функции.
import logging
import datetime

from modules.database import Database
from modules.product import Product
from modules.order import Order
from modules.user import User

from telegram import ForceReply, Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackContext

# Тексты для меню
CUSTOMER_MENU_TEXT = "<b>Менюшечка</b>\n\n"
SHOW_PRODUCTS_TEXT = "<b>Барная карта</b>\n\n Нажмите на напиток, чтобы показать подробности."
MAKE_ORDER_TEXT = "<b>Выбор напитка</b>\n\n Нажмите на напиток, чтобы заказать"
SHOW_ORDERS_TEXT = "<b>Мои заказы</b>\n\n"

# Тексты для кнопок
SHOW_PRODUCTS_BUTTON = "Барная карта"
MAKE_ORDER_BUTTON = "Сделать заказ"
SHOW_ORDERS_BUTTON = "Мои заказы"
APPROVE_ORDERS_BUTTON = "Подтвердить заказ."
BACK_TO_CUSTOMER_MENU_BUTTON = "Вернуться в главное меню"
BACK_BUTTON = "Назад"

# Костыль для того, чтобы работало окно подтверждения заказа
pre_data_to_approve_order = [None, None]


# Создание клавиатур
def build_customer_menu() -> InlineKeyboardMarkup:
    buttons = [[InlineKeyboardButton(SHOW_PRODUCTS_BUTTON, callback_data=SHOW_PRODUCTS_BUTTON)],
               [InlineKeyboardButton(MAKE_ORDER_BUTTON, callback_data=MAKE_ORDER_BUTTON)],
               [InlineKeyboardButton(SHOW_ORDERS_BUTTON, callback_data=SHOW_ORDERS_BUTTON)]]
    return InlineKeyboardMarkup(buttons)


def build_show_products_menu() -> InlineKeyboardMarkup:
    db = Database()
    my_products = db.get_all_products()
    buttons = []
    if my_products is not None:
        for product in my_products:
            button = InlineKeyboardButton(product.name, callback_data=f'shown_{product.name}')
            buttons.append([button])
    else:
        logging.getLogger(__name__).info(f"No products in database")
    buttons.append([InlineKeyboardButton(BACK_BUTTON, callback_data=BACK_TO_CUSTOMER_MENU_BUTTON)])
    return InlineKeyboardMarkup(buttons)

"""def build_show_product_info_menu() -> InlineKeyboardMarkup:
    buttons = [[InlineKeyboardButton(BACK_TO_CUSTOMER_MENU_BUTTON, callback_data=BACK_TO_CUSTOMER_MENU_BUTTON)],
            [InlineKeyboardButton(BACK_BUTTON, callback_data=SHOW_PRODUCTS_BUTTON)]]
    return InlineKeyboardMarkup(buttons)"""


def build_show_product_info_menu(pre_data) -> InlineKeyboardMarkup:
    buttons = [[InlineKeyboardButton("Сделать заказ", callback_data=pre_data)],
               [InlineKeyboardButton(BACK_TO_CUSTOMER_MENU_BUTTON, callback_data=BACK_TO_CUSTOMER_MENU_BUTTON)],
               [InlineKeyboardButton(BACK_BUTTON, callback_data=SHOW_PRODUCTS_BUTTON)]]
    return InlineKeyboardMarkup(buttons)


def build_make_orders_menu() -> InlineKeyboardMarkup:
    db = Database()
    my_products = db.get_all_products()
    buttons = []
    if my_products is not None:
        for product in my_products:
            button = InlineKeyboardButton(product.name, callback_data=f'chosen_{product.name}')
            buttons.append([button])
    else:
        logging.getLogger(__name__).info(f"No products in database")
    buttons.append([InlineKeyboardButton(BACK_BUTTON, callback_data=BACK_TO_CUSTOMER_MENU_BUTTON)])
    return InlineKeyboardMarkup(buttons)

def build_pre_approve_order_menu(pre_data) -> InlineKeyboardMarkup:
    buttons = [[InlineKeyboardButton(APPROVE_ORDERS_BUTTON, callback_data=pre_data)],
               [InlineKeyboardButton(BACK_BUTTON, callback_data=MAKE_ORDER_BUTTON)],
               [InlineKeyboardButton(BACK_TO_CUSTOMER_MENU_BUTTON, callback_data=BACK_TO_CUSTOMER_MENU_BUTTON)]]
    return InlineKeyboardMarkup(buttons)

def build_approve_order_menu(data) -> InlineKeyboardMarkup:
    buttons = [[InlineKeyboardButton(BACK_TO_CUSTOMER_MENU_BUTTON, callback_data=BACK_TO_CUSTOMER_MENU_BUTTON)],
               [InlineKeyboardButton(BACK_BUTTON, callback_data=data)]]
    return InlineKeyboardMarkup(buttons)

def build_show_orders_menu(id) -> InlineKeyboardMarkup:
    db = Database()
    my_orders = db.get_orders_by_customer_id(id)
    buttons = []
    if my_orders is not None:
        for my_order in my_orders:
            button = InlineKeyboardButton(my_order.date[:-7], callback_data=f'shown_{my_order.date}')
            buttons.append([button])
    else:
            logging.getLogger(__name__).info(f"No orders found for user")

    buttons.append([InlineKeyboardButton(BACK_BUTTON, callback_data=BACK_TO_CUSTOMER_MENU_BUTTON)])
    return InlineKeyboardMarkup(buttons)

def build_show_order_info_menu() -> InlineKeyboardMarkup:
    buttons = [[InlineKeyboardButton(BACK_TO_CUSTOMER_MENU_BUTTON, callback_data=BACK_TO_CUSTOMER_MENU_BUTTON)],
               [InlineKeyboardButton(BACK_BUTTON, callback_data=SHOW_ORDERS_BUTTON)]]
    return InlineKeyboardMarkup(buttons)


class Customer:
    def __init__(self):
        pass

    async def menu(update: Update, context: CallbackContext) -> None:
        """
        This handler sends a menu with the inline buttons we pre-assigned above
        """
        # logging.getLogger(__name__).info(f'{update.message.from_user.id} use {update.message.text}')

        await context.bot.send_message(
            update.message.from_user.id,
            CUSTOMER_MENU_TEXT,
            parse_mode=ParseMode.HTML,
            reply_markup=build_customer_menu()
        )

    # Обработка нажатия кнопок
    async def on_button_tap(update: Update, context: CallbackContext) -> None:
        """
        This handler processes the inline buttons on the menu
        """
        global pre_data_to_approve_order

        data = update.callback_query.data
        text = ''
        markup = None

        db = Database()
        my_products: list[Product] = db.get_all_products()
        product_names = [Product.get_name() for Product in my_products]

        my_orders: list[Order] = db.get_all_orders()
        order_dates = [str(Order.get_order_date()) for Order in my_orders]

        # Обработка кнопок Барной карты
        if data == SHOW_PRODUCTS_BUTTON:
            logging.getLogger(__name__).info(
                f'{update.effective_user.id} press the SHOW_PRODUCTS_BUTTON or return to SHOW_PRODUCTS menu')
            text = SHOW_PRODUCTS_TEXT
            markup = build_show_products_menu()


        elif data[6:] in product_names and data[:6] == "shown_":
            logging.getLogger(__name__).info(f'{update.effective_user.id} watch for the {data}')
            db = Database()
            product = db.get_product_by_name(data[6:])
            text = f'{product.name}\nОписание:\n{product.description}\nЦена:\n{product.price}руб.'
            markup = build_show_product_info_menu(str("chosen_"+data[6:]))
        # Обработка кнопок для создания заказа
        elif data == MAKE_ORDER_BUTTON:
            logging.getLogger(__name__).info(
                f'{update.effective_user.id} press the MAKE_ORDER_BUTTON or return to MAKE_ORDER menu')
            text = MAKE_ORDER_TEXT
            markup = build_make_orders_menu()


        elif data[7:] in product_names and data[:7] == "chosen_":
            logging.getLogger(__name__).info(f'{update.effective_user.id} chosen the {data}')
            text = f'Выбран {data[7:]}.\nПодтвердите ваш заказ.'
            markup = build_pre_approve_order_menu(data[1:])
            pre_data_to_approve_order = [data[1:], update.effective_user.id]


        elif data == pre_data_to_approve_order[0] and update.effective_user.id == pre_data_to_approve_order[1] and pre_data_to_approve_order[0] != None:
            order = Order(str(datetime.datetime.now()), data[6:], update.effective_user.id, None, 'placed')
            db = Database()
            db.insert_order(order)
            pre_data_to_approve_order = [None, None]
            text = f'Выбран {data}\nПодтвердите ваш заказ'
            markup = build_approve_order_menu('c' + data)

        # Обработка кнопок просмотра заказов
        elif data == SHOW_ORDERS_BUTTON:
            logging.getLogger(__name__).info(
                f'{update.effective_user.id} press the SHOW_ORDERS_BUTTON or return to SHOW_ORDERS menu')
            text = SHOW_ORDERS_TEXT
            markup = build_show_orders_menu(update.effective_user.id)

        elif data[6:] in order_dates and data[:6] == "shown_":
            logging.getLogger(__name__).info(f'{update.effective_user.id} watch for the {data}')
            db = Database()
            order = db.get_order_by_date(data[6:])
            text = f'Заказ от: {order.date[:-7]}\nПродукт:\n{order.product}\nId покупателя:\n{order.customer_id}\nId бармена:\n{order.barman_id}\nСтатус:\n{order.status}'
            markup = build_show_order_info_menu()

        # Обработка кнопки назад в меню
        elif data == BACK_TO_CUSTOMER_MENU_BUTTON:
            logging.getLogger(__name__).info(f'{update.effective_user.id} return to the CUSTOMER_MENU')
            text = CUSTOMER_MENU_TEXT
            markup = build_customer_menu()

        logging.getLogger(__name__).info(f'{update.effective_user.id} Callbackdata: {data}')

        # Close the query to end the client-side loading animation
        await update.callback_query.answer()

        # Update message content with corresponding menu section
        await update.callback_query.edit_message_text(
            text,
            ParseMode.HTML,
            reply_markup=markup
        )
