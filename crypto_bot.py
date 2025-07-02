import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TELEGRAM_BOT_TOKEN = "7607019510:AAFUEV2XxBCc6bYYVeY8gmCxVgrJg9UvERk"

COINGECKO_API_URL = "https://api.coingecko.com/api/v3/simple/price"
coins = ["bitcoin", "ethereum", "binancecoin", "dogecoin", "ripple"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 مرحبًا بك في Crypto Daily Alerts Bot!\n"
        "اكتب /prices لعرض أسعار أهم العملات.\n"
        "اكتب /help لمزيد من الأوامر."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/prices - يعرض أسعار العملات\n"
        "/help - يعرض هذه الرسالة"
    )

async def prices(update: Update, context: ContextTypes.DEFAULT_TYPE):
    symbols = ",".join(coins)
    url = f"{COINGECKO_API_URL}?ids={symbols}&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    
    message = "💰 **أسعار العملات اليوم:**\n"
    for coin in coins:
        price = data[coin]["usd"]
        message += f"• {coin.capitalize()}: ${price}\n"
    
    await update.message.reply_text(message, parse_mode="Markdown")

# تنبيه تلقائي لو سعر بيتكوين نزل عن 100,000$
async def check_btc_alert(context: ContextTypes.DEFAULT_TYPE):
    url = f"{COINGECKO_API_URL}?ids=bitcoin&vs_currencies=usd"
    response = requests.get(url)
    price = response.json()["bitcoin"]["usd"]
    if price < 100000:
        await context.bot.send_message(
            chat_id=context.job.chat_id,
            text=f"🚨 تنبيه: سعر البيتكوين الآن ${price} (أقل من 100,000$!)"
        )

async def set_alert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    context.job_queue.run_repeating(check_btc_alert, interval=3600, first=10, chat_id=chat_id)
    await update.message.reply_text("✅ تم تفعيل تنبيه بيتكوين كل ساعة إذا نزل عن 100,000$.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(7607019510:AAFUEV2XxBCc6bYYVeY8gmCxVgrJg9UvERk).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("prices", prices))
    app.add_handler(CommandHandler("setalert", set_alert))

    print("🤖 البوت شغال...")
    app.run_polling()