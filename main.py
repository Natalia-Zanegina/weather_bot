from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from bot_commands import *

updater = Updater('Токен')

updater.dispatcher.add_handler(CommandHandler('weather', weather_command))

updater.start_polling()
updater.idle()
