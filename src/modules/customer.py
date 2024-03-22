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



# Создание клавиатур


# Не могу полноценно пользоваться классом из-за асинхронного программирования. self не работает в классах с async функциями :( Обойти пытался, но наследование всё равно работает через очко, поэтому пока так.
class Customer:
    CUSTOMER_MENU_TEXT = "<b>Менюшечка</b>\n\n"
    SHOW_PRODUCTS_TEXT = "<b>Барная карта</b>\n\n Нажмите на напиток, чтобы показать подробности."
    MAKE_ORDER_TEXT = "<b>Выбор напитка</b>\n\n Нажмите на напиток, чтобы заказать"
    SHOW_ORDERS_TEXT = "<b>Мои заказы</b>\n\n"

    # Тексты для кнопок
    SHOW_PRODUCTS_BUTTON = "Барная карта"
    MAKE_ORDER_BUTTON = "Сделать заказ"
    SHOW_ORDERS_BUTTON = "Мои заказы"
    APPROVE_ORDERS_BUTTON = "Подтвердить заказ."
    BACK_TO_MENU_BUTTON = "Вернуться в главное меню"
    BACK_BUTTON = "Назад"

    def __init__(self):

        pass

    def create_customer_menu_buttons(self):
        return [[InlineKeyboardButton(self.SHOW_PRODUCTS_BUTTON, callback_data=self.SHOW_PRODUCTS_BUTTON)],
                   [InlineKeyboardButton(self.MAKE_ORDER_BUTTON, callback_data=self.MAKE_ORDER_BUTTON)],
                   [InlineKeyboardButton(self.SHOW_ORDERS_BUTTON, callback_data=self.SHOW_ORDERS_BUTTON)]]


    def build_customer_menu(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(self.create_customer_menu_buttons(self))

    def build_show_products_menu(self) -> InlineKeyboardMarkup:
        db = Database()
        my_products = db.get_all_products()
        buttons = []
        if my_products is not None:
            for product in my_products:
                button = InlineKeyboardButton(product.name, callback_data=f'shown_{product.name}')
                buttons.append([button])
        else:
            logging.getLogger(__name__).info(f"No products in database")
        buttons.append([InlineKeyboardButton(self.BACK_TO_MENU_BUTTON, callback_data=self.BACK_TO_MENU_BUTTON)])
        return InlineKeyboardMarkup(buttons)

    """def build_show_product_info_menu() -> InlineKeyboardMarkup:
        buttons = [[InlineKeyboardButton(BACK_TO_CUSTOMER_MENU_BUTTON, callback_data=BACK_TO_CUSTOMER_MENU_BUTTON)],
                [InlineKeyboardButton(BACK_BUTTON, callback_data=SHOW_PRODUCTS_BUTTON)]]
        return InlineKeyboardMarkup(buttons)"""

    def build_show_product_info_menu(self, data) -> InlineKeyboardMarkup:
        buttons = [[InlineKeyboardButton("Сделать заказ", callback_data=data)],
                   [InlineKeyboardButton(self.BACK_BUTTON, callback_data=self.SHOW_PRODUCTS_BUTTON)],
                   [InlineKeyboardButton(self.BACK_TO_MENU_BUTTON, callback_data=self.BACK_TO_MENU_BUTTON)]]
        return InlineKeyboardMarkup(buttons)

    def build_make_orders_menu(self) -> InlineKeyboardMarkup:
        db = Database()
        my_products = db.get_all_products()
        buttons = []
        if my_products is not None:
            for product in my_products:
                button = InlineKeyboardButton(product.name, callback_data=f'chose_{product.name}')
                buttons.append([button])
        else:
            logging.getLogger(__name__).info(f"No products in database")
        buttons.append([InlineKeyboardButton(self.BACK_TO_MENU_BUTTON, callback_data=self.BACK_TO_MENU_BUTTON)])
        return InlineKeyboardMarkup(buttons)

    def build_pre_approve_order_menu(self, data) -> InlineKeyboardMarkup:
        buttons = [[InlineKeyboardButton(self.APPROVE_ORDERS_BUTTON, callback_data=data)],
                   [InlineKeyboardButton(self.BACK_BUTTON, callback_data=self.MAKE_ORDER_BUTTON)],
                   [InlineKeyboardButton(self.BACK_TO_MENU_BUTTON, callback_data=self.BACK_TO_MENU_BUTTON)]]
        return InlineKeyboardMarkup(buttons)

    def build_approve_order_menu(self, pre_data) -> InlineKeyboardMarkup:
        buttons = ([InlineKeyboardButton(self.BACK_BUTTON, callback_data=pre_data)],
                   [InlineKeyboardButton(self.BACK_TO_MENU_BUTTON, callback_data=self.BACK_TO_MENU_BUTTON)])

        return InlineKeyboardMarkup(buttons)

    def build_show_orders_menu(self, id) -> InlineKeyboardMarkup:
        db = Database()
        my_orders = db.get_orders_by_customer_id(id)
        buttons = []
        if my_orders is not None:
            for my_order in my_orders:
                button = InlineKeyboardButton(my_order.date[:-7], callback_data=f'shown_{my_order.date}')
                buttons.append([button])
        else:
            logging.getLogger(__name__).info(f"No orders found for user")

        buttons.append([InlineKeyboardButton(self.BACK_TO_MENU_BUTTON, callback_data=self.BACK_TO_MENU_BUTTON)])
        return InlineKeyboardMarkup(buttons)

    def build_show_order_info_menu(self) -> InlineKeyboardMarkup:
        buttons = [[InlineKeyboardButton(self.BACK_BUTTON, callback_data=self.SHOW_ORDERS_BUTTON)],
                   [InlineKeyboardButton(self.BACK_TO_MENU_BUTTON, callback_data=self.BACK_TO_MENU_BUTTON)]]
        return InlineKeyboardMarkup(buttons)


    def back_to_customer_menu(self, data, tg_user_id) -> [str, InlineKeyboardMarkup]:
        text = ''
        markup = None
        # Обработка кнопки назад в меню
        if data == self.BACK_TO_MENU_BUTTON:
            logging.getLogger(__name__).info(f'{tg_user_id} return to the CUSTOMER_MENU')
            text = self.CUSTOMER_MENU_TEXT
            markup = self.build_customer_menu(self)
            return text, markup

    def on_button_tap(self, data, tg_user_id) -> (str, InlineKeyboardMarkup):
        text = ''
        markup = None

        db = Database()
        my_products: list[Product] = db.get_all_products()
        product_names = [Product.get_name() for Product in my_products]

        my_orders: list[Order] = db.get_all_orders()
        order_dates = [str(Order.get_order_date()) for Order in my_orders]

        # Обработка кнопок Барной карты
        if data == self.SHOW_PRODUCTS_BUTTON:
            logging.getLogger(__name__).info(
                f'{tg_user_id} press the SHOW_PRODUCTS_BUTTON or return to SHOW_PRODUCTS menu')
            text = self.SHOW_PRODUCTS_TEXT
            markup = self.build_show_products_menu(self)


        if data[6:] in product_names and data[:6] == "shown_":
            logging.getLogger(__name__).info(f'{tg_user_id} watch for the {data[6:]}')
            db = Database()
            product = db.get_product_by_name(data[6:])
            text = f'{product.name}\nОписание:\n{product.description}\nЦена:\n{product.price}руб.'
            markup = self.build_show_product_info_menu(self, str(data[1:]))

        # Обработка кнопок для создания заказа
        if data == self.MAKE_ORDER_BUTTON:
            logging.getLogger(__name__).info(
                f'{tg_user_id} press the MAKE_ORDER_BUTTON or return to MAKE_ORDER menu')
            text = self.MAKE_ORDER_TEXT
            markup = self.build_make_orders_menu(self)


        if (data[6:] in product_names and data[:6] == "chose_") or (
                data[5:] in product_names and data[:5] == 'hown_'):
            if data[:5] == 'hown_':
                data = 's' + data
            logging.getLogger(__name__).info(f'{tg_user_id} chosen the {data}')
            text = f'Выбран {data[6:]}.\nПодтвердите ваш заказ.'
            print(str("next" + data)[:10])
            markup = self.build_pre_approve_order_menu(self, str('next' + data))


        if data[10:] in product_names and (data[:10] == "nextchose_" or data[:10] == "nextshown_"):
            order = Order(str(datetime.datetime.now()), data[10:], tg_user_id, None, 'размещён')
            db = Database()
            db.insert_order(order)
            text = f'Заказ оформлен!\nВремя заказа: {order.date[:-7]}\nПродукт:\n{order.product}\nId покупателя:\n{order.customer_id}'
            markup = self.build_approve_order_menu(self, data[4:])

        # Обработка кнопок просмотра заказов
        if data == self.SHOW_ORDERS_BUTTON:
            logging.getLogger(__name__).info(
                f'{tg_user_id} press the SHOW_ORDERS_BUTTON or return to SHOW_ORDERS menu')
            text = self.SHOW_ORDERS_TEXT
            markup = self.build_show_orders_menu(self, tg_user_id)

        if data[6:] in order_dates and data[:6] == "shown_":
            logging.getLogger(__name__).info(f'{tg_user_id} watch for the {data}')
            db = Database()
            order = db.get_order_by_date(data[6:])
            text = f'''
            Заказ от: {order.date[:-7]}\n
            Продукт: {order.product}
            Id покупателя: {order.customer_id}
            Id бармена: {order.barman_id}
            Статус: {order.status} '''
            markup = self.build_show_order_info_menu(self)


        return (text, markup)

    # Обработка нажатия кнопок




