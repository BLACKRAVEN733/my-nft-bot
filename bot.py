import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "YOUR_BOT_TOKEN"

# Get ETH price in USD
def get_eth_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
    data = requests.get(url).json()
    return data["ethereum"]["usd"]

# Convert USD to MMK
def usd_to_mmk(usd):
    rate = 2100  # you can replace with live API
    return usd * rate

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    eth_price = get_eth_price()
    mmk_price = usd_to_mmk(eth_price)

    msg = f"💰 NFT Floor Price (ETH): {eth_price} USD\n🇲🇲 MMK: {int(mmk_price)} Ks"
    await update.message.reply_text(msg)

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("price", price))

app.run_polling()
