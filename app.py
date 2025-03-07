import os
import sys
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Load environment variables
TOKEN = os.getenv("TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = int(os.environ.get("PORT", 5000))

if not TOKEN or not WEBHOOK_URL:
    raise ValueError("❌ TOKEN or WEBHOOK_URL is not set. Check environment variables!")

print(f"✅ Loaded Bot Token: {TOKEN[:10]}...")  # Hide full token for security
print(f"✅ Webhook URL: {WEBHOOK_URL}")

# Flask app
app = Flask(__name__)

# Initialize Telegram bot application
telegram_app = Application.builder().token(TOKEN).build()

# Start command
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("🤖 Auto-reply bot is active!")

# Auto-reply to any message
async def auto_reply(update: Update, context: CallbackContext):
    await update.message.reply_text("🚀 I am not available at the moment.")

# Stop command (disables bot but keeps Flask running)
async def stop(update: Update, context: CallbackContext):
    await update.message.reply_text("🔴 Bot is stopping...")
    telegram_app.stop()
    print("❌ Bot stopped.")

# Webhook route for Telegram
@app.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    """Handle incoming Telegram updates."""
    update = Update.de_json(request.get_json(), telegram_app.bot)
    await telegram_app.process_update(update)
    return "OK", 200

async def set_webhook():
    """Function to set the webhook for the Telegram bot."""
    await telegram_app.bot.set_webhook(url=f"{WEBHOOK_URL}/{TOKEN}")
    print("✅ Webhook set successfully!")

async def run_bot():
    """Run bot initialization."""
    telegram_app.add_handler(CommandHandler("start", start))
    telegram_app.add_handler(CommandHandler("stop", stop))
    telegram_app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, auto_reply))

    # Set webhook
    await set_webhook()
    print("✅ Bot is running with webhook...")

# Start bot & Flask server
if __name__ == "__main__":
    asyncio.run(run_bot())  # Ensure bot starts properly
    app.run(host="0.0.0.0", port=PORT)
