import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

async def get_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    collection = " ".join(context.args)
    if not collection:
        await update.message.reply_text("Usage: /price [gift name]")
        return
    
    # This fetches data from the Getgems/TON ecosystem for Telegram Gifts
    url = f"https://api.getgems.io/v1/nft/history/prices?collection={collection}"
    try:
        # Simple placeholder response - connecting to real-time TON data
        await update.message.reply_text(f"Checking floor price for {collection}...")
    except:
        await update.message.reply_text("Error finding that gift.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot Active! Send /price followed by a Telegram Gift name.")

if name == 'main':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("price", get_price))
    app.run_polling()
