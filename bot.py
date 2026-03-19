import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "8628757389:AAG6MlRL4OrUW7HrHtRNSJfwfcMTqIXgwh4"

CHAT_ID = None  # will store user chat id

# Get ETH price
def get_eth_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
    data = requests.get(url).json()
    return data["ethereum"]["usd"]

# USD → MMK
def usd_to_mmk(usd):
    rate = 2100  # you can replace with live API
    return usd * rate

# Send price
async def send_price(context: ContextTypes.DEFAULT_TYPE):
    global CHAT_ID
    if CHAT_ID is None:
        return

    eth_price = get_eth_price()
    mmk_price = usd_to_mmk(eth_price)

    msg = f"🔄 Auto Update\n💰 ETH: {eth_price} USD\n🇲🇲 MMK: {int(mmk_price)} Ks"
    await context.bot.send_message(chat_id=CHAT_ID, text=msg)

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global CHAT_ID
    CHAT_ID = update.effective_chat.id

    await update.message.reply_text("✅ Auto price update started!")

    # Run every 60 seconds
    context.job_queue.run_repeating(send_price, interval=60, first=5)

# Manual command
async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    eth_price = get_eth_price()
    mmk_price = usd_to_mmk(eth_price)

    msg = f"💰 ETH: {eth_price} USD\n🇲🇲 MMK: {int(mmk_price)} Ks"
    await update.message.reply_text(msg)

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("price", price))

app.run_polling()
