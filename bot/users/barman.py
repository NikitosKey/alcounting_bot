import logging

from bot.users.customer import Customer
from bot.database.database import Database
from bot.database.user import User

from telegram import InlineKeyboardMarkup, InlineKeyboardButton


class Barman(Customer):
    # Тексты для меню
    QUEUE_TEXT = "<b>Очередь</b>"
    # Тексты для кнопок
    QUEUE_BUTTON = "Очередь заказов"
    COMPLETE_BUTTON = "Завершить заказ"

    # Создание клавиатур
    def create_barman_buttons_menu(self):
        buttons = Customer.create_customer_menu_buttons(self)
        buttons.append(
            [InlineKeyboardButton(self.QUEUE_BUTTON, callback_data=self.QUEUE_BUTTON)]
        )
        return buttons

    def build_barman_menu(self):
        return InlineKeyboardMarkup(self.create_barman_buttons_menu())

    def build_queue_menu(self) -> InlineKeyboardMarkup:
        db = Database()
        my_orders = db.get_orders_queue()
        buttons = []
        if my_orders is not None:
            for my_order in my_orders:
                button = InlineKeyboardButton(
                    f"{my_order.date[:-7]} {my_order.product}",
                    callback_data=f"chose_{my_order.date}",
                )
                buttons.append([button])
        else:
            logging.getLogger(__name__).info(f"No orders in database")
        buttons.append(
            [
                InlineKeyboardButton(
                    Customer.BACK_TO_MENU_BUTTON,
                    callback_data=Customer.BACK_TO_MENU_BUTTON,
                )
            ]
        )
        return InlineKeyboardMarkup(buttons)

    def build_pre_complete_order_menu(self, data):
        return InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(self.COMPLETE_BUTTON, callback_data=data)],
                [
                    InlineKeyboardButton(
                        Customer.BACK_BUTTON, callback_data=self.QUEUE_BUTTON
                    )
                ],
                [
                    InlineKeyboardButton(
                        Customer.BACK_TO_MENU_BUTTON,
                        callback_data=Customer.BACK_TO_MENU_BUTTON,
                    )
                ],
            ]
        )

    def build_complete_order_menu(self):
        return InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        Customer.BACK_BUTTON, callback_data=self.QUEUE_BUTTON
                    )
                ],
                [
                    InlineKeyboardButton(
                        Customer.BACK_TO_MENU_BUTTON,
                        callback_data=Customer.BACK_TO_MENU_BUTTON,
                    )
                ],
            ]
        )

    # Обработка нажатия кнопок
    def back_to_barman_menu(self, data, tg_user_id):
        text = ""
        markup = None

        # Обработка кнопки назад в меню
        if data == self.BACK_TO_MENU_BUTTON:
            logging.getLogger(__name__).info(f"{tg_user_id} return to the barman_menu")
            text = self.CUSTOMER_MENU_TEXT
            markup = self.build_barman_menu(self)

            return text, markup

    def on_button_tap(self, data, tg_user_id):
        text = ""
        markup = None

        text, markup = Customer.on_button_tap(Customer, data, tg_user_id)

        db = Database()

        my_orders = db.get_all_orders()
        order_dates = [str(Order.get_order_date()) for Order in my_orders]

        return text, markup
