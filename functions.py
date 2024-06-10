from dotenv import load_dotenv
import os
from telegram.ext import Application, CommandHandler,MessageHandler,filters,ConversationHandler
from telegram import ReplyKeyboardMarkup,ReplyKeyboardRemove
from connection import mdb,searchorsave,saveBloodLevel
from datetime import datetime,timezone


main_keyboard = ReplyKeyboardMarkup(
    [['Blood Sugar Level', 'Well-being'], ['Food', 'Medications'], ['Exercise']],
    resize_keyboard=True
)
async def start(bot,update):
    searchorsave(mdb,bot.effective_user,bot.message)
    await bot.message.reply_text("Hello, {}!".format(bot.message.chat.first_name),reply_markup=main_keyboard)


# Define the help command handler
async def sugarLevel(update,context):
    await update.message.reply_text("What is the value?",reply_markup=ReplyKeyboardRemove())
    return "sugarLevel"

async def getLevel(update,context):
    context.user_data['sugarLevel'] = update.message.text
    my_keyboard = ReplyKeyboardMarkup([['Just Now', 'Before']], resize_keyboard=True)
    await update.message.reply_text(
        "When was the value measured?", reply_markup=my_keyboard
    )
    return "timeSelect"

async def timeSelection(update, context):
    user_choice = update.message.text
    if user_choice == "Just Now":
        context.user_data['date_time'] = datetime.now(timezone.utc)
        saveBloodLevel(mdb, update.effective_user, context.user_data['sugarLevel'], context.user_data['date_time'])
        await update.message.reply_text("Blood sugar level and current date-time saved.",reply_markup=main_keyboard)
        return ConversationHandler.END
    elif user_choice == "Before":
        await update.message.reply_text(
            "Please provide the date and time for this reading (YYYY-MM-DD HH:MM):",
            reply_markup=ReplyKeyboardRemove()
        )
        return "timem"

async def getDateTime(update, context):
    timemstr = update.message.text
    try:
        timem = datetime.strptime(timemstr, '%Y-%m-%d %H:%M')
        context.user_data['timem'] = timem
        saveBloodLevel(mdb, update.effective_user, context.user_data['sugarLevel'], context.user_data['timem'])
        await update.message.reply_text("Blood sugar level and date-time saved.",reply_markup=main_keyboard)
        return ConversationHandler.END
    except ValueError:
        await update.message.reply_text("Invalid date-time format. Please enter the date and time in YYYY-MM-DD HH:MM format:")
        return "timem"