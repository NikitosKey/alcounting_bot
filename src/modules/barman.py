# Бармен имеет очередь заказов, он их принимает и отмечает выполненными.
# Также может заказать что-то сам, либо стать заказчиком.
# Здеся либо класс, либо просто написать логику для менюшек, какие-то функции только для бармена и прочее, прочее.
import logging
import datetime
from typing import Tuple, Any

from modules.customer import Customer
from modules.database import Database
from modules.product import Product
from modules.order import Order
from modules.user import User


from telegram import ForceReply, Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackContext

# Тексты для меню


# Тексты для кнопок


# Создание клавиатур


class Barman(Customer):
    QUEUE_BUTTON = "Очередь заказов"
    QUEUE_TEXT = "<b>Очередь</b>"
    COMPLETE_BUTTON = "Завершить заказ"

    def create_barman_buttons_menu(self):
        buttons = Customer.create_customer_menu_buttons(Customer)
        buttons.append([InlineKeyboardButton(self.QUEUE_BUTTON, callback_data=self.QUEUE_BUTTON)])
        return buttons

    def build_barman_menu(self):
        return InlineKeyboardMarkup(self.create_barman_buttons_menu(self))

    def build_queue_menu(self) -> InlineKeyboardMarkup:
        db = Database()
        my_orders = db.get_orders_queue()
        buttons = []
        if my_orders is not None:
            for my_order in my_orders:
                button = InlineKeyboardButton(f'{my_order.date[:-7]} {my_order.product}', callback_data=f'chose_{my_order.date}')
                buttons.append([button])
        else:
            logging.getLogger(__name__).info(f"No orders in database")
        buttons.append(
            [InlineKeyboardButton(Customer.BACK_TO_MENU_BUTTON, callback_data=Customer.BACK_TO_MENU_BUTTON)])
        return InlineKeyboardMarkup(buttons)

    def build_pre_complete_order_menu(self, data):
        return InlineKeyboardMarkup([[InlineKeyboardButton(self.COMPLETE_BUTTON, callback_data=data)],
                                    [InlineKeyboardButton(Customer.BACK_BUTTON, callback_data=self.QUEUE_BUTTON)],
                                    [InlineKeyboardButton(Customer.BACK_TO_MENU_BUTTON, callback_data=Customer.BACK_TO_MENU_BUTTON)]
                                    ])

    def build_complete_order_menu(self):
        return InlineKeyboardMarkup([
            [InlineKeyboardButton(Customer.BACK_BUTTON, callback_data=self.QUEUE_BUTTON)],
            [InlineKeyboardButton(Customer.BACK_TO_MENU_BUTTON, callback_data=Customer.BACK_TO_MENU_BUTTON)]
            ])

    def back_to_barman_menu(self, data, tg_user_id):
        text = ''
        markup = None

        # Обработка кнопки назад в меню
        if data == self.BACK_TO_MENU_BUTTON:
            logging.getLogger(__name__).info(f'{tg_user_id} return to the barman_menu')
            text = self.CUSTOMER_MENU_TEXT
            markup = self.build_barman_menu(self)

            return text, markup


    def on_button_tap(self, data, tg_user_id):
        text = ''
        markup = None

        text, markup = Customer.on_button_tap(Customer, data, tg_user_id)

        db = Database()

        my_orders: list[Order] = db.get_all_orders()
        order_dates = [str(Order.get_order_date()) for Order in my_orders]


        if data == self.QUEUE_BUTTON:
            logging.getLogger(__name__).info(
                f'{tg_user_id} press the QUEUE_BUTTON or return to the QUEUE menu')
            text = f'{self.QUEUE_BUTTON}'
            markup = self.build_queue_menu(self)

        if data[6:] in order_dates and data[:6] == "chose_":
            logging.getLogger(__name__).info(f'{tg_user_id} watch for the {data}')
            db = Database()
            order = db.get_order_by_date(data[6:])
            text = f'''
            Заказ от: {order.date[:-7]}\nПродукт: {order.product}\nId покупателя: {order.customer_id}\nId бармена: {order.barman_id}\nСтатус: {order.status}'''
            markup = self.build_pre_complete_order_menu(self, str("next"+data))

        if data[10:] in order_dates and data[:10] == "nextchose_":
            db = Database()
            order = db.get_order_by_date(data[10:])
            order.set_order_barman_id(tg_user_id)
            order.set_order_status("завершён")
            db.update_order(order)
            text = f'''Заказ завершён!!!\nОт: {order.date[:-7]}\nПродукт: {order.product}\nId покупателя: {order.customer_id}\nId бармена: {order.barman_id}\nСтатус: {order.status}'''
            markup = self.build_complete_order_menu(self)



        return text, markup




