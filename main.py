from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from pygismeteo import Gismeteo


CITY, PERIOD = range(2)

city_req = str()

def start(update, _):
    update.message.reply_text(
        'Введите название города:\n'
        )
        
    return CITY

def city(update, _):
    global city_req
    city_req = update.message.text
    
    reply_keyboard = [['Текущая погода'], ['Прогноз на 3 дня'], ['Прогноз на 5 дней']]
    markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    update.message.reply_text(
        'Выберите период прогноза:\n',
        reply_markup=markup_key,)
    return PERIOD

def period(update, _):
    global city_req
    gismeteo = Gismeteo()
    period_req = update.message.text
    search_results = gismeteo.search.by_query(city_req)
    city_id = search_results[0].id
    if period_req == "Текущая погода":
        current = gismeteo.current.by_id(city_id)
        update.message.reply_text(f'{current.description.full}.\nТемпература воздуха: {current.temperature.air.c} C.'
        )
        
    elif period_req == "Прогноз на 3 дня":
        forecast = gismeteo.step24.by_id(city_id, days=3)
        for i in forecast:
            update.message.reply_text(f'{i.date.local}\n{i.description.full}.\nТемпература воздуха: {i.temperature.air.avg.c} C.\n'
            )
    else:
        forecast = gismeteo.step24.by_id(city_id, days=5)
        for i in forecast:
            update.message.reply_text(f'{i.date.local}\n{i.description.full}.\nТемпература воздуха: {i.temperature.air.avg.c} C.\n'
            )
        
    update.message.reply_text(
        '/start\n/cancel', 
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END
    

def cancel(update, _):
    update.reply_markup=ReplyKeyboardRemove()
    return ConversationHandler.END



updater = Updater('Токен')
    
dispatcher = updater.dispatcher

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        CITY: [MessageHandler(Filters.text & ~Filters.command, city)],
        PERIOD: [MessageHandler(Filters.regex('^(Текущая погода|Прогноз на 3 дня|Прогноз на 5 дней|Прогноз на 7 дней|Прогноз на 10 дней)$'), period)]
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)

dispatcher.add_handler(conv_handler)

updater.start_polling()
updater.idle()