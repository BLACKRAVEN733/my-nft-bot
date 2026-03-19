import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

# Function to get live TON price in USD and MMK
def get_live_rates():
    try:
        # Fetching live Toncoin price from CoinGecko
        url = "https://api.coingecko.com/api/v3/simple/price?ids=toncoin&vs_currencies=usd,mmk"
        response = requests.get(url).json()
        usd = response['toncoin']['usd']
        mmk = response['toncoin']['mmk']
        return usd, mmk
    except:
        # Backup rates if the API is down
        return 5.15, 2830

async def get_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    gift_name = "-".join(context.args).lower()
    
    if not gift_name:
        await update.message.reply_text("❌ Usage: /price gift-name", parse_mode='Markdown')
        return

    msg = await update.message.reply_text(f"🔍 Searching for {gift_name.replace('-', ' ').title()}...")

    # Fetching Gift Floor Price from Marketplace
    market_url = f"https://portal-market.com/api/collections?search={gift_name}&limit=1"
    
    try:
        market_res = requests.get(market_url).json()
        data = market_res["collections"][0]
        floor_ton = float(data.get("floor_price", 0))
        display_name = data.get("name")

        # AUTO UPDATE: Fetch live rates right now
        ton_to_usd, ton_to_mmk = get_live_rates()
        
        price_usd = floor_ton * ton_to_usd
        price_mmk = floor_ton * ton_to_mmk

        getgems_link = f"https://getgems.io/collection/{gift_name}"
        
        text = (
            f"🎁 {display_name}\n"
            f"━━━━━━━━━━━━━━━\n"
            f"💰 Floor Price: {floor_ton} TON\n"
            f"💵 USD: ${price_usd:.2f}\n"
            f"🇲🇲 MMK: {price_mmk:,.0f} K\n"
            f"━━━━━━━━━━━━━━━\n"
            f"📊 *Rates: 1 TON = {ton_to_mmk:,.0f} MMK*\n"
            f"👉 [View on Marketplace]({getgems_link})"
        )
        
        await msg.edit_text(text, parse_mode='Markdown', disable_web_page_preview=True)

    except Exception:
        await msg.edit_text("❌ Gift not found. Try plush-pepe or dog-pals.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Auto-Update Bot Online!\nUse /price [name]", parse_mode='Markdown')

if name == 'main':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("price", get_price))
    app.run_polling()