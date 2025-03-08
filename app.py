import os
import json
from dotenv import load_dotenv
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')  # Your webhook URL

# Initialize Flask app
app = Flask(__name__)

# Initialize the bot application
bot = Application.builder().token(TOKEN).build()

# Bot state control
bot_running = False  # Initially, the bot is stopped

# Define handlers
async def start(update: Update, context: CallbackContext) -> None:
    """Handles the /start command and enables the bot."""
    global bot_running
    bot_running = True
    await update.message.reply_text('Hello! I am your auto-responder bot and now active.')

async def stop(update: Update, context: CallbackContext) -> None:
    """Handles the /stop command and disables the bot."""
    global bot_running
    bot_running = False
    await update.message.reply_text('The bot is now stopped. Send /start to activate again.')

async def auto_respond(update: Update, context: CallbackContext) -> None:
    """Auto-responds to messages if the bot is running and from a specific user."""
    if bot_running and update.message.from_user.id == 7122508724:
        await update.message.reply_text("Hi. I am currently AFK, I'll get back to you as soon as I can. Respectfully, Lana")

# Register handlers
bot.add_handler(CommandHandler("start", start))
bot.add_handler(CommandHandler("stop", stop))
bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_respond))

# Webhook route
@app.route('/webhook', methods=['POST'])
def webhook() -> str:
    """Handles incoming webhook requests from Telegram."""
    try:
        json_str = request.get_data(as_text=True)
        if not json_str:
            return 'No data received', 400  # Bad Request

        data = json.loads(json_str)  # Convert JSON string to dictionary
        print("Incoming Update:", data)  # Debugging log

        update = Update.de_json(data, bot.bot)  # Convert to Telegram update object
        bot.process_update(update)

        return 'OK'
    except Exception as e:
        print("Error in Webhook:", str(e))
        return 'Internal Server Error', 500

# Set webhook function
def set_webhook() -> None:
    """Sets the webhook for the Telegram bot."""
    bot.bot.set_webhook(WEBHOOK_URL)

# Home route for server status check
@app.route('/')
def home() -> str:
    """Simple route to check if the server is running."""
    return "Telegram bot is running."

# Run the app
if __name__ == '__main__':
    set_webhook()
    app.run(host='0.0.0.0', port=5000)
