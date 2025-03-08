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

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Initialize the bot application
bot = Application.builder().token(TOKEN).build()

# Define handlers for the bot
async def start(update: Update, context: CallbackContext) -> None:
    """Handles the /start command."""
    await update.message.reply_text('Hello! I am your auto-responder bot.')

async def auto_respond(update: Update, context: CallbackContext) -> None:
    """Auto-responds to a specific user ID."""
    if update.message.from_user.id == 7122508724:
        await update.message.reply_text("Hi. I am currently AFK, I'll get back to you as soon as I can. Respectfully, Lana")

# Register handlers
bot.add_handler(CommandHandler("start", start))
bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_respond))

@app.route('/')
def home() -> str:
    """Home route to check if the server is running."""
    return "Telegram bot is running."

@app.route('/webhook', methods=['POST'])
async def webhook() -> tuple[str, int]:
    """Handles incoming webhook requests from Telegram."""
    try:
        json_data = request.get_json()
        logger.info(f"Incoming Update: {json_data}")  # Logging for debugging

        if not json_data:
            return 'Bad Request: No JSON received', 400

        update = Update.de_json(json_data, bot.bot)

        # Queue the update for async processing
        await bot.update_queue.put(update)

        return 'OK', 200
    
    except Exception as e:
        logger.error(f"Error in Webhook: {e}", exc_info=True)
        return 'Internal Server Error', 500

async def set_webhook() -> None:
    """Sets the webhook for the Telegram bot asynchronously."""
    try:
        success = await bot.bot.set_webhook(WEBHOOK_URL)
        if success:
            logger.info("Webhook set successfully!")
        else:
            logger.error("Failed to set webhook.")
    except Exception as e:
        logger.error(f"Error setting webhook: {e}", exc_info=True)

if __name__ == '__main__':
    # Start webhook setup before running the Flask app
    asyncio.run(set_webhook())  # Properly runs the async webhook setup
    app.run(host='0.0.0.0', port=5000)  # Run the Flask app
