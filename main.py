import telegram.ext
from dotenv import load_dotenv
import os
from telegram.ext import Application, CommandHandler,MessageHandler,filters

# Load environment variables from a .env file
load_dotenv()
TOKEN = os.getenv("TOKEN")

# Define the start command handler
async def start(update, context):
    await update.message.reply_text("Hello, {}!".format(update.message.chat.first_name))


# Define the help command handler
async def helps(update, context):
    await update.message.reply_text("h")

# Create the application and pass the bot token
application = Application.builder().token(TOKEN).build()

# Add the command handlers to the application
application.add_handler(CommandHandler('start', start))
application.add_handler(CommandHandler('help', helps))
application.add_handler(MessageHandler(filters.Regex('start'),start))
# Start the bot
application.run_polling()







