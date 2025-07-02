import os
import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# احصل على التوكن من متغير البيئة
TELEGRAM_BOT_TOKEN = os.getenv("7607019510:AAFUEV2XxBCc6bYYVeY8gmCxVgrJg9UvERk")

# رابط CoinGecko API
COINGECKO_API_URL = "https://api.coingecko.com/api/v3/simple/price"
coins = ["bitcoin", "ethereum", "binancecoin", "dogecoin", "ripple"]

# دالة /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 مرحبًا بك في *Crypto Daily Alerts Bot*!\n"
        "اكتب /help لرؤية قائمة الأوامر المتاحة.",
        parse_mode="Markdown"
    )

# دالة /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📝 *قائمة الأوامر:*\n"
        "/start - بدء تشغيل البوت\n"
        "/help - عرض قائمة الأوامر\n"
        "/prices - أسعار العملات الرقمية\n"
        "/setalert - تنبيه سعر البيتكوين\n"
        "/about - معلومات عن البوت\n"
        "/top - العملات الأكثر تداولًا\n"
        "/convert 0.1 - تحويل BTC إلى الدولار\n"
        "/news - أحدث الأخبار",
        parse_mode="Markdown"
    )

# دالة /prices
async def prices(update: Update, context: ContextTypes.DEFAULT_TYPE):
    symbols = ",".join(coins)
    url = f"{COINGECKO_API_URL}?ids={symbols}&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    message = "💰 *أسعار العملات الآن:*\n"
    for coin in coins:
        price = data[coin]["usd"]
        message += f"• {coin.capitalize()}: ${price}\n"
    await update.message.reply_text(message, parse_mode="Markdown")

# دالة تنبيه بيتكوين
async def check_btc_alert(context: ContextTypes.DEFAULT_TYPE):
    url = f"{COINGECKO_API_URL}?ids=bitcoin&vs_currencies=usd"
    response = requests.get(url)
    price = response.json()["bitcoin"]["usd"]
    if price < 30000:
        await context.bot.send_message(
            chat_id=context.job.chat_id,
            text=f"🚨 تنبيه: سعر البيتكوين الآن ${price} (أقل من 30,000$!)"
        )

# دالة /setalert
async def setalert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    context.job_queue.run_repeating(
        check_btc_alert, interval=3600, first=10, chat_id=chat_id
    )
    await update.message.reply_text("✅ تم تفعيل تنبيه البيتكوين كل ساعة.")

# دالة /about
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 *Crypto Daily Alerts Bot*\n"
        "يعرض لك أسعار العملات الرقمية، تنبيهات وتحليلات.\n"
        "تم تطويره باستخدام CoinGecko API.",
        parse_mode="Markdown"
    )

# دالة /top
async def top(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌟 العملات الأكثر تداولًا حاليًا:\n"
        "1. Bitcoin\n"
        "2. Ethereum\n"
        "3. Binance Coin\n"
        "4. XRP\n"
        "5. Solana"
    )

# دالة /convert
async def convert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if len(context.args) != 1:
            await update.message.reply_text("💡 استعمل:\n/convert 0.1")
            return
        btc_amount = float(context.args[0])
        url = f"{COINGECKO_API_URL}?ids=bitcoin&vs_currencies=usd"
        response = requests.get(url)
        price = response.json()["bitcoin"]["usd"]
        converted = btc_amount * price
        await update.message.reply_text(
            f"🔄 {btc_amount} BTC = ${converted:.2f} USD"
        )
    except:
        await update.message.reply_text("❌ خطأ في الصيغة، جرب مجددًا.")

# دالة /news
async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "📰 *أحدث الأخبار (مثال ثابت):*\n"
        "- البيتكوين يحافظ على سعر فوق 30,000$\n"
        "- الاثيريوم يحقق نمو 2%\n"
        "- المزيد قريبًا..."
    )
    await update.message.reply_text(message, parse_mode="Markdown")

# تشغيل التطبيق
if __name__ == "__main__":
    app = ApplicationBuilder().token(7607019510:AAFUEV2XxBCc6bYYVeY8gmCxVgrJg9UvERk).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("prices", prices))
    app.add_handler(CommandHandler("setalert", setalert))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CommandHandler("top", top))
    app.add_handler(CommandHandler("convert", convert))
    app.add_handler(CommandHandler("news", news))

    print("🤖 البوت جاهز ويعمل الآن...")
    app.run_polling()