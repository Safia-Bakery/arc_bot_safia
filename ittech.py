#from bot import CHOOSESIZE,CHOOSEDAY,CHOOSEMONTH,INPUTIMAGECAR,COMMENTCAR,MANU,CHOOSEHOUR,manu_buttons,backend_location,CATEGORY,session,transform_list

import bot
import crud
from telegram import ReplyKeyboardMarkup,Update, InlineKeyboardMarkup,InlineKeyboardButton
from telegram.ext import (
    ContextTypes,
    ConversationHandler

)

import microser
from microser import transform_list, sendtotelegram, inlinewebapp

BASE_URL = 'https://api.service.safiabakery.uz/'
import datetime
import re
import pytz
timezonetash = pytz.timezone("Asia/Tashkent")
import os
from dotenv import load_dotenv
load_dotenv()
BOTTOKEN = os.environ.get('BOT_TOKEN')
IT_SUPERGROUP = os.environ.get('IT_SUPERGROUP')

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
    elif user_mess == 'Обслуживание и тех.поддержка':
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
        reply_keyboard = [['⬅️ Назад']]
        await update.message.reply_text('Введите номер телефона в формате: 998941114411 или 941114411',
                                        reply_markup=ReplyKeyboardMarkup(keyboard=reply_keyboard, resize_keyboard=True))
        return bot.ITPHONENUMBER


