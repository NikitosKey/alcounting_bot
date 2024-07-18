""" Admin classes for the bot. """

import logging

from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from bot.users.customer import Customer
from bot.users.barman import Barman
from bot.database.database import Database


class Admin(Barman):
    """Admin class"""

    """
    Text section
    """
    ADMIN_MENU_TEXT = "Админ панель."
    TO_CUSTOMER_MENU_BUTTON_TEXT = "В меню покупателя."
    TO_BARMAN_MENU_BUTTON_TEXT = "В меню бармена."
    USERS_TABLE_BUTTON_TEXT = "Таблица пользователей."
    MENU_TABLE_BUTTON_TEXT = "Таблица меню."
    ORDERS_TABLE_BUTTON_TEXT = "Таблица заказов."
    STATISTIC_BUTTON_TEXT = "Статистика."
    DELETE_ALL_BUTTON_TEXT = "Удалить всё."
    DELETE_BUTTON_TEXT = "Удалить."
    ADD_NEW_BUTTON_TEXT = "Добавить запись."

    """
    Create buttons section
    """
    # general buttons

    # admin menu buttons
    TO_CUSTOMER_BUTTON = Customer.create_button(
        Customer, TO_CUSTOMER_MENU_BUTTON_TEXT, TO_CUSTOMER_MENU_BUTTON_TEXT
    )

    TO_BARMAN_MENU_BUTTON = InlineKeyboardButton(
        TO_BARMAN_MENU_BUTTON_TEXT, callback_data=TO_BARMAN_MENU_BUTTON_TEXT
    )

    USERS_TABLE_BUTTON = InlineKeyboardButton(
        USERS_TABLE_BUTTON_TEXT, callback_data=USERS_TABLE_BUTTON_TEXT
    )
    MENU_TABLE_BUTTON = InlineKeyboardButton(
        MENU_TABLE_BUTTON_TEXT, callback_data=MENU_TABLE_BUTTON_TEXT
    )
    ORDERS_TABLE_BUTTON = InlineKeyboardButton(
        ORDERS_TABLE_BUTTON_TEXT, callback_data=ORDERS_TABLE_BUTTON_TEXT
    )

    # users table menu buttons

    # products table menu buttons

    # orders table menu buttons

    """
    Build keyboards section
    """

    def build_admin_menu(self):
        buttons = [[]]
        buttons.append([self.TO_CUSTOMER_BUTTON, self.TO_BARMAN_MENU_BUTTON])
        buttons.append([self.USERS_TABLE_BUTTON])
        buttons.append([self.MENU_TABLE_BUTTON])
        buttons.append([self.ORDERS_TABLE_BUTTON])
        return InlineKeyboardMarkup(buttons)

    def build_users_table_menu(self):
        db = Database()
        users = db.get_all_users()
        buttons = []
        for user in users:
            buttons.append([InlineKeyboardButton(user.name, callback_data=user.id)])
        buttons.append(
            [
                InlineKeyboardButton(
                    self.DELETE_ALL_BUTTON_TEXT,
                    callback_data=self.DELETE_ALL_BUTTON_TEXT + "_usr",
                )
            ]
        )
        buttons.append(
            [
                InlineKeyboardButton(
                    self.BACK_TO_MENU_BUTTON, callback_data=self.BACK_TO_MENU_BUTTON
                )
            ]
        )

        return InlineKeyboardMarkup(buttons)

    def build_products_table_menu(self):
        db = Database()
        products = db.get_all_products()
        buttons = []
        for product in products:
            buttons.append(
                [InlineKeyboardButton(product.name, callback_data=product.name)]
            )
        buttons.append(
            [
                InlineKeyboardButton(
                    self.DELETE_ALL_BUTTON_TEXT,
                    callback_data=self.DELETE_ALL_BUTTON_TEXT + "_pro",
                )
            ]
        )
        buttons.append(
            [
                InlineKeyboardButton(
                    self.BACK_TO_MENU_BUTTON, callback_data=self.BACK_TO_MENU_BUTTON
                )
            ]
        )

        return InlineKeyboardMarkup(buttons)

    def build_orders_table_menu(self, context):
        db = Database()
        orders = db.get_all_orders()
        buttons = []
        for order in orders:
            buttons.append(
                [InlineKeyboardButton(order.date, callback_data=(order.date + context))]
            )
        buttons.append(
            [
                InlineKeyboardButton(
                    self.DELETE_ALL_BUTTON_TEXT,
                    callback_data=self.DELETE_ALL_BUTTON_TEXT + "_ord",
                )
            ]
        )
        buttons.append(
            [
                InlineKeyboardButton(
                    self.BACK_TO_MENU_BUTTON, callback_data=self.BACK_TO_MENU_BUTTON
                )
            ]
        )

        return InlineKeyboardMarkup(buttons)

    def back_to_admin_menu(self, data, tg_user_id):
        text = ""
        markup = None

        # Обработка кнопки назад в меню
        if data == self.BACK_TO_MENU_BUTTON:
            logging.getLogger(__name__).info(f"{tg_user_id} return to the admin_menu")
            text = self.ADMIN_MENU_TEXT
            markup = self.build_admin_menu(self)

            return text, markup

    # def on_button_tap(self, data, tg_user_id) -> [str, InlineKeyboardMarkup]:
    #     """
    #     This handler processes the inline buttons on the menu
    #     """
    #
    #     text = ''
    #     markup = None
    #
    #     text, markup = Barman.on_button_tap(Barman, data, tg_user_id)
    #
    #     db = Database()
    #
    #
    #
    #     return text, markup
