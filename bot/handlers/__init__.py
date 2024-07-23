"""Package containing"""

__all__ = ["start_command", "help_command", "callback_handler", "menu_command", "cmd"]

from telegram.ext import CommandHandler, CallbackQueryHandler, MessageHandler, filters

from bot.handlers.callbacks import callback_handler
from bot.handlers.cmd import cmd
from bot.handlers.help import help_command
from bot.handlers.menu import menu_command
from bot.handlers.start import start_command


def register_commands(application):
    """Register all commands"""
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("menu", menu_command))
    application.add_handler(CallbackQueryHandler(callback_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, cmd))


# Alias
register_handlers = register_commands
