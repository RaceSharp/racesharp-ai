from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from racesharp.commands import race_command
from racesharp.config import BOT_TOKEN
from racesharp.analyzer import analyze_image
from racesharp.atr_scraper import (
    get_atr_page,
    get_racecards,
)


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    await update.message.reply_text(
        "RaceSharp Final Edition Online\n\n"
        "Commands:\n"
        "/race 16:53 Salisbury\n"
        "/atr\n"
        "/testatr\n"
        "/testcards\n\n"
        "Or send a horse racing screenshot."
    )


async def race(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    try:

        args = context.args

        if len(args) < 2:
            raise ValueError(
                "Please provide a time and track."
            )

        race_time = args[0]
        track = " ".join(args[1:])

        report = race_command(
            track,
            race_time,
        )

        if not report:
            report = "No report generated."

        chunks = [
            report[i:i + 4000]
            for i in range(
                0,
                len(report),
                4000,
            )
        ]

        for chunk in chunks:
            await update.message.reply_text(
                chunk
            )

    except Exception as e:

        await update.message.reply_text(
            f"Usage:\n"
            f"/race 16:53 Salisbury\n\n"
            f"Error:\n{str(e)}"
        )


async def atr(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    try:

        result = get_atr_page()

        await update.message.reply_text(
            f"ATR TEST\n\n{result}"
        )

    except Exception as e:

        await update.message.reply_text(
            f"ATR ERROR\n\n{str(e)}"
        )


async def testatr(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    await atr(
        update,
        context,
    )


async def testcards(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    await update.message.reply_text(
        "TESTCARDS STARTED"
    )

    try:

        cards = get_racecards()

        await update.message.reply_text(
            f"Found {len(cards)} cards"
        )

        if not cards:

            await update.message.reply_text(
                "No racecards found."
            )
            return

        await update.message.reply_text(
            "\n".join(cards[:20])
        )

    except Exception as e:

        await update.message.reply_text(
            f"TESTCARDS ERROR\n\n{str(e)}"
        )


async def handle_photo(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    try:

        await update.message.reply_text(
            "RaceSharp analysing screenshot..."
        )

        photo = update.message.photo[-1]

        file = await context.bot.get_file(
            photo.file_id
        )

        image_url = file.file_path

        report = analyze_image(
            image_url
        )

        if not report:
            report = "No report generated."

        chunks = [
            report[i:i + 4000]
            for i in range(
                0,
                len(report),
                4000,
            )
        ]

        for chunk in chunks:
            await update.message.reply_text(
                chunk
            )

    except Exception as e:

        await update.message.reply_text(
            f"Screenshot analysis failed:\n\n{str(e)}"
        )


def main():

    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    app.add_handler(
        CommandHandler(
            "start",
            start,
        )
    )

    app.add_handler(
        CommandHandler(
            "race",
            race,
        )
    )

    app.add_handler(
        CommandHandler(
            "atr",
            atr,
        )
    )

    app.add_handler(
        CommandHandler(
            "testatr",
            testatr,
        )
    )

    app.add_handler(
        CommandHandler(
            "testcards",
            testcards,
        )
    )

    app.add_handler(
        MessageHandler(
            filters.PHOTO,
            handle_photo,
        )
    )

    print(
        "RaceSharp Final Edition Online"
    )

    app.run_polling()


if __name__ == "__main__":
    main()
