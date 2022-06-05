import aiohttp

from io import BytesIO
from config import JOKE_API_ENDPOINT
from telegram import Update
from telegram.ext import CallbackContext
from recognition import recognize_faces


async def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    await user.send_message(
        f"Hi {user.full_name}!\n\n"
        f"I am a bot that recognizes faces in photos\n"
        f"To start send me any photo"
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
            'No faces found in this photo'
        )


async def send_joke(update: Update, context: CallbackContext) -> None:
    user = update.effective_user

    async with aiohttp.ClientSession() as session:
        async with session.get(JOKE_API_ENDPOINT) as response:
            json_response = await response.json()

    joke = json_response['value']
    await user.send_message(joke)


# Utility function for downloading user image as bytearray
async def download_photo(update: Update, context: CallbackContext) -> BytesIO:
    file = await context.bot.get_file(
        update.message.photo[-1].file_id
    )
    byte_array = await file.download_as_bytearray()
    return BytesIO(byte_array)
