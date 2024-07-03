# Админ может делать всё, быть барменом, либо заказчиком. 
# Также какие-то логи возможно смотреть и прочую техническую часть. 
# Назначать бармена, и прочее прочее.
# Здеся либо класс, либо просто написать логику для менюшек, какие-то функции только для админа и прочее, прочее.
import logging

from telegram import ForceReply, Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackContext

from modules.barman import Barman
from modules.database import Database

class Admin(Barman):
    def __init__(self):
        pass

    ADMIN_MENU_TEXT = "Админ панель."

    def create_admin_buttons_menu(self):
        buttons = self.create_barman_buttons_menu(Barman)
        # buttons.append([InlineKeyboardButton(self.QUEUE_BUTTON, callback_data=self.QUEUE_BUTTON)])
        return buttons

    def build_admin_menu(self):
        return InlineKeyboardMarkup(self.create_admin_buttons_menu(Admin))


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

        #db = Database()

        return text, markup

