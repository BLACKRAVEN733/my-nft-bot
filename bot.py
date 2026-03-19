import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

def get_live_rates():
    try:
        # Fetching live Toncoin price
        url = "https://api.coingecko.com/api/v3/simple/price?ids=toncoin&vs_currencies=usd,mmk"
        response = requests.get(url).json()
        usd = response['toncoin']['usd']
        mmk = response['toncoin']['mmk']
        return usd, mmk
    except:
        return 5.15, 2830 # Backup rates

async def get_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    gift_name = "-".join(context.args).lower()
    if not gift_name:
        await update.message.reply_text("❌ Usage: `/price gift-name`", parse_mode='Markdown')
        return

    msg = await update.message.reply_text(f"🔍 Searching for **{gift_name.title()}**...")

    url = f"https://portal-market.com/api/collections?search={gift_name}&limit=1"
    
    try:
        res = requests.get(url).json()
        data = res["collections"][0]
        floor_ton = float(data.get("floor_price", 0))
        
        ton_to_usd, ton_to_mmk = get_live_rates()
        price_usd = floor_ton * ton_to_usd
        price_mmk = floor_ton * ton_to_mmk

        text = (
            f"🎁 **{data.get('name')}**\n"
            f"━━━━━━━━━━━━━━━\n"
            f"💰 **Floor Price:** `{floor_ton} TON`\n"
            f"💵 **USD:** `${price_usd:.2f}`\n"
            f"🇲🇲 **MMK:** `{price_mmk:,.0f} K`\n"
            f"━━━━━━━━━━━━━━━\n"
            f"👉 [View on Marketplace](https://getgems.io/collection/{gift_name})"
        )
        await msg.edit_text(text, parse_mode='Markdown', disable_web_page_preview=True)
    except:
        await msg.edit_text("❌ Gift not found.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ **Bot Online!**\nUse `/price [name]`")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("price", get_price))
    app.run_polling()
