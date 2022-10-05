from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from pygismeteo import Gismeteo


def weather_command(update: Update, context: CallbackContext):
    gismeteo = Gismeteo()
    msg = update.message.text
    items = msg.split()
    query = items[1]
    search_results = gismeteo.search.by_query(query)
    city_id = search_results[0].id
    current = gismeteo.current.by_id(city_id)
    update.message.reply_text(f'{current.description.full}. Температура воздуха: {current.temperature.air.c} C. Атмосферное давление: {current.pressure.mm_hg_atm} мм ртутного столба.')