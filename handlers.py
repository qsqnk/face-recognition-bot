from io import BytesIO

from telegram import Update
from telegram.ext import CallbackContext
from recognition import recognize_faces


async def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    await user.send_message(
        f"Привет, {user.full_name}!\n\n"
        f"Я - бот, позволяющий выделить лица на фотографиях.\n"
        f"Для этого пришли мне любую фотографию."
    )


async def send_faces(update: Update, context: CallbackContext) -> None:
    input_stream = await download_photo(update, context)
    recognized_faces = recognize_faces(input_stream)

    if recognized_faces:
        await update.message.reply_media_group(
            recognized_faces
        )
    else:
        await update.message.reply_text(
            'На данной фотографии не обнаружено лиц.'
        )


# Utility function for downloading user image as bytearray
async def download_photo(update: Update, context: CallbackContext) -> BytesIO:
    file = await context.bot.get_file(update.message.photo[-1].file_id)
    byte_array = await file.download_as_bytearray()
    return BytesIO(byte_array)
