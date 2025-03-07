#from bot import MEALSIZE, MEALBREADSIZE, MANU, transform_list,session,BRANCHES,manu_buttons
import re

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
import crud


async  def arc_factory_managers(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    entered_data = update.message.text
    if entered_data == '⬅️ Назад':
        await update.message.reply_text(f"Главное меню",
                                        reply_markup=ReplyKeyboardMarkup(bot.manu_buttons, resize_keyboard=True))
        return bot.MANU

    try:
        get_manager_divisions = crud.get_arc_factory_managers(name=entered_data)
        if get_manager_divisions:
            divisions = crud.get_manager_divisions(manager_id=get_manager_divisions[0].id)
            reply_keyboard = bot.transform_list(divisions, 2, 'name')
            reply_keyboard.append(['⬅️ Назад'])
            context.user_data['manager'] = get_manager_divisions[0].id
            await update.message.reply_text('Выберите отдел',reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
            return bot.ARCFACTORYDIVISIONS

    except:
        managers = crud.get_arc_factory_managers()
        reply_keyboard = bot.transform_list(managers, 2, 'name')
        reply_keyboard.append(['⬅️ Назад'])
        await update.message.reply_text('Выберите своего Бригадира:',reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
        return bot.ARCFACTORYMANAGER



async def arc_factory_divisions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    entered_data = update.message.text
    if entered_data == '⬅️ Назад':
        managers = crud.get_arc_factory_managers()
        reply_keyboard = bot.transform_list(managers, 2, 'name')
        reply_keyboard.append(['⬅️ Назад'])
        await update.message.reply_text('Выберите менеджера',reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
        return bot.ARCFACTORYMANAGER

    try:
        categories = crud.get_category_list(department=context.user_data['type'], sphere_status=2)
        reply_keyboard = bot.transform_list(categories, 2, 'name')
        reply_keyboard.append(['⬅️ Назад'])

        current_division = crud.get_manager_division_by_name(name=entered_data,manager_id=context.user_data['manager'])
        context.user_data['division_id'] = current_division.id
        if int(context.user_data['type']) == 10:
            category = crud.get_category_department(department_id=int(context.user_data['type']))
            context.user_data['category'] = category.name
            await update.message.reply_text('Пожалуйста укажите название/модель оборудования',
                                            reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
            return bot.PRODUCT

        await update.message.reply_text(f"Пожалуйста выберите категорию:",
                                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
        return bot.CATEGORY

    except Exception as e:
        await update.message.reply_text(str(e) + f"manager id {context.user_data['manager']}")
        divisions = crud.get_manager_divisions(manager_id=context.user_data['manager'])
        reply_keyboard = bot.transform_list(divisions, 2, 'name')
        reply_keyboard.append(['⬅️ Назад'])
        await update.message.reply_text('Выберите отдел',reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
        return bot.ARCFACTORYDIVISIONS


