import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import yt_dlp




# --- CONFIGURATION ---
TOKEN = "YOUR BOT TOKEN HERE"

async def download_instagram(url):
    """Downloads Instagram video using yt-dlp."""
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.%(ext)s',
        'quiet': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            return "video.mp4"  # Simplified; yt-dlp finds the best extension
    except Exception as e:
        print(f"Error: {e}")
        return None


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "instagram.com" not in url:
        await update.message.reply_text("Please send a valid Instagram link!")
        return

    status_msg = await update.message.reply_text("📥 Downloading... please wait.")

    file_path = await download_instagram(url)

    if file_path and os.path.exists(file_path):
        await update.message.reply_video(video=open(file_path, 'rb'))
        os.remove(file_path)  # Clean up space
        await status_msg.delete()
    else:
        await status_msg.edit_text("❌ Failed to download. The post might be private or the link is broken.")


if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("Bot is running...")
    app.run_polling()

import yt_dlp
import os



          
