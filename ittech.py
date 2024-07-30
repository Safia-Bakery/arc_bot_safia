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
from microser import transform_list,sendtotelegram
BASE_URL = 'https://api.service.safiabakery.uz/'
import datetime
import calendar
import re
import pytz
timezonetash = pytz.timezone("Asia/Tashkent")
import os
from dotenv import load_dotenv
load_dotenv()
BOTTOKEN = os.environ.get('BOT_TOKEN')

async def it_sphere(update:Update,context:ContextTypes.DEFAULT_TYPE) ->int:
    user_mess = update.message.text
    if user_mess == '⬅️ Назад':
        await update.message.reply_text('Пожалуйста выберите направление:',reply_markup=ReplyKeyboardMarkup(keyboard=bot.manu_buttons,resize_keyboard=True))
        return bot.MANU
    context.user_data['itsphere'] = user_mess
    if user_mess == "Закуп":
        context.user_data['productd'] = {}
        data = crud.get_category_list(department=4,sphere_status=3)
        reply_keyboard = transform_list(data,3,'name')
        reply_keyboard.append(['⬅️ Назад'])
        await update.message.reply_text('Выберите категорию',reply_markup=ReplyKeyboardMarkup(keyboard=reply_keyboard,resize_keyboard=True))
    elif user_mess=='Обслуживание и тех.поддержка':
        data = crud.get_category_list(department=4,sphere_status=4)
        reply_keyboard = transform_list(data,3,'name')
        reply_keyboard.append(['⬅️ Назад'])
        await update.message.reply_text('Выберите категорию заявки',reply_markup=ReplyKeyboardMarkup(keyboard=reply_keyboard,resize_keyboard=True))
    else:
        reply_keyboard=[['Обслуживание и тех.поддержка','Закуп']]
        await update.message.reply_text('Выберите тип заявки:',reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
        return bot.ITSPHERE
    return bot.ITCATEGORY


async def it_category(update:Update,context:ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == '⬅️ Назад':
        await update.message.reply_text('Пожалуйста выберите направление:',reply_markup=ReplyKeyboardMarkup(keyboard=bot.manu_buttons,resize_keyboard=True))
        return bot.MANU
    if update.message.text == 'Перейти в корзину':
        if not bool(context.user_data['productd']):
            data = crud.get_category_list(department=4,sphere_status=3)
            reply_keyboard = transform_list(data,3,'name')
            reply_keyboard.append(['⬅️ Назад'])
            await update.message.reply_text('Ваша корзина пуста',reply_markup=ReplyKeyboardMarkup(keyboard=reply_keyboard,resize_keyboard=True))
            return bot.ITCATEGORY
        reply_keyboard = [['⬅️ Назад']]
        await update.message.reply_text(f"Введите комментарии к заявке",reply_markup=ReplyKeyboardMarkup(keyboard=reply_keyboard,resize_keyboard=True))
        return bot.ITCOMMENT
    user_cat = update.message.text
    context.user_data['category'] = user_cat
    if context.user_data['itsphere'] =='Закуп':
        query = crud.get_products(category=user_cat)
        if not query:
            data = crud.get_category_list(department=4,sphere_status=3)
            reply_keyboard = transform_list(data,3,'name')
            reply_keyboard.append(['⬅️ Назад'])
            await update.message.reply_text('Выберите категорию',reply_markup=ReplyKeyboardMarkup(keyboard=reply_keyboard,resize_keyboard=True))
            return bot.ITCATEGORY
        reply_keyboard = transform_list(query,3,'name')
        reply_keyboard.append(['⬅️ Назад'])

        await update.message.reply_text('Выберите товар',reply_markup=ReplyKeyboardMarkup(keyboard=reply_keyboard,resize_keyboard=True))
        return bot.ITPRODUCTS
    if context.user_data['itsphere'] =='Обслуживание и тех.поддержка':
        reply_keyboard = [['⬅️ Назад']]
        await update.message.reply_text('Введите комментарии к заявке',reply_markup=ReplyKeyboardMarkup(keyboard=reply_keyboard,resize_keyboard=True))
        return bot.ITCOMMENT

async def it_products(update:Update,context:ContextTypes.DEFAULT_TYPE) -> int:
    user_prod = update.message.text
    if user_prod == '⬅️ Назад':
        data = crud.get_category_list(department=4,sphere_status=3)
        reply_keyboard = transform_list(data,3,'name')
        reply_keyboard.append(['⬅️ Назад','Перейти в корзину'])
        await update.message.reply_text('Выберите категорию',reply_markup=ReplyKeyboardMarkup(keyboard=reply_keyboard,resize_keyboard=True))
        return bot.ITCATEGORY
    #context.user_data['productd'] = {}
    user_prod = update.message.text
    context.user_data['product'] = user_prod
    reply_keyboard = [['1','2','3'],['4','5','6'],['7','8','9'],['⬅️ Назад']]
    await update.message.reply_text('Выберите или введите количество:',reply_markup=ReplyKeyboardMarkup(keyboard=reply_keyboard,resize_keyboard=True))
    return bot.ITAMOUNT

async def it_amount(update:Update,context:ContextTypes.DEFAULT_TYPE) -> int:
    user_amount = update.message.text
    if user_amount == '⬅️ Назад':
        query = crud.get_products(category=context.user_data['category'])
        reply_keyboard = transform_list(query,3,'name')
        reply_keyboard.append(['⬅️ Назад'])
        await update.message.reply_text('Выберите товар',reply_markup=ReplyKeyboardMarkup(keyboard=reply_keyboard,resize_keyboard=True))
        return bot.ITPRODUCTS
    user_amount = re.findall('\d+', user_amount)
    if not user_amount:
        reply_keyboard = [['1','2','3'],['4','5','6'],['7','8','9'],['⬅️ Назад']]
        await update.message.reply_text('Выберите или введите количество:',reply_markup=ReplyKeyboardMarkup(keyboard=reply_keyboard,resize_keyboard=True))
        return bot.ITAMOUNT
    user_amount = int(user_amount[0])
    context.user_data['amount'] = user_amount
    products = context.user_data['productd']
    products[context.user_data['product']]=user_amount
    context.user_data['productd']=  products
    text = ''
    for key,val in products.items():
        text = text+f"{key} - {val}\n"
    #reply_keyboard= [['Yes','No']]
    #await update.message.reply_text('please enter comment',reply_markup=ReplyKeyboardMarkup(keyboard=reply_keyboard,resize_keyboard=True))
    data = crud.get_category_list(department=4,sphere_status=3)
    reply_keyboard = transform_list(data,3,'name')
    reply_keyboard.append(['⬅️ Назад','Перейти в корзину'])
    await update.message.reply_text(text,reply_markup=ReplyKeyboardMarkup(keyboard=reply_keyboard,resize_keyboard=True))
    return bot.ITCATEGORY






    
async def it_comment(update:Update,context:ContextTypes.DEFAULT_TYPE) -> int:
    user_comment = update.message.text
    if user_comment == '⬅️ Назад':
        if context.user_data['itsphere'] =='Закуп':
            data = crud.get_category_list(department=4,sphere_status=3)
            reply_keyboard = transform_list(data,3,'name')
            reply_keyboard.append(['⬅️ Назад'])
            await update.message.reply_text('Выберите категорию',reply_markup=ReplyKeyboardMarkup(keyboard=reply_keyboard,resize_keyboard=True))
            return bot.CATEGORY
        if context.user_data['itsphere'] =='Обслуживание и тех.поддержка':
            data = crud.get_category_list(department=4,sphere_status=4)
            reply_keyboard = transform_list(data,3,'name')
            reply_keyboard.append(['⬅️ Назад'])
            await update.message.reply_text('Выберите категорию заявки',reply_markup=ReplyKeyboardMarkup(keyboard=reply_keyboard,resize_keyboard=True))
            return bot.ITCATEGORY
    context.user_data['comment'] = user_comment
    if context.user_data['itsphere'] =='Закуп':
        products = context.user_data['productd']
        text = ''
        for key,val in products.items():
            text = text+f"{key} - {val}\n"
        reply_keyboard = [['Подтвердить','⬅️ Назад']]
        await update.message.reply_text(f"Ваша корзина:\n{text}",reply_markup=ReplyKeyboardMarkup(keyboard=reply_keyboard,resize_keyboard=True))
        return bot.ITFINISHING
    
    if context.user_data['itsphere'] =='Обслуживание и тех.поддержка':
        #category_query = crud.getcategoryname(name=context.user_data['category'])
        #fillial_query = crud.getchildbranch(fillial=context.user_data['branch'],type=int(context.user_data['type']),factory=int(context.user_data['sphere_status']))
        #fillial_id = fillial_query.id
        #user_query = crud.get_user_tel_id(id=update.message.from_user.id)
        #finishing_time = datetime.timedelta(hours=category_query.ftime)+datetime.datetime.now(tz=timezonetash)
        #data = crud.add_it_request(category_id=category_query.id,fillial_id=fillial_id,user_id=user_query.id,size=None,finishing_time=finishing_time,comment=user_comment)
        #if context.user_data['image_it'] is not None:
        #    crud.create_files(request_id=data.id,filename=context.user_data['image_it'])
        #reply_keyboard = [['⬅️ Назад']]
        reply_keyboard = [['⬅️ Назад',"Пропустить"]]
        await update.message.reply_text('Пожалуйста отправьте фото',reply_markup=ReplyKeyboardMarkup(keyboard=reply_keyboard,resize_keyboard=True))
        return bot.ITFILES
    



async def it_files(update:Update,context:ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text:
        input_text = update.message.text
        if input_text == '⬅️ Назад':
            #data = crud.get_category_list(department=4,sphere_status=4)
            #reply_keyboard = transform_list(data,3,'name')
            reply_keyboard = [['⬅️ Назад']]
            await update.message.reply_text('Введите комментарии к заявке',reply_markup=ReplyKeyboardMarkup(keyboard=reply_keyboard,resize_keyboard=True))
            return bot.ITCOMMENT
        else:
            context.user_data['image_it'] = None
    else:
        if update.message.document:
        #context.user_data['file_url']=f"files/{update.message.document.file_name}"
            file_id = update.message.document.file_id
            file_name = update.message.document.file_name
            new_file = await context.bot.get_file(file_id=file_id)
            file_content = await new_file.download_as_bytearray()
            #files_open = {'files':file_content}
        if update.message.photo:
            file_name = f"{update.message.photo[-1].file_id}.jpg"
            getFile = await context.bot.getFile(update.message.photo[-1].file_id)
            file_content = await getFile.download_as_bytearray()
            #files_open = {'files':file_content}
        with open(f"{bot.backend_location}files/{file_name}",'wb+') as f:
            f.write(file_content)
            f.close()
        context.user_data['image_it'] ='files/'+file_name
    #reply_keyboard = [['⬅️ Назад']]
    #await update.message.reply_text('Введите комментарии к заявке',reply_markup=ReplyKeyboardMarkup(keyboard=reply_keyboard,resize_keyboard=True))
    if context.user_data['itsphere'] =='Обслуживание и тех.поддержка':
        user_comment = context.user_data['comment']
        category_query = crud.getcategoryname(name=context.user_data['category'],department=int(context.user_data['type']))
        fillial_query = crud.getchildbranch(fillial=context.user_data['branch'],type=int(context.user_data['type']),factory=int(context.user_data['sphere_status']))
        fillial_id = fillial_query.id
        user_query = crud.get_user_tel_id(id=update.message.from_user.id)
        finishing_time = datetime.timedelta(hours=category_query.ftime)+datetime.datetime.now(tz=timezonetash)
        data = crud.add_it_request(category_id=category_query.id,fillial_id=fillial_id,user_id=user_query.id,size=None,finishing_time=finishing_time,comment=user_comment)
        if context.user_data['image_it'] is not None:
            crud.create_files(request_id=data.id,filename=context.user_data['image_it'])
        #reply_keyboard = [['⬅️ Назад']]
        await update.message.reply_text(f"Спасибо, ваша заявка #{data.id}s по IT🧑‍💻 принята.  Как ваша заявка будет назначена в работу, вы получите уведомление",reply_markup=ReplyKeyboardMarkup(keyboard=bot.manu_buttons,resize_keyboard=True))

        formatted_datetime_str = data.created_at.strftime("%Y-%m-%d %H:%M")
        text = f"📑Заявка № {data.id}\n\n📍Филиал: {fillial_query.name}\n" \
               f"🕘Дата поступления заявки: {formatted_datetime_str}\n\n" \
               f"🔰Категория проблемы: {data.category_name}\n" \
               f"💬Комментарии: {data.description}"

        sendtotelegram(bot_token=BOTTOKEN, chat_id=data.chat_id, message_text=text, buttons=[])

    return bot.MANU

async def it_finishing(update:Update,context:ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == '⬅️ Назад':
        reply_keyboard = [['⬅️ Назад']]
        await update.message.reply_text('Введите комментарии к заявке',reply_markup=ReplyKeyboardMarkup(keyboard=reply_keyboard,resize_keyboard=True))
        return bot.ITCOMMENT
    category_query = crud.getcategoryname(name=context.user_data['category'],department=int(context.user_data['type']))
    fillial_query = crud.getchildbranch(fillial=context.user_data['branch'],type=int(context.user_data['type']),factory=int(context.user_data['sphere_status']))
    fillial_id = fillial_query.id
    user_query = crud.get_user_tel_id(id=update.message.from_user.id)
    finishing_time = datetime.timedelta(hours=category_query.ftime)+datetime.datetime.now(tz=timezonetash)
    data = crud.add_it_request(category_id=category_query.id,fillial_id=fillial_id,user_id=user_query.id,size=None,finishing_time=finishing_time,comment=context.user_data['comment'])
    #reply_keyboard = [['⬅️ Назад']]
    formatted_datetime_str = data.created_at.strftime("%Y-%m-%d %H:%M")
    text = f"📑Заявка № {data.id}\n\n📍Филиал: {fillial_query.name}\n" \
           f"🕘Дата поступления заявки: {formatted_datetime_str}\n\n" \
           f"🔰Категория проблемы: {data.category_name}\n" \
           f"💬Комментарии: {data.description}"




    sendtotelegram(bot_token=BOTTOKEN,chat_id=data.chat_id,message_text=text,buttons=[])

    products = dict(context.user_data['productd'])
    for key,value in products.items():
        product = crud.get_product_by_name(name=key)
        crud.create_order_product(order_id=data.id,product_id=product.id,amount=value)
    await update.message.reply_text(f"Спасибо, ваша заявка #{data.id}s по IT🧑‍💻 принята.  Как ваша заявка будет назначена в работу, вы получите уведомление",reply_markup=ReplyKeyboardMarkup(keyboard=bot.manu_buttons,resize_keyboard=True))
    return bot.MANU


    