from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import requests

# ==========================
# ВСТАВЬ СВОЙ ТОКЕН СЮДА
# ==========================
TOKEN = "8849365328:AAFKhqMlGXv2plnUEQ_D-6EdFems7YbRQBY"

# =========================
# TMDb API
# ==========================
with open("apikey.txt", "r", encoding="utf-8") as f:
    TMDB_API_KEY = f.read().strip()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎬 MovieBot запущен!\n\n"
        "Просто отправь название фильма или сериала."
    )


async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text

    url = "https://api.themoviedb.org/3/search/multi"

    params = {
        "api_key": TMDB_API_KEY,
        "language": "ru-RU",
        "query": query,
        "page": 1,
    }

    r = requests.get(url, params=params, timeout=30)

    if r.status_code != 200:
        await update.message.reply_text("Ошибка подключения к TMDb.")
        return

    data = r.json()

    if not data["results"]:
        await update.message.reply_text("Ничего не найдено.")
        return

    film = data["results"][0]

    title = film.get("title") or film.get("name")
    overview = film.get("overview", "Нет описания.")
    date = film.get("release_date") or film.get("first_air_date", "")
    rating = film.get("vote_average", 0)

    text = (
        f"🎬 {title}\n\n"
        f"📅 {date}\n"
        f"⭐ {rating}\n\n"
        f"{overview}"
    )

    await update.message.reply_text(text)


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search))

print("MovieBot запущен!")

app.run_polling()
