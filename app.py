import os
import asyncio
import logging
from dotenv import load_dotenv
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Load environment variables
load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')

# Enable logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Create the bot application
bot = Application.builder().token(TOKEN).build()

async def start(update: Update, context: CallbackContext) -> None:
    """Handles the /start command."""
    await update.message.reply_text('Hello! I am your auto-responder bot.')

async def auto_respond(update: Update, context: CallbackContext) -> None:
    """Auto-responds to any text message from any user except the bot itself."""
    user_id = update.message.from_user.id
    if user_id != bot.bot.id:  # Ensure the bot does not respond to itself
        await update.message.reply_text("Hi. I am currently AFK, I'll get back to you as soon as I can. Respectfully, Lana")

# Register handlers
bot.add_handler(CommandHandler("start", start))
bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_respond))

@app.route('/')
def home():
    """Home route to check if the server is running."""
    return "Telegram bot is running."

@app.route('/webhook', methods=['POST'])
async def webhook():
    """Handles incoming webhook requests from Telegram."""
    try:
        json_data = request.get_json()
        logge
