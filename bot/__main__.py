"""Allows running bot."""

import os
import logging
from datetime import datetime

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
)

from bot.handlers import register_handlers


def main() -> None:
    """Start the bot and register handlers."""
    # Enable logging
    time = datetime.now().isoformat()
    log_path = os.getcwdb().decode() + "/logs/"
    if not os.path.exists(log_path):
        os.makedirs(log_path, exist_ok=True)

    logging.basicConfig(
        handlers=(
            logging.StreamHandler(),
            logging.FileHandler(log_path + time + ".log"),
        ),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.DEBUG,
    )
    # set higher logging level for httpx to avoid all GET and POST requests being logged
    logging.getLogger("httpx").setLevel(logging.WARNING)

    # logger = logging.getLogger(__name__)

    # Create the Application and pass it your bot's token.
    application = Application.builder().token(os.getenv("BOT_TOKEN")).build()

    register_handlers(application)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
