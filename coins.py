#from bot import CHOOSESIZE,CHOOSEDAY,CHOOSEMONTH,INPUTIMAGECAR,COMMENTCAR,MANU,CHOOSEHOUR,manu_buttons,backend_location,CATEGORY,session,transform_list
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

from microser import transform_list

import datetime
import calendar
from dotenv import load_dotenv
import os

default_coin_category = os.environ.get('DEFAULT_COIN_CATEGORY')


async def coin_amount(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    input_text = update.message.text
    if input_text == '⬅️ Назад':
        request_db = crud.get_branch_list(sphere_status=1)
        reply_keyboard = transform_list(request_db, 2, 'name')
        reply_keyboard.insert(0, ['⬅️ Назад'])
        reply_keyboard.append(['<<<Предыдущий', 'Следующий>>>'])
        await update.message.reply_text(f"Выберите филиал или отдел:",
                                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
        return bot.BRANCHES
    try:
        input_value = int(input_text)
        context.user_data['amount'] = input_value
        reply_keyboard = [['⬅️ Назад']]
        await update.message.reply_text('Пожалуйста, введите описание, например, количество монет в соответствии с их номиналом. Укажите номинал монеты и количество. Например: мне нужно 200 монет номиналом 100 сумов.',
                                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
        return bot.COINDESCRIPTION
    except:
        reply_keyboard = [['⬅️ Назад']]

        await  update.message.reply_text(
            'Неверный формат, пожалуйста, введите в числовом формате.',
        reply_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
        return bot.COINAMOUNT



async def coin_description(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    input_text = update.message.text
    if input_text=='⬅️ Назад':
        reply_keyboard = [['⬅️ Назад']]
        await update.message.reply_text('Пожалуйста, введите количество монет в числовом формате.',
                                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
        return bot.COINAMOUNT

    user_query = crud.get_user_tel_id(id=update.message.from_user.id)
    fillial_query = crud.getchildbranch(fillial=context.user_data['branch'], type=int(context.user_data['type']),
                                        factory=1)
    fillial_id = fillial_query.id


    data = crud.create_coint_request(
        user_id=user_query.id,
        category=default_coin_category,
        branch_id=fillial_id,
        description=input_text,
        amount=context.user_data['amount']
                                     )

    reply_text = f"Спасибо, ваш заявка #{data.id}s на заказ монет принят."



    await update.message.reply_text(reply_text,
                                    reply_markup=ReplyKeyboardMarkup(bot.manu_buttons, resize_keyboard=True))
    return bot.MANU

