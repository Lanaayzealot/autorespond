import os
import asyncio
from dotenv import load_dotenv
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import traceback

# Load environment variables
load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')

app = Flask(__name__)

# Initialize the bot application
bot = Application.builder().token(TOKEN).build()

# Define handlers for the bot
async def start(update: Update, context: CallbackContext) -> None:
    """Handles the /start command."""
    await update.message.reply_text('Hello! I am your auto-responder bot.')

async def auto_respond(update: Update, context: CallbackContext) -> None:
    """Auto-responds to any text message from the user with ID 7122508724."""
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
async def webhook() -> str:
    """Handles incoming webhook requests from Telegram."""
    try:
        json_data = request.get_json()
        print("Incoming Update:", json_data)  # Debugging line

        if json_data is None:
            raise ValueError("Invalid JSON data")

        update = Update.de_json(json_data, bot.bot)

        # Use `bot.update_queue.put()` instead of `bot.process_update(update)`
        await bot.update_queue.put(update)

        # Send a reply to the user for any incoming message
        if update.message:
            chat_id = update.message.chat.id
            text = update.message.text
            # Respond to the user based on the received message
            if text.lower() == "/start":
                await bot.bot.send_message(chat_id=chat_id, text="Welcome! How can I help you?")
            else:
                await bot.bot.send_message(chat_id=chat_id, text="Hello, I received your message!")

        return 'OK'
    
    except Exception as e:
        print("Error in Webhook:", str(e))
        print("Traceback:", traceback.format_exc())
        return 'Internal Server Error', 500

def set_webhook() -> None:
    """Sets the webhook for the Telegram bot."""
    asyncio.run(bot.bot.set_webhook(WEBHOOK_URL))

if __name__ == '__main__':
    set_webhook()
    app.run(host='0.0.0.0', port=5000)
