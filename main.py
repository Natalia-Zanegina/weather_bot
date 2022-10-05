from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from bot_commands import *

updater = Updater('5618333846:AAFXlZv4BeOBLhY8a88Cl-zFNspD47coDaY')

updater.dispatcher.add_handler(CommandHandler('weather', weather_command))

updater.start_polling()
updater.idle()
