import logging

from telegram.ext import Application, CommandHandler, MessageHandler, filters

from config import TOKEN
from handlers import *

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def main() -> None:
    app = Application.builder().token(TOKEN).build()
    for handler in [
        CommandHandler(
            command='start',
            callback=start
        ),
        MessageHandler(
            filters=filters.PHOTO,
            callback=send_faces
        )
    ]:
        app.add_handler(handler)
    app.run_polling()


if __name__ == "__main__":
    main()
