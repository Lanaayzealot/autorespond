import os
from dotenv import load_dotenv
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')  # Should be set in .env (e.g., https://yourapp.onrender.com/webhook)

# Flask app instance
app = Flask(__name__)

# Initialize the Telegram bot
bot = Application.builder().token(TOKEN).build()

# Variable to track bot status (active or stopped)
bot_active = False  # Default is stopped

# Define handlers for the bot
async def start(update: Update, context: CallbackContext) -> None:
    """Handles the /start command and activates the bot."""
    global bot_active
    bot_active = True
    await update.message.reply_text('Hello! Auto-responder is now active.')

async def stop(update: Update, context: CallbackContext) -> None:
    """Handles the /stop command and stops auto-responses."""
    global bot_active
    bot_active = False
    await update.message.reply_text('Auto-responder is now stopped.')

async def auto_respond(update: Update, context: CallbackContext) -> None:
    """Auto-responds only if the bot is active and the sender is user ID 7122508724."""
    if bot_active and update.message.from_user.id == 7122508724:
        await update.message.reply_text("Hi. I am currently AFK, I'll get back to you as soon as I can. Respectfully, Lana")

# Register handlers
bot.add_handler(CommandHandler("start", start))
bot.add_handler(CommandHandler("stop", stop))
bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_respond))

# Flask route to handle webhook requests
@app.route('/webhook', methods=['POST'])
def webhook() -> str:
    """Handles incoming webhook requests from Telegram."""
    try:
        json_str = request.get_data(as_text=True)
        if not json_str:
            return 'No data received', 400  # Return 400 Bad Request if empty

        print("Incoming Update:", json_str)  # Debugging log
        update = Update.de_json(json_str, bot.bot)
        bot.process_update(update)
        return 'OK'
    except Exception as e:
        print("Error in Webhook:", str(e))
        return 'Internal Server Error', 500

@app.route('/')
def home() -> str:
    """Home route to check if the server is running."""
    return "Telegram bot is running."

def set_webhook() -> None:
    """Sets the webhook for the Telegram bot."""
    if WEBHOOK_URL:
        bot.bot.set_webhook(WEBHOOK_URL + "/webhook")
        print(f"Webhook set to: {WEBHOOK_URL}/webhook")

if __name__ == '__main__':
    set_webhook()
    app.run(host='0.0.0.0', port=5000)
