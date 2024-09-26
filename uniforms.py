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


async def uniformcategories(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    entered_data = update.message.text
    reply_keyboard = [['⬅️ Назад']]
    if entered_data == '⬅️ Назад':
        context.user_data['page_number'] =0
        context.user_data['type'] = 9
        request_db = crud.get_branch_list(sphere_status=1)
        reply_keyboard = bot.transform_list(request_db,2,'name')
        reply_keyboard.insert(0,['⬅️ Назад'])
        reply_keyboard.append(['<<<Предыдущий','Следующий>>>'])
        await update.message.reply_text(f"Выберите филиал или отдел:",reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
        return bot.BRANCHES

    get_category = crud.getcategoryname(name=entered_data,department=context.user_data['type'])
    context.user_data['category'] = get_category.id
    context.user_data['category_name'] = get_category.name
    context.user_data['price'] = get_category.price
    uniformsizes = crud.get_products(category=entered_data)
    context.user_data['uniformsizes'] = uniformsizes
    reply_keyboard = bot.transform_list(uniformsizes,3,'name')
    reply_keyboard.append(['⬅️ Назад'])
    await update.message.reply_text('Выберите размер',reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
    return bot.UNIFORMSIZE
    # except:
    #     categories = crud.get_category_list(department=context.user_data['type'])
    #     reply_keyboard = bot.transform_list(categories,3,'name')
    #     reply_keyboard.append(['⬅️ Назад'])
    #
    #     await update.message.reply_text('Выберите тип формы',reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
    #     return bot.UNIFORMCATEGORIES

async def uniformsize(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    entered_data = update.message.text
    reply_keyboard = [['⬅️ Назад']]
    if entered_data == '⬅️ Назад':
        categories = crud.get_category_list(department=context.user_data['type'])
        reply_keyboard = bot.transform_list(categories, 3, 'name')
        reply_keyboard.append(['⬅️ Назад'])

        await update.message.reply_text('Выберите тип формы',
                                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
        return bot.UNIFORMCATEGORIES
    try:
        uniformsize = crud.get_product_by_name(entered_data,category=context.user_data['category'])
        if uniformsize:
            context.user_data['uniformsize'] = uniformsize.id
            context.user_data['uniformsize_name'] = uniformsize.name
            reply_keyboard = [['1','2','3'],['4','5','6'],['7','8','9'],['⬅️ Назад']]
            product_info = f"{context.user_data['category_name']} {entered_data} - {context.user_data['price']} сум"
            await update.message.reply_text(product_info+'\n\nВыберите количество',reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
            return bot.UNIFORMAMOUNT
        else:
            uniformsizes = crud.get_products(category=entered_data)
            reply_keyboard = bot.transform_list(uniformsizes, 3, 'name')
            reply_keyboard.append(['⬅️ Назад'])
            await update.message.reply_text('Выберите размер',
                                            reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
            return bot.UNIFORMSIZE
    except:
        uniformsizes = crud.get_products(category=entered_data)
        context.user_data['uniformsizes'] = uniformsizes
        reply_keyboard = bot.transform_list(uniformsizes, 3, 'name')
        reply_keyboard.append(['⬅️ Назад'])
        await update.message.reply_text('Выберите размер',
                                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
        return bot.UNIFORMSIZE


async def uniformamount(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    entered_data = update.message.text
    if entered_data == '⬅️ Назад':
        uniformsizes = context.user_data['uniformsizes']
        reply_keyboard = bot.transform_list(uniformsizes, 3, 'name')
        reply_keyboard.append(['⬅️ Назад'])
        await update.message.reply_text('Выберите размер',
                                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
        return bot.UNIFORMSIZE
    try:
        amount = int(entered_data)

        context.user_data['card'].append({'product_id':context.user_data['uniformsize'],'amount':amount,'price':context.user_data['price'],'category_name':context.user_data['category_name'],'uniformsize_name':context.user_data['uniformsize_name']})
        text_to_send = "Товар добавлен в корзину\n\n"
        total_summ = 0
        for item in context.user_data['card']:
            if item['price'] is not None:
                total_summ += item['price']*item['amount']
            product_info = f"{item['category_name']} {item['uniformsize_name']} - {item['price']} сум - {item['amount']} шт"
            text_to_send += product_info+'\n'
        text_to_send += f"\nИтого: {total_summ} сум"
        context.user_data['total_summ'] = total_summ
        await update.message.reply_text(text_to_send)
        reply_keyboard = [['Подтвердить',"Добавить еще"],['⬅️ Назад']]
        await update.message.reply_text('Выберите действие',reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
        return bot.UNIFORMVERIFY
    except:
        reply_keyboard = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9'], ['⬅️ Назад']]
        await update.message.reply_text('Укажите количество', reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
        return bot.UNIFORMAMOUNT

async def uniformverify(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    entered_data = update.message.text
    reply_keyboard = [['⬅️ Назад']]
    if entered_data == '⬅️ Назад':
        uniformsizes = context.user_data['uniformsizes']
        reply_keyboard = bot.transform_list(uniformsizes, 3, 'name')
        reply_keyboard.append(['⬅️ Назад'])
        await update.message.reply_text('Выберите размер',
                                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
        return bot.UNIFORMSIZE
    if entered_data == 'Подтвердить':
        text_to_send = """Укажите полное ФИО кому заказываете форму и должность сотрудника
(Как сотрудник получит форму, итоговая сумма будет списана с его заработной платы)"""
        reply_keyboard = [['⬅️ Назад']]
        await update.message.reply_text(text_to_send,
                                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
        return bot.UNIFORMNAME
    if entered_data == 'Добавить еще':
        categories = crud.get_category_list(department=context.user_data['type'])
        reply_keyboard = bot.transform_list(categories, 3, 'name')
        reply_keyboard.append(['⬅️ Назад'])

        await update.message.reply_text('Выберите тип формы',
                                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
        return bot.UNIFORMCATEGORIES
    else:
        reply_keyboard = [['Подтвердить', "Добавить еще"], ['⬅️ Назад']]
        await update.message.reply_text('Выберите действие', reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
        return bot.UNIFORMVERIFY


async def uniformname(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    entered_data = update.message.text
    context.user_data['name'] = entered_data
    reply_keyboard = [['⬅️ Назад']]
    if entered_data == '⬅️ Назад':
        reply_keyboard = [['Подтвердить', "Добавить еще"], ['⬅️ Назад']]
        await update.message.reply_text('Выберите действие', reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
        return bot.UNIFORMVERIFY
    try:
        user_query = crud.get_user_tel_id(id=update.message.from_user.id)
        fillial_query = crud.getchildbranch(fillial=context.user_data['branch'], type=int(context.user_data['type']),
                                            factory=1)
        fillial_id = fillial_query.id

        data = crud.add_uniform_request(user_id=user_query.id,category_id=context.user_data['category'],fillial_id=fillial_id, description=context.user_data['name'],total_cum=float(context.user_data['total_summ']))
        for i in context.user_data['card']:
            crud.add_uniform_product(request_id=data.id,product_id=i['product_id'],amount=i['amount'])
        await update.message.reply_text(f"Спасибо, ваша заявка #{data.id}s по форме принята.",reply_markup= ReplyKeyboardMarkup(bot.manu_buttons,resize_keyboard=True))
        return bot.MANU
    except Exception as e:
        text_to_send = """Укажите полное ФИО кому заказываете форму и должность сотрудника
(Как сотрудник получит форму, итоговая сумма будет списана с его заработной платы)"""
        await update.message.reply_text(text=text_to_send,reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
        return bot.UNIFORMNAME