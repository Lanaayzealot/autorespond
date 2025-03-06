import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Bot Token from BotFather
TOKEN = os.getenv("TOKEN")  # Use environment variable for security
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Your Render app URL

# Flask app
app = Flask(__name__)

# Initialize Telegram bot
telegram_app = Application.builder().token(TOKEN).build()

# Start command
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("🤖 Auto-reply bot is active!")

# Auto-reply to any direct message
async def auto_reply(update: Update, context: CallbackContext):
    await update.message.reply_text("🚀 I am not available at the moment.")

# Stop command (only works locally or on a VPS)
async def stop(update: Update, context: CallbackContext):
    await update.message.reply_text("🔴 Bot is stopping...")

# Webhook route for Telegram
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(), telegram_app.bot)
    telegram_app.process_update(update)
    return "OK", 200

def main():
    # Add handlers
    telegram_app.add_handler(CommandHandler("start", start))
    telegram_app.add_handler(CommandHandler("stop", stop))
    telegram_app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, auto_reply))

    # Set webhook for Telegram (Ensure your Render app URL is correctly configured)
    telegram_app.bot.set_webhook(url=f"{WEBHOOK_URL}/{TOKEN}")
    print("✅ Bot is running with webhook...")

    # Start Flask server
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

if __name__ == "__main__":
    main()
