import os
import subprocess
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = os.getenv("TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام 👋\n"
        "لینک اینستاگرام را بفرستید تا دانلود کنم."
    )


async def download_instagram(update: Update, context: ContextTypes.DEFAULT_TYPE):

    url = update.message.text

    if "instagram.com" not in url:
        await update.message.reply_text(
            "❌ لطفاً لینک معتبر اینستاگرام بفرستید."
        )
        return

    await update.message.reply_text(
        "⏳ در حال دانلود..."
    )

    try:
        filename = "instagram_video.mp4"

        command = [
            "yt-dlp",
            "-f",
            "mp4",
            "-o",
            filename,
            url
        ]

        subprocess.run(
            command,
            check=True
        )

        await update.message.reply_video(
            video=open(filename, "rb"),
            caption="✅ دانلود شد"
        )

        os.remove(filename)

    except Exception as e:
        await update.message.reply_text(
            f"❌ خطا:\n{e}"
        )


def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT,
            download_instagram
        )
    )

    app.run_polling()


if __name__ == "__main__":
    main()
