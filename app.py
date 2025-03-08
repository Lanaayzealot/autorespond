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
logger = logging.getLogger("app")

app = Flask(__name__)

# Initialize the bot application
bot = Application.builder().token(TOKEN).build()

# Define handlers for the bot
async def start(update: Update, context: CallbackContext) -> None:
    """Handles the /start command."""
    logger.info(f"Processing /start from {update.message.from_user.id}")
    await update.message.reply_text('Hello! I am your auto-responder bot.')

async def auto_respond(update: Update, context: CallbackContext) -> None:
    """Auto-responds to messages from a specific user."""
    user_id = update.message.from_user.id
    logger.info(f"Received message from {user_id}: {update.message.text}")

    if user_id == 7122508724:
        logger.info("Sending auto-response...")
        await update.message.reply_text("Hi. I am currently AFK, I'll get back to you as soon as I can. Respectfully, Lana")
    else:
        logger.info("Message ignored (not from the target user).")

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
        logger.info(f"Incoming Update: {json_data}")

        if not json_data:
            return 'Bad Request: No JSON received', 400

        update = Update.de_json(json_data, bot.bot)

        # Ensure the update is processed
        await bot.process_update(update)

        return 'OK', 200
    
    except Exception as e:
        logger.error(f"Error in Webhook: {e}", exc_info=True)
        return 'Internal Server Error', 500

async def main():
    """Initialize the bot and set up the webhook."""
    await bot.initialize()  # Ensure bot is properly initialized
    await bot.bot.set_webhook(WEBHOOK_URL)
    logger.info("Webhook set successfully!")

    # Run Flask app in an async event loop
    loop = asyncio.get_running_loop()
    loop.run_in_executor(None, app.run, "0.0.0.0", 5000)

if __name__ == '__main__':
    asyncio.run(main())  # Initialize bot and start the webhook
