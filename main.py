import telegram.ext
from dotenv import load_dotenv
import os
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler
from connection import mdb  
from functions import *  

# Load environment variables from a .env file
load_dotenv()
TOKEN = os.getenv("TOKEN")

# Create the application and pass the bot token
application = Application.builder().token(TOKEN).build()

# Add the command handlers to the application
application.add_handler(CommandHandler('start', start))
application.add_handler(ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('Blood Sugar Level'), sugarLevel),],
    states={
        "sugarLevel": [MessageHandler(filters.TEXT, getLevel)],
        "timeSelect":[MessageHandler(filters.TEXT, timeSelection)],
        "timem": [MessageHandler(filters.TEXT, getDateTime)]
    },
    fallbacks=[]
))



# Start the bot
application.run_polling()








