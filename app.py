import os
from dotenv import load_dotenv
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import traceback

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
    """Auto-responds to any text message from the user with ID 7122508724."""
    # Check if the message is from the user with ID 7122508724
    if update.message.from_user.id == 7122508724:
        # Send auto-response message
        update.message.reply_text("Hi. I am currently AFK, I'll get back to you as soon as I can. Respectfully, Lana")

# Register handlers
bot.add_handler(CommandHandler("start", start))
bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_respond))

@app.route('/webhook', methods=['POST'])
def webhook() -> str:
    """Handles incoming webhook requests from Telegram."""
    try:
        # Use Flask's request.get_json() to parse JSON data into a dictionary
        json_data = request.get_json()
        print("Incoming Update:", json_data)  # Debugging line

        if json_data is None:
            raise ValueError("Invalid JSON data")

        # Create the Update object using the parsed JSON data
        update = Update.de_json(json_data, bot.bot)
        
        # Process the update with the bot
        bot.process_update(update)
        return 'OK'
    
    except Exception as e:
        print("Error in Webhook:", str(e))
        print("Traceback:", traceback.format_exc())  # Print traceback for more detailed error logs
        return 'Internal Server Error', 500

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
