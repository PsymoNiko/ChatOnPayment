
import os
from dotenv import load_dotenv

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

load_dotenv()
TOKEN = os.getenv("API_KEY")
WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")
print(TOKEN)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # First keyboard - TON Payment
    ton_keyboard = [
        [InlineKeyboardButton("Pay with Tonkeeper", url=f"ton://transfer/{WALLET_ADDRESS}?amount=5&text=ChannelAccess")]
    ]
    ton_reply_markup = InlineKeyboardMarkup(ton_keyboard)
    await update.message.reply_text(
        "Baraye dastrasi be channel, ba Tonkeeper pardakht kon:",
        reply_markup=ton_reply_markup
    )

    # Second keyboard - Website and Channel
    link_keyboard = [
        [InlineKeyboardButton("Visit My Website", url="https://alimohammadnia.ir")],
        [InlineKeyboardButton("Join My Channel", url="https://t.me/+hro1TmPhQks1OWVk")]
    ]
    link_reply_markup = InlineKeyboardMarkup(link_keyboard)
    await update.message.reply_text(
        "Salam! Baraye baz kardan safhe web ya join kardan channel rooye dokme click konid:",
        reply_markup=link_reply_markup
    )

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
