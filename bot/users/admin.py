import logging

from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from bot.users.customer import Customer
from bot.users.barman import Barman
from bot.database.database import Database


class Admin(Barman):
    def __init__(self):
        pass

    """
    Text section
    """
    ADMIN_MENU_TEXT = "Админ панель."
    TO_BARMAN_MENU_BUTTON = "В меню бармена."
    TO_CUSTOMER_MENU_BUTTON = "В меню покупателя."
    USERS_TABLE_BUTTON = "Таблица пользователей."
    MENU_TABLE_BUTTON = "Таблица меню."
    ORDERS_TABLE_BUTTON = "Таблица заказов."
    STATISTIC_BUTTON = "Статистика."
    DELETE_ALL_BUTTON = "Удалить всё."
    DELETE_BUTTON = "Удалить."
    ADD_NEW_BUTTON = "Добавить запись."

    """
    Create buttons section
    """
    # admin menu buttons

    # users table menu buttons

    # products table menu buttons

    # orders table menu buttons



    """
    Build keyboards section
    """
    def build_admin_menu(self):
        buttons = [[InlineKeyboardButton(self.TO_CUSTOMER_MENU_BUTTON, callback_data=self.TO_CUSTOMER_MENU_BUTTON)]]
        buttons.append([InlineKeyboardButton(self.TO_BARMAN_MENU_BUTTON, callback_data=self.TO_BARMAN_MENU_BUTTON)])
        buttons.append([InlineKeyboardButton(self.USERS_TABLE_BUTTON, callback_data=self.USERS_TABLE_BUTTON)])
        buttons.append([InlineKeyboardButton(self.ORDERS_TABLE_BUTTON, callback_data=self.ORDERS_TABLE_BUTTON)])
        buttons.append([InlineKeyboardButton(self.MENU_TABLE_BUTTON, callback_data=self.MENU_TABLE_BUTTON)])
        return InlineKeyboardMarkup(buttons)

    def build_users_table_menu(self):
        db = Database()
        users = db.get_all_users()
        buttons = []
        for user in users:
            buttons.append([InlineKeyboardButton(user.name, callback_data=user.id)])
        buttons.append([InlineKeyboardButton(self.DELETE_ALL_BUTTON, callback_data=self.DELETE_ALL_BUTTON + '_usr')])
        buttons.append([InlineKeyboardButton(self.BACK_TO_MENU_BUTTON, callback_data=self.BACK_TO_MENU_BUTTON)])

        return InlineKeyboardMarkup(buttons)

    def build_products_table_menu(self):
        db = Database()
        products = db.get_all_products()
        buttons = []
        for product in products:
            buttons.append([InlineKeyboardButton(product.name, callback_data=product.name)])
        buttons.append([InlineKeyboardButton(self.DELETE_ALL_BUTTON, callback_data=self.DELETE_ALL_BUTTON + '_pro')])
        buttons.append([InlineKeyboardButton(self.BACK_TO_MENU_BUTTON, callback_data=self.BACK_TO_MENU_BUTTON)])

        return InlineKeyboardMarkup(buttons)

    def build_orders_table_menu(self, context):
        db = Database()
        orders = db.get_all_orders()
        buttons = []
        for order in orders:
            buttons.append([InlineKeyboardButton(order.date, callback_data=(order.date + context))])
        buttons.append([InlineKeyboardButton(self.DELETE_ALL_BUTTON, callback_data=self.DELETE_ALL_BUTTON + '_ord')])
        buttons.append([InlineKeyboardButton(self.BACK_TO_MENU_BUTTON, callback_data=self.BACK_TO_MENU_BUTTON)])

        return InlineKeyboardMarkup(buttons)

    def back_to_admin_menu(self, data, tg_user_id):
        text = ''
        markup = None

        # Обработка кнопки назад в меню
        if data == self.BACK_TO_MENU_BUTTON:
            logging.getLogger(__name__).info(f'{tg_user_id} return to the admin_menu')
            text = self.ADMIN_MENU_TEXT
            markup = self.build_admin_menu(self)

            return text, markup

    def on_button_tap(self, data, tg_user_id) -> None:
        """
        This handler processes the inline buttons on the menu
        """

        text = ''
        markup = None

        text, markup = Barman.on_button_tap(Barman, data, tg_user_id)

        db = Database()

        if data == self.TO_CUSTOMER_MENU_BUTTON:
            logging.getLogger(__name__).info(
                f'{tg_user_id} press the TO_CUSTOMER_MENU_BUTTON'
            )
            text = self.CUSTOMER_MENU_TEXT
            markup = self.build_customer_menu(Customer)

        if data == self.TO_BARMAN_MENU_BUTTON:
            logging.getLogger(__name__).info(
                f'{tg_user_id} press the TO_BARMAN_MENU_BUTTON'
            )
            text = self.CUSTOMER_MENU_TEXT
            markup = self.build_barman_menu(Barman)

        if data == self.USERS_TABLE_BUTTON:
            logging.getLogger(__name__).info(
                f'{tg_user_id} press the USERS_TABLE_BUTTON'
            )
            text = self.USERS_TABLE_TEXT
            markup = self.build_users_table_menu(self)

        if data == self.MENU_TABLE_BUTTON:
            logging.getLogger(__name__).info(
                f'{tg_user_id} press the MENU_TABLE_BUTTON'
            )
            text = self.MENU_TABLE_BUTTON
            markup = self.build_products_table_menu(self)

        if data == self.ORDERS_TABLE_BUTTON:
            logging.getLogger(__name__).info(
                f'{tg_user_id} press the ORDERS_TABLE_BUTTON'
            )
            text = self.ORDERS_TABLE_BUTTON
            markup = self.build_orders_table_menu(self, "admin")

        if db.get_user_by_id(data) != None:
            logging.getLogger(__name__).info(
                f'{tg_user_id} press the {data}'
            )

        return text, markup
