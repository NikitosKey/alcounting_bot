import os
import logging
from datetime import datetime

from bot.handlers import cmd, start, help, menu, callbacks

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler


def main() -> None:
    time = datetime.now().isoformat()
    log_path = os.getcwdb().decode() + "/logs/"
    if not os.path.exists(log_path):
        os.makedirs(log_path, exist_ok=True)
    # Enable logging
    logging.basicConfig(
        handlers=(logging.StreamHandler(), logging.FileHandler(log_path + time + ".log")),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG,
    )
    # set higher logging level for httpx to avoid all GET and POST requests being logged
    logging.getLogger("httpx").setLevel(logging.WARNING)

    logger = logging.getLogger(__name__)
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(os.getenv('BOT_TOKEN')).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("menu", menu))

    # Register handler for inline buttons
    application.add_handler(CallbackQueryHandler(callbacks))

    # on non command i.e. message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, cmd))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
