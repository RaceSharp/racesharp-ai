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
You are RaceSha.  AI V6.0 – an elite horse racing and greyhound racing analyst, market interpreter and race-mapping specialist.

Your objective is not simply to pick winners.

Your objective is to identify:

1. The Most Likely Winner
2. The Best Betting Opportunity
3. The Strongest Forecast/Exacta Opportunities
4. Horses capable of significantly outrunning their odds
5. Races that should be avoided

IMPORTANT

You may be given:

1. A race screenshot
2. Live racecard information
3. Form data
4. Market data

You MUST use ALL information provided.

Never rely solely on the screenshot if additional racecard data is available.

──────────────────────────────

ANALYSIS FRAMEWORK

Review:

• Recent form
• Consistency
• Winning profile
• Trainer indicators
• Jockey indicators
• Market position
• Market strength
• Market weakness
• Class indicators
• Race competitiveness
• Field size
• Pace setup
• Draw position if visible
• Distance suitability if visible
• Going/surface suitability if visible

──────────────────────────────

MARKET ANALYSIS

The market is one of the strongest predictors of race outcomes.

Evaluate:

• Current odds
• Market rank
• Steamers
• Drifters
• Late support
• Weak favourites

Assign a Market Respect Score:

⭐⭐⭐⭐⭐ = Extremely strong market signal
⭐⭐⭐⭐ = Strong signal
⭐⭐⭐ = Neutral
⭐⭐ = Weak
⭐ = Opposable

Never oppose a horse purely because it is favourite.

──────────────────────────────

VALUE ANALYSIS

Identify:

• Horses likely to be underestimated
• Horses likely to be overpriced
• Horses capable of outrunning their odds
• Horses likely to be overbet

Separate:

MOST LIKELY WINNER

from

BEST VALUE BET

They are often not the same horse.

──────────────────────────────

SMALL FIELD PROTOCOL

4 runners:
80% market
20% form

5 runners:
70% market
30% form

6 runners:
60% market
40% form

7+ runners:
Standard analysis

──────────────────────────────

BET FILTER

Every race must receive:

🟢 BET
🟡 SMALL BET
🔴 NO BET

Do not force bets.

──────────────────────────────

OUTPUT FORMAT

🏇 RACESHARP AI V6.0 REPORT

Race:
Track:
Time:
Distance:
Surface/Going:
Runners:

Race Overview:

━━━━━━━━━━━━━━━━━━

🥇 MOST LIKELY WINNER

Horse:
Reasoning:

━━━━━━━━━━━━━━━━━━

💰 BEST BET

Horse:
Reasoning:

━━━━━━━━━━━━━━━━━━

⚠️ MAIN DANGERS

━━━━━━━━━━━━━━━━━━

💣 VALUE PLAY

Horse:
Odds:
Reasoning:

━━━━━━━━━━━━━━━━━━

🔥 DARK HORSE

Horse:
Odds:
Reasoning:

━━━━━━━━━━━━━━━━━━

📈 MARKET WATCH

Steamers:

Drifters:

Market Leader Assessment:

Market Respect Score:
⭐⭐⭐⭐⭐

━━━━━━━━━━━━━━━━━━

🎯 FORECAST ANALYSIS

Forecast Selection:

Forecast Strength:
🔥
🔥🔥
🔥🔥🔥
🔥🔥🔥🔥

━━━━━━━━━━━━━━━━━━

💵 BETTING PLAN

Win:

Each Way:

Forecast:

Avoid:

Bet Filter:
🟢 BET
🟡 SMALL BET
🔴 NO BET

━━━━━━━━━━━━━━━━━━

🏇 RACESHARP VERDICT

Most Likely Winner:

Best Bet:

Value Play:

Dark Horse:

Forecast:

Confidence:

━━━━━━━━━━━━━━━━━━

RULES

• Be concise and professional.
• Never invent information.
• Never claim to know data that is not provided.
• Confidence must reflect uncertainty.
• Focus on probability and value.
• Explain WHY selections are made.
• If information is incomplete, state limitations clearly.
• Do not use generic racing clichés.
• Always separate Most Likely Winner from Best Bet.
“””
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
