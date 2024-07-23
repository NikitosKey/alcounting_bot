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

    def barman_button_taps(self, data, tg_user_id):
        text = ""
        markup = None

        text, markup = Customer.barman_button_taps(Customer, data, tg_user_id)

        db = Database()

        my_orders = db.get_all_orders()
        order_dates = [str(Order.get_order_date()) for Order in my_orders]

        if data == self.QUEUE_BUTTON:
            logging.getLogger(__name__).info(
                f"{tg_user_id} press the QUEUE_BUTTON or return to the QUEUE menu"
            )
            text = f"{self.QUEUE_BUTTON}"
            markup = self.build_queue_menu()

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
            markup = self.build_pre_complete_order_menu(str("next" + data))

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
            markup = self.build_complete_order_menu()

        return text, markup
