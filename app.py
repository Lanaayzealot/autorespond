import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Load environment variables
TOKEN = os.getenv("TOKEN")  # Bot Token from BotFather
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Your webhook URL
PORT = int(os.environ.get("PORT", 10000))  # Default port

# Flask app
app = Flask(__name__)

# Initialize Telegram bot
telegram_app = Application.builder().token(TOKEN).build()

# Start command
async def start(update: Update, context):
    await update.message.reply_text("🤖 Auto-reply bot is active!")

# Auto-reply to any direct message
async def auto_reply(update: Update, context):
    await update.message.reply_text("Hi, I am AFK right now, I will get back to you as soon as I can. Thank you!")

# Stop command (only works locally or on a VPS)
async def stop(update: Update, context):
    await update.message.reply_text("🔴 Bot is stopping...")

# Webhook route for Telegram
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()
    print("📩 Received Update:", data)  # Debugging line to check if updates are received
    update = Update.de_json(data, telegram_app.bot)
    telegram_app.create_task(telegram_app.process_update(update))  # Process update immediately
    return "OK", 200

async def set_webhook():
    await telegram_app.bot.set_webhook(url=f"{WEBHOOK_URL}/{TOKEN}")
    print("✅ Webhook set successfully.")

async def run_bot():
    # Add handlers for commands and messages
    telegram_app.add_handler(CommandHandler("start", start))
    telegram_app.add_handler(CommandHandler("stop", stop))
    telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply))

    await set_webhook()  # Set webhook AFTER adding handlers
    print("🤖 Bot is running with webhook...")

def main():
    # Run bot setup and start Flask server
    telegram_app.loop.run_until_complete(run_bot())
    app.run(host="0.0.0.0", port=PORT)  # Start Flask server

if __name__ == "__main__":
    main()
