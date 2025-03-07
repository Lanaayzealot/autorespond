import os
import sys
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Load environment variables
TOKEN = os.getenv("TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Ensure TOKEN is set
if not TOKEN:
    raise ValueError("❌ TOKEN is not set. Check environment variables!")

if not WEBHOOK_URL:
    raise ValueError("❌ WEBHOOK_URL is not set. Check environment variables!")

print(f"✅ Loaded Bot Token: {TOKEN[:10]}...")  # Be cautious with logging sensitive data
print(f"✅ Webhook URL: {WEBHOOK_URL}")

# Flask app
app = Flask(__name__)

# Initialize Telegram bot application
telegram_app = Application.builder().token(TOKEN).build()

# Start command
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("🤖 Auto-reply bot is active!")

# Auto-reply to any direct message
async def auto_reply(update: Update, context: CallbackContext):
    await update.message.reply_text("🚀 Hi, I am AFK right now, I will get back to you as soon as I can. Thank you!")

# Stop command (for debugging)
async def stop(update: Update, context: CallbackContext):
    await update.message.reply_text("🔴 Bot cannot be stopped remotely on Render.")

# Webhook route for Telegram
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(), telegram_app.bot)
    asyncio.run(telegram_app.process_update(update))  # Ensure async execution
    return "OK", 200

async def set_webhook():
    """Function to set the webhook for Telegram bot."""
    await telegram_app.bot.set_webhook(url=f"{WEBHOOK_URL}/{TOKEN}")
    print("✅ Webhook set successfully!")

async def main():
    """Function to initialize the bot and set up handlers."""
    telegram_app.add_handler(CommandHandler("start", start))
    telegram_app.add_handler(CommandHandler("stop", stop))
    telegram_app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, auto_reply))

    # Set webhook
    await set_webhook()

# Run the Flask app and bot setup asynchronously
if __name__ == "__main__":
    # Start Flask server
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

    print("✅ Bot is running with webhook...")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
