import os
import google.generativeai as genai

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚨 VERSION 12345 🚨\n\n"
        "Send me a horse racing or greyhound screenshot."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start - Start bot\n"
        "/help - Help menu"
    )


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text("🔍 Analysing screenshot...")

        photo = update.message.photo[-1]

        file = await context.bot.get_file(photo.file_id)

        image_path = "race_image.jpg"
        await file.download_to_drive(image_path)

        prompt = """
You are RaceSharp AI.

Analyse this race screenshot.

Return:

🏆 Predicted Winner
📈 Confidence %
💎 Best Value Bet
⚠️ Risks

Keep response concise and easy to read.
"""

        response = model.generate_content(
            [
                prompt,
                {"mime_type": "image/jpeg", "data": open(image_path, "rb").read()},
            ]
        )

        await update.message.reply_text(response.text)

    except Exception as e:
        await update.message.reply_text(
            f"Error analysing image:\n{str(e)}"
        )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Please send a race screenshot."
    )


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    app.run_polling()


if __name__ == "__main__":
    main()
