import os
from dotenv import load_dotenv
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')  # URL for your webhook (e.g., https://yourdomain.com/webhook)

app = Flask(__name__)

# Initialize the bot application
bot = Application.builder().token(TOKEN).build()

# Define handlers for the bot
async def start(update: Update, context: CallbackContext) -> None:
    """Handles the /start command."""
    update.message.reply_text('Hello! I am your auto-responder bot.')

async def auto_respond(update: Update, context: CallbackContext) -> None:
    """Auto-responds to any text message."""
    # Check if the message contains the word 'Lana' (case-insensitive)
    if 'lana' in update.message.text.lower():
        update.message.reply_text('I am AFK at the moment. I will get back to you as soon as I can!')

# Register handlers
bot.add_handler(CommandHandler("start", start))
bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_respond))

# Flask route to handle the webhook requests
@app.route('/webhook', methods=['POST'])
def webhook() -> str:
    """Handles incoming webhook requests from Telegram."""
    json_str = request.get_data().decode('UTF-8')
    update = Update.de_json(json_str, bot.bot)
    bot.process_update(update)
    return 'OK'

def set_webhook() -> None:
    """Sets the webhook for the Telegram bot."""
    bot.bot.set_webhook(WEBHOOK_URL)

@app.route('/')
def home() -> str:
    """Home route to check if the server is running."""
    return "Telegram bot is running."

if __name__ == '__main__':
    set_webhook()
    app.run(host='0.0.0.0', port=5000)
