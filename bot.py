from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

from racesharp.commands import race_command
from racesharp.config import BOT_TOKEN


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏇 RaceSharp Final Edition Online"
    )


async def race(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        args = context.args

        time = args[0]
        track = " ".join(args[1:])

        report = race_command(track, time)

        await update.message.reply_text(report)

    except Exception:
        await update.message.reply_text(
            "Usage:\n/race 15:18 Salisbury"
        )


def main():

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("race", race))

    app.run_polling()


if __name__ == "__main__":
    main()
