import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

async def get_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    gift_name = " ".join(context.args).lower()
    if not gift_name:
        await update.message.reply_text("❌ Please enter a gift name.\nExample: /price plush pepe")
        return

    await update.message.reply_text(f"🔍 Searching for {gift_name.title()}...")
    await update.message.reply_text(f"📊 *{gift_name.title()}* Info:\n\n💰 Floor Price: Checking...\n🔗 [View Marketplace](https://getgems.io/)", parse_mode='Markdown')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ *Bot is Online!*\nUse /price [name] to check a gift.", parse_mode='Markdown')

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("price", get_price))
    app.run_polling()
