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
from racesharp.atr_scraper import get_atr_page

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

await update.message.reply_text(
    "RaceSharp Final Edition Online\n\n"
    "Commands:\n"
    "/race 16:53 Salisbury\n"
    "/testatr\n\n"
    "Or send a horse racing screenshot."
)

async def race(update: Update, context: ContextTypes.DEFAULT_TYPE):

try:
    args = context.args
    time = args[0]
    track = " ".join(args[1:])
    report = race_command(track, time)
    await update.message.reply_text(report)
except Exception as e:
    await update.message.reply_text(
        f"Usage:\n/race 16:53 Salisbury\n\nError:\n{str(e)}"
    )

async def testatr(update: Update, context: ContextTypes.DEFAULT_TYPE):

try:
    result = get_atr_page()
    await update.message.reply_text(
        str(result)
    )
except Exception as e:
    await update.message.reply_text(
        f"ATR Test Failed:\n\n{str(e)}"
    )

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):

try:
    await update.message.reply_text(
        "🔍 RaceSharp analysing screenshot..."
    )
    photo = update.message.photo[-1]
    file = await context.bot.get_file(
        photo.file_id
    )
    image_url = file.file_path
    report = analyze_image(
        image_url
    )
    await update.message.reply_text(
        report
    )
except Exception as e:
    await update.message.reply_text(
        f"Screenshot analysis failed:\n\n{str(e)}"
    )

def main():

app = Application.builder().token(
    BOT_TOKEN
).build()
app.add_handler(
    CommandHandler(
        "start",
        start
    )
)
app.add_handler(
    CommandHandler(
        "race",
        race
    )
)
app.add_handler(
    CommandHandler(
        "testatr",
        testatr
    )
)
app.add_handler(
    MessageHandler(
        filters.PHOTO,
        handle_photo
    )
)
print(
    "RaceSharp Final Edition Online"
)
app.run_polling()

if name == “main”:
main()
