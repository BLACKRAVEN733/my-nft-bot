import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# This uses your secret token from Render's Environment Variables
TOKEN = os.getenv("BOT_TOKEN")

async def get_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    gift_name = " ".join(context.args).lower()
    if not gift_name:
        await update.message.reply_text("❌ Please enter a gift name.\nExample: /price plush pepe", parse_mode='Markdown')
        return

    await update.message.reply_text(f"🔍 Searching for the best price on {gift_name.title()}...")

    # Fetching from the TON ecosystem API (Getgems)
    url = f"https://api.getgems.io/v1/nft/history/prices?collection={gift_name.replace(' ', '-')}"
    
    try:
        # Note: In a real scenario, you'd parse specific marketplace data here
        # For this 'copy-paste' version, we'll simulate the response format
        response = requests.get(url).json()
        # This is a simplified display for the demo
        await update.message.reply_text(f"📊 *{gift_name.title()}* Info:\n\n💰 Floor Price: Checking Marketplace...\n🔗 [View on Getgems](https://getgems.io/)", parse_mode='Markdown')
    except:
        await update.message.reply_text("⚠️ Could not fetch live data. Please check the name and try again.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ *Bot is Online!*\n\nUse /price [name] to check any Telegram NFT Gift.", parse_mode='Markdown')

if name == 'main':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("price", get_price))
    print("Bot is running...")
    app.run_polling()
