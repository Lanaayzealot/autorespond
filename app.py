import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Retrieve the TOKEN and WEBHOOK_URL from environment variables
TOKEN = os.getenv("TOKEN")  # Your bot's token
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # The URL for your deployed Flask app

# Flask app
app = Flask(__name__)

# Initialize Telegram bot with the token
telegram_app = Application.builder().token(TOKEN).build()

# Start command handler
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("🤖 Auto-reply bot is active!")

# Auto-reply to any direct message
async def auto_reply(update: Update, context: CallbackContext):
    await update.message.reply_text("Hi, I am AFK right now, I will get back to you as soon as I can. Thank you!")

# Stop command (for testing, e.g., to stop the bot locally or for a clean shutdown)
async def stop(update: Update, context: CallbackContext):
    await update.message.reply_text("🔴 Bot is stopping...")

# Webhook route for Telegram (using the token in the route)
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()
    print(f"📩 Received Update: {data}")  # Log the received update for debugging
    update = Update.de_json(data, telegram_app.bot)
    telegram_app.create_task(telegram_app.process_update(update))  # Process the update
    return "OK", 200

# Set the webhook URL for Telegram
async def set_webhook():
    webhook_url = f"{WEBHOOK_URL}/{TOKEN}"
    await telegram_app.bot.set_webhook(url=webhook_url)
    print(f"✅ Webhook set to {webhook_url}")

# Run bot setup and add handlers
async def run_bot():
    telegram_app.add_handler(CommandHandler("start", start))
    telegram_app.add_handler(CommandHandler("stop", stop))
    telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply))

    # Set the webhook after handlers are added
    await set_webhook()
    print("🤖 Bot is running with webhook...")

# Main function to start everything
def main():
    telegram_app.loop.run_until_complete(run_bot())  # Set up webhook and start the bot
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))  # Start Flask server

if __name__ == "__main__":
    main()
