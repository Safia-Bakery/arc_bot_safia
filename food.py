#from bot import MEALSIZE, MEALBREADSIZE, MANU, transform_list,session,BRANCHES,manu_buttons
import bot
import crud
from telegram import ReplyKeyboardMarkup,Update,WebAppInfo,KeyboardButton,InlineKeyboardMarkup,InlineKeyboardButton,ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,PicklePersistence
)

import pytz 
from datetime import datetime,timedelta

async def meal_size(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    entered_data = update.message.text
    reply_keyboard = [['⬅️ Назад']]
    if entered_data == '⬅️ Назад':
        context.user_data['page_number'] =0
        context.user_data['type'] = 6
        request_db = crud.get_branch_list(db=bot.session,sphere_status=1)
        reply_keyboard = bot.transform_list(request_db,2,'name')

        reply_keyboard.insert(0,['⬅️ Назад'])
        reply_keyboard.append(['<<<Предыдущий','Следующий>>>'])
        await update.message.reply_text(f"Выберите филиал или отдел:",reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
        
        return bot.BRANCHES
    try:
        meal_size = int(entered_data)
        context.user_data['meal_size'] = meal_size
        await update.message.reply_text('Укажите количество хлеба',reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
        return bot.MEALBREADSIZE
    except:
        await update.message.reply_text('Укажите количество порции еды',reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
        return bot.MEALSIZE
    

async def meal_bread_size(update:Update,context:ContextTypes.DEFAULT_TYPE) -> int:
    entered_data = update.message.text
    reply_keyboard = [['⬅️ Назад']]
    if entered_data =="⬅️ Назад":
        await update.message.reply_text('Укажите количество порции еды',reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
        return bot.MEALSIZE
    try:
        timezonetash = pytz.timezone("Asia/Tashkent")
        bread_size = int(entered_data)
        time_delivery = datetime.now(timezonetash)
        time_delivery = time_delivery + timedelta(days=1)
        next_day_noon = datetime(time_delivery.year, time_delivery.month, time_delivery.day, 12, 0, 0)
        fillial_query = crud.getchildbranch(db=bot.session,fillial=context.user_data['branch'],type=int(context.user_data['type']),factory=int(context.user_data['sphere_status']))
        user_query = crud.get_user_tel_id(db=bot.session,id=update.message.from_user.id)
        data = crud.add_meal_request(db=bot.session,fillial_id=fillial_query.id,user_id=user_query.id,bread_size=bread_size,meal_size=context.user_data['meal_size'],time_delivery=next_day_noon)
        await update.message.reply_text(f"Спасибо, ваша заявка №{data.id} по Запрос машины принята. Как ваша заявка будет назначена в работу ,вы получите уведомление.",reply_markup=ReplyKeyboardMarkup(bot.manu_buttons,resize_keyboard=True))
        return bot.MANU
    except:
        await update.message.reply_text('Укажите количество хлеба',reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
        return bot.MEALBREADSIZE


