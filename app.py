import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')

async def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! I am your auto-responder bot.')

async def auto_respond(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('I am AFK at the moment. I will get back to you as soon as I can!')

def main() -> None:
    # Initialize the bot application
    app = Application.builder().token(TOKEN).build()

    # Register handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_respond))

    # Start polling
    app.run_polling()

if __name__ == '__main__':
    main()