async def itphonenumber(update:Update,context:ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == '⬅️ Назад':
        data = crud.get_category_list(department=4,sphere_status=4)
        reply_keyboard = transform_list(data,3,'name')
        reply_keyboard.append(['⬅️ Назад'])
        await update.message.reply_text('Выберите категорию заявки',reply_markup=ReplyKeyboardMarkup(keyboard=reply_keyboard,resize_keyboard=True))
        return bot.ITCATEGORY

    user_comment = update.message.text
    is_phone_number = microser.validate_phone_number(user_comment)
    reply_keyboard = [['⬅️ Назад']]
    if not is_phone_number:
        # if len(user_comment) < 9:
        await update.message.reply_text('Введите номер телефона в формате: 998941114411 или 941114411',
                                        reply_markup=ReplyKeyboardMarkup(keyboard=reply_keyboard,
                                                                         resize_keyboard=True))
        return bot.ITPHONENUMBER

    user_comment = microser.clean_and_format_phone_number(user_comment)
    context.user_data['phone_number'] = user_comment
    await update.message.reply_text('Пожалуйста отправьте фото',
                                    reply_markup=ReplyKeyboardMarkup(keyboard=reply_keyboard, resize_keyboard=True))
    return bot.ITFILES




async def it_files(update:Update,context:ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text:
        input_text = update.message.text
        if input_text == '⬅️ Назад':
            #data = crud.get_category_list(department=4,sphere_status=4)
            #reply_keyboard = transform_list(data,3,'name')
            reply_keyboard = [['⬅️ Назад']]
            await update.message.reply_text('Введите номер телефона в формате: 998941114411 или 941114411',
                                            reply_markup=ReplyKeyboardMarkup(keyboard=reply_keyboard, resize_keyboard=True))
            return bot.ITPHONENUMBER

        else:
            context.user_data['image_it'] = None
    else:
        file_name = ''
        file_content = ''
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
        try:
            with open(f"{bot.backend_location}files/{file_name}",'wb+') as f:
                f.write(file_content)
                f.close()
        except:
            print("There is no any folder such as 'files'")

        context.user_data['image_it'] ='files/'+file_name

    #reply_keyboard = [['⬅️ Назад']]
    #await update.message.reply_text('Введите комментарии к заявке',reply_markup=ReplyKeyboardMarkup(keyboard=reply_keyboard,resize_keyboard=True))
    if context.user_data['itsphere'] =='Обслуживание и тех.поддержка':
        user_comment = context.user_data['comment']
        category_query = crud.getcategoryname(name=context.user_data['category'],department=int(context.user_data['type']))
        fillial_query = crud.getchildbranch(fillial=context.user_data['branch'],type=int(context.user_data['type']),
                                            factory=int(context.user_data['sphere_status']))
        fillial_id = fillial_query.id
        user_query = crud.get_user_tel_id(id=update.message.from_user.id)
        finishing_time = datetime.timedelta(hours=category_query.ftime)+datetime.datetime.now(tz=timezonetash)
        phone_number = context.user_data['phone_number']
        data = crud.add_it_request(category_id=category_query.id,fillial_id=fillial_id,user_id=user_query.id,size=None,finishing_time=finishing_time,comment=user_comment,phone_number=phone_number)
        if context.user_data['image_it'] is not None:
            crud.create_files(request_id=data.id,filename=context.user_data['image_it'])
        formatted_created_time = data.created_at.strftime("%d.%m.%Y %H:%M")
        formatted_finishing_time = data.finishing_time.strftime("%d.%m.%Y %H:%M")
        text = f"📑Заявка #{data.id}s\n\n" \
               f"📍Филиал: {fillial_query.parent_fillial}\n" \
               f"👨‍💼Сотрудник: {user_query.full_name}\n" \
               f"📱Номер телефона сотрудника: +{user_query.phone_number}\n" \
               f"📱Номер телефона для заявки: {phone_number}\n" \
               f"🔰Категория проблемы: {data.category_name}\n" \
               f"🕘Дата поступления заявки: {formatted_created_time}\n" \
               f"🕘Дата дедлайна заявки: {formatted_finishing_time}\n" \
               f"❗️SLA: {category_query.ftime} часов\n" \
               f"💬Комментарии: {data.description}"

        await update.message.reply_text(
            text=text,
            reply_markup=ReplyKeyboardMarkup(keyboard=bot.manu_buttons, resize_keyboard=True),
            parse_mode='HTML'
        )
        keyboard = [
            [InlineKeyboardButton("Принять заявку", callback_data='accept_action')],
            [InlineKeyboardButton("Посмотреть фото", url=f"{BASE_URL}{context.user_data['image_it']}")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        message = await context.bot.send_message(chat_id=IT_SUPERGROUP, text=text, reply_markup=reply_markup,
                                                 parse_mode='HTML')
        crud.update_it_request(id=data.id, message_id=message.message_id, status=0)

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



    if data.chat_id is not None:
        sendtotelegram(bot_token=BOTTOKEN,chat_id=data.chat_id,message_text=text,buttons=[])

    products = dict(context.user_data['productd'])
    for key,value in products.items():
        product = crud.get_product_by_name(name=key)
        crud.create_order_product(order_id=data.id,product_id=product.id,amount=value)
    await update.message.reply_text(f"Спасибо, ваша заявка #{data.id}s по IT🧑‍💻 принята.  Как ваша заявка будет назначена в работу, вы получите уведомление",reply_markup=ReplyKeyboardMarkup(keyboard=bot.manu_buttons,resize_keyboard=True))
    return bot.MANU


async def it_deny_reason(update:Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_comment = update.message.text
    request = crud.update_it_request(id=context.user_data['request_id'], status=4, deny_reason=user_comment)
    # formatted_created_time = request.created_at.strftime("%d.%m.%Y %H:%M")
    # formatted_finishing_time = request.finishing_time.strftime("%d.%m.%Y %H:%M")
    # request_text = f"📑Заявка № {request.id}\n\n" \
    #                f"📍Филиал: {request.parentfillial_name}\n" \
    #                f"👨‍💼Сотрудник: {request.user_full_name}\n" \
    #                f"📱Номер телефона: {request.phone_number}\n" \
    #                f"🔰Категория проблемы: {request.category_name}\n" \
    #                f"🕘Дата поступления заявки: {formatted_created_time}\n" \
    #                f"🕘Дата дедлайна заявки: {formatted_finishing_time}\n" \
    #                f"❗️SLA: {request.sla} часов\n" \
    #                f"💬Комментарии: {request.description}"
    #
    # text = f"{request_text}\n\n" \
    #        f"<b>Заявка отменена 🚫</b>\n" \
    #        f"Причина отмены: {request.deny_reason}"

    # await update.callback_query.edit_message_text(text=text, reply_markup=None, parse_mode='HTML')
    message_text = f"❌Ваша заявка #{request.id}s по IT👨🏻‍💻 отменена по причине: {request.deny_reason}\n\n" \
                   f"Если Вы с этим не согласны, поставьте, пожалуйста, " \
                   f"рейтинг нашему решению по Вашей заявке от 1 до 5, и напишите свои комментарий."

    url = f"{bot.FRONT_URL}tg/order-rating/{request.id}?user_id={request.user_id}&department={request.category_department}&sub_id={request.category_sub_id}"
    inlinewebapp(
        bot_token=BOTTOKEN,
        chat_id=request.user_telegram_id,
        message_text=message_text,
        url=url
    )
    return ConversationHandler.END


