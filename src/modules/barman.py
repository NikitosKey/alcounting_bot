# Бармен имеет очередь заказов, он их принимает и отмечает выполненными.
# Также может заказать что-то сам, либо стать заказчиком.
# Здеся либо класс, либо просто написать логику для менюшек, какие-то функции только для бармена и прочее, прочее.
import logging
import datetime

from modules.database import Database
from modules.product import Product
from modules.order import Order
from modules.user import User
from modules.customer import Customer

from telegram import ForceReply, Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackContext

# Тексты для меню


# Тексты для кнопок


# Создание клавиатур


class Barman(Customer):
    def __init__(self):
        super().__init__()

    async def menu(update: Update, context: CallbackContext):
        pass



    async def on_button_tap(update: Update, context: CallbackContext) -> None:
        pass

