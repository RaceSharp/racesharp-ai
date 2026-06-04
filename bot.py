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

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Gemini 2.0 Flash
model = genai.GenerativeModel("gemini-2.0-flash")


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
You are RaceSharp AI, a professional horse racing and greyhound racing analyst.

Analyse the race screenshot and return ONLY this format:

🏆 MOST LIKELY WINNER
- Runner:
- Confidence: X/10
- Short reason:

🔥 NAP OF THE RACE
- Runner:
- Confidence: X/10
- Why this is the strongest bet:

💎 BEST VALUE BET
- Runner:
- Odds:
- Why it offers value:

⚠️ LAY CANDIDATE
- Runner:
- Why it may be vulnerable:

📊 MARKET ANALYSIS
- Market movers
- Steamers
- Drifters

⚡ RISK FACTORS
- Key concerns
- Race competitiveness
- Field size impact

🎯 VERDICT
1st Choice:
2nd Choice:
3rd Choice:

Betting Strategy:
WIN / EACH WAY / NO BET

Keep analysis concise and professional.
"""

        with open(image_path, "rb") as img:
            image_bytes = img.read()

        response = model.generate_content(
            [
                prompt,
                {
                    "mime_type": "image/jpeg",
                    "data": image_bytes,
                },
            ]
        )

        await update.message.reply_text(response.text)

    except Exception as e:
        await update.message.reply_text(
            f"❌ Error analysing image:\n\n{str(e)}"
        )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📸 Please send a horse racing or greyhound screenshot."
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


if __name__ == "__main__":
    main()
