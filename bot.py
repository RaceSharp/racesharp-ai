import os
import base64

from openai import OpenAI

from telegram import Update
from telegram.ext import (
Application,
CommandHandler,
MessageHandler,
ContextTypes,
filters,
)

BOT_TOKEN = os.getenv(“BOT_TOKEN”)
OPENAI_API_KEY = os.getenv(“OPENAI_API_KEY”)

client = OpenAI(api_key=OPENAI_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
await update.message.reply_text(
“🏇 RaceSharp AI V6.0\n\n”
“Send me a horse racing or greyhound screenshot.”
)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
await update.message.reply_text(
“/start - Start bot\n”
“/help - Help menu”
)

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
try:
await update.message.reply_text(“🔍 Analysing screenshot…”)

    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    image_path = "race_image.jpg"
    await file.download_to_drive(image_path)
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(
            image_file.read()
        ).decode("utf-8")
    prompt = """

PASTE YOUR FULL RACESHARP 6.0 PROMPT HERE
“””

    response = client.responses.create(
        model="gpt-5.5",
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": prompt,
                    },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{base64_image}",
                    },
                ],
            }
        ],
    )
    result = response.output_text
    await update.message.reply_text(result)
except Exception as e:
    await update.message.reply_text(
        f"❌ Error analysing image:\n\n{str(e)}"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
await update.message.reply_text(
“📸 Please send a horse racing or greyhound screenshot.”
)

def main():
app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(
    MessageHandler(filters.PHOTO, handle_photo)
)
app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        handle_message
    )
)
print("RaceSharp AI Online")
app.run_polling()

if name == “main”:
main()
