from telegram import Update
from telegram.ext import ContextTypes

from modules.kp import search_movie


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет!\n\nНапиши название фильма или сериала."
    )


async def text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    movie = search_movie(update.message.text)

    if movie is None:
        await update.message.reply_text("Ничего не найдено.")
        return

    name = movie.get("nameRu") or movie.get("nameOriginal") or "Без названия"
    year = movie.get("year", "?")
    rating = movie.get("ratingKinopoisk", "-")

    await update.message.reply_text(
        f"🎬 {name}\n"
        f"📅 {year}\n"
        f"⭐ {rating}"
    )
