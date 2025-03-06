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

print(f"✅ Loaded Bot Token: {TOKEN[:10]}...")  # Print partial token for security
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
    await update.message.reply_text("🚀 I am not available at the moment.")

# Stop command (only works locally or on a VPS)
async def stop(update: Update, context: CallbackContext):
    await update.message.reply_text("🔴 Bot is stopping...")
    sys.exit()

# Webhook route for Telegram
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(), telegram_app.bot)
    telegram_app.process_update(update)
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
    print("✅ Bot is running with webhook...")

if __name__ == "__main__":
    # Run the bot setup
    asyncio.run(main())

    # Start Flask server
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
