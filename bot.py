#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""


from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update,KeyboardButton,InlineKeyboardMarkup
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
    CallbackContext
    

)
import os 
from io import BytesIO


manu_buttons = [['Подать заявку📝'],['Обучение🧑‍💻','Информацияℹ️'],['Оставить отзыв💬','Настройки⚙️']]
import datetime

import requests
BASE_URL = 'http://backend.service.safiabakery.uz/'
backend_location = '/var/www/safia/arc_backend/'

PHONE, FULLNAME, MANU, BRANCHES,CATEGORY,DESCRIPTION,PRODUCT,FILES, TYPE,BRIG_MANU,LOCATION_BRANCH,ORDERSTG,FINISHING= range(13)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about their gender."""
    await update.message.reply_text(
        "Здравствуйте. Давайте сначала познакомимся ☺️\nКак Вас зовут? (в формате Ф.И.О)",
        
    )

    return FULLNAME



async def fullname(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the: photo and asks for a location."""
    #photo_file = await update.message.photo[-1].get_file()
    #await photo_file.download_to_drive("user_photo.jpg")
    #logger.info("Photo of %s: %s", user.first_name, "user_photo.jpg")
    context.user_data['full_name']=update.message.text
    reply_keyboard = [[KeyboardButton(text='Поделиться контактом', request_contact=True)]]
    await update.message.reply_text(
        f"📱 Какой у Вас номер, {update.message.text}? Отправьте или введите ваш номер телефона.",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True,input_field_placeholder="Поделиться контактом",resize_keyboard=True
        ),
    )

    return PHONE

async def phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    context.user_data['phone_number'] = update.message.contact.phone_number.replace('+','')
    body = {'phone_number':context.user_data['phone_number'],'telegram_id':update.message.from_user.id,'full_name':context.user_data['full_name']}
    requests_data = requests.post(f"{BASE_URL}tg/create/user",json=body)
    await update.message.reply_text(f"Главное меню",reply_markup=ReplyKeyboardMarkup(manu_buttons,one_time_keyboard=True,resize_keyboard=True))

    
    return MANU









def transform_list(lst, size, key):
    return [[f"{item[key]}" for item in lst[i:i+size]] for i in range(0, len(lst), size)]



async def manu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the location and asks for some info about the user."""
    text_manu = update.message.text
    if text_manu.lower() !='подать заявку📝':
        await update.message.reply_text(f"Iltimos boshqa menu tanlang bu hali aktiv emas",reply_markup=ReplyKeyboardMarkup(manu_buttons,one_time_keyboard=True,resize_keyboard=True))
        return MANU
    else:
        reply_keyboard = [['Арс🛠',"IT🧑‍💻"],['Маркетинг📈','Инвентарь📦']]
        await update.message.reply_text(f"Iltimos buzulish tipini tanlang.",reply_markup=ReplyKeyboardMarkup(reply_keyboard,one_time_keyboard=True,resize_keyboard=True))

        return TYPE



async def type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    type_name = update.message.text
    if type_name.lower() !='арс🛠':
        reply_keyboard = [['Арс🛠',"IT🧑‍💻"],['Маркетинг📈','Инвентарь📦']]
        
        await update.message.reply_text(f"Siz tanlagan menu hozir aktiv emas",reply_markup=ReplyKeyboardMarkup(reply_keyboard,one_time_keyboard=True,resize_keyboard=True))
        return TYPE
    else:
        context.user_data['type'] = 'arc'
        request_db = requests.get(f"{BASE_URL}fillials/list/tg").json()
        fillials = request_db
        reply_keyboard = transform_list(request_db,3,'name')
        await update.message.reply_text(f"Filliallarni tanlang",reply_markup=ReplyKeyboardMarkup(reply_keyboard,one_time_keyboard=True,resize_keyboard=True))

        return BRANCHES



async def branches(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the info about the user and ends the conversation."""
    context.user_data['branch'] = update.message.text
    request_db = requests.get(f"{BASE_URL}get/category/tg").json()
    categoryies = request_db
    reply_keyboard = transform_list(request_db,3,'name')
    await update.message.reply_text(f"Iltimos kategoriyani tanlang",reply_markup=ReplyKeyboardMarkup(reply_keyboard,one_time_keyboard=True,resize_keyboard=True))

    return CATEGORY



async def category(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    
    context.user_data['category']=update.message.text
    await update.message.reply_text('Iltimos qanday narsa ekanligini tasvirlang',reply_markup=ReplyKeyboardRemove())
    return DESCRIPTION



async def description(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['description'] = update.message.text
    await update.message.reply_text('Iltimos product nomini kiriting')
    return PRODUCT



async def product(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['product'] = update.message.text
    await update.message.reply_text('menga file yuboring qanday narsani tuzatish kerakligiini bilish uchun')
    return FILES



async def files(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['file_url']=f"files/{update.message.document.file_name}"
    #ile = update.message.document.get_file()
    #with open(file, 'rb') as f:
    #    print(f)
    #update.message.document().get_file()
    file_id = update.message.document.file_id
    file_name = update.message.document.file_name
    new_file = await context.bot.get_file(file_id=file_id)
    
    file_content = await new_file.download_as_bytearray()
    files_open = {'files':file_content}
    data = {'description':context.user_data['description'],
            'product':context.user_data['product'],
            'category':context.user_data['category'],
            'fillial':context.user_data['branch'],
            'type':context.user_data['type'],
            'telegram_id':update.message.from_user.id,
            'file_name':file_name}
    #responsefor = requests.post(url=f"{BASE_URL}tg/request",data=data)
    
    #file_name = update.message.document.file_name
    #with open(f"files/{file_name}", 'wb') as f:
    #    context.bot.get_file(update.message.document).download(out=f)
    responsefor = requests.post(url=f"{BASE_URL}tg/request",data=data,files=files_open)
    await update.message.reply_text('File qabul qilindi va ',reply_markup=ReplyKeyboardMarkup(manu_buttons,one_time_keyboard=True,resize_keyboard=True))
    #print(context.user_data)
    return MANU





async def brig_manu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_choose = update.message.text
    user_id = update.message.from_user.id
    if user_choose == 'zakazlar':
        request_db = requests.get(f"{BASE_URL}tg/branch/get/request?telegram_id={user_id}").json()
        reply_keyboard = transform_list(request_db,3,'id')
        if not reply_keyboard:
            reply_keyboard = [['zakazlar'],['filliallar']]
            await update.message.reply_text(
            f"sizga biriktirilgan zakazlar yoq", reply_markup=ReplyKeyboardMarkup(reply_keyboard,one_time_keyboard=True,resize_keyboard=True))
            return BRIG_MANU
        await update.message.reply_text(f"ushu sizning elonglaringiz",reply_markup=ReplyKeyboardMarkup(reply_keyboard,one_time_keyboard=True,resize_keyboard=True))
        return ORDERSTG
    elif user_choose == 'filliallar':
        request_db = requests.get(f"{BASE_URL}fillials/list/tg").json()
        reply_keyboard = transform_list(request_db,3,'name')
        await update.message.reply_text(f"Filliallarni tanlang",reply_markup=ReplyKeyboardMarkup(reply_keyboard,one_time_keyboard=True,resize_keyboard=True))
        return LOCATION_BRANCH
    else:
        reply_keyboard = [['zakazlar'],['filliallar']]
        await update.message.reply_text(
        f"Manu", reply_markup=ReplyKeyboardMarkup(reply_keyboard,one_time_keyboard=True,resize_keyboard=True))
        return BRIG_MANU


isTrue = {0:'No',1:'Yes'}

async def orderstg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uservalue = int(update.message.text)
    context.user_data['last_request'] = uservalue
    request_db = requests.get(f"{BASE_URL}tg/get/request?id={uservalue}").json()
    reply_keyboard = [['tugatish'],['olib ketish'],['ortga']]
    if request_db['status'] == 2:
        reply_keyboard = [['tugatish'],['ortga']]
    
    
    await update.message.reply_text(f"📑Заявка № {request_db['id']}\n\n📍Филиал: {request_db['fillial']['name']}\n"\
                                    f"🔰Категория проблемы: {request_db['category']['name']}\n\n"\
                                    f"🕘Дата поступления заявки: {request_db['started_at']}\n"\
                                    f"🆘Срочность:  {isTrue[request_db['urgent']]}\n\n"\
                                    f"💬Комментарии: {request_db['description']}",reply_markup=ReplyKeyboardMarkup(reply_keyboard,one_time_keyboard=True,resize_keyboard=True))
    if request_db['file']:
        for i in request_db['file']:
            await update.message.reply_document(document=open(f"{backend_location}{i['url']}",'rb'))
    return FINISHING




async def finishing(update:Update,context:ContextTypes.DEFAULT_TYPE):
    user_button = update.message.text
    if user_button=='tugatish':
        requests.put(f"{BASE_URL}tg/request",json={'request_id':int(context.user_data['last_request']),'status':3})
    if user_button=='olib ketish':
        requests.put(f"{BASE_URL}tg/request",json={'request_id':int(context.user_data['last_request']),'status':2})
        
        
    
    reply_keyboard = [['zakazlar'],['filliallar']]
    await update.message.reply_text(
    f"Manu", reply_markup=ReplyKeyboardMarkup(reply_keyboard,one_time_keyboard=True,resize_keyboard=True))
    return BRIG_MANU


async def location_branch(update:Update,context:ContextTypes.DEFAULT_TYPE):
    chosen_branch  = update.message.text
    repsonsedata = requests.post(f"{BASE_URL}tg/get/branch",data={'branch_name':chosen_branch}).json()
    reply_keyboard = [['zakazlar'],['filliallar']]
    await update.message.reply_html(text=f"{repsonsedata['name'].capitalize()} - <a href='https://maps.google.com/?q={repsonsedata['latitude']},{repsonsedata['longtitude']}'>Fillial manzili</a>",reply_markup=ReplyKeyboardMarkup(reply_keyboard,one_time_keyboard=True,resize_keyboard=True))
    return BRIG_MANU
    
    



async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    await update.message.reply_text(
        "Siz Manu page ga yonaltirildingiz", reply_markup=ReplyKeyboardMarkup(manu_buttons,one_time_keyboard=True,resize_keyboard=True)
    )
    
    return MANU




async def check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_check = requests.get(f"{BASE_URL}tg/check/user?telegram_id={update.message.from_user.id}")
    if user_check.status_code == 200:
        reply_keyboard = [['zakazlar'],['filliallar']]
        await update.message.reply_text(
        f"sizning brigadangiz {user_check.json()['brigada_name']}", reply_markup=ReplyKeyboardMarkup(reply_keyboard,one_time_keyboard=True,resize_keyboard=True)
        )
        return BRIG_MANU
    else:
        await update.message.reply_text(
        "Siz Manu page ga yonaltirildingiz", reply_markup=ReplyKeyboardMarkup(manu_buttons,one_time_keyboard=True,resize_keyboard=True)
        )
    
        return BRIG_MANU





def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("6247686133:AAG-7Z9ZMpaEanMd1VlyiKO4S2Xbm_jp8BE").build()

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            PHONE: [MessageHandler(filters.CONTACT, phone)],
            FULLNAME: [MessageHandler(filters.TEXT, fullname)],
            MANU: [MessageHandler(filters.TEXT & ~filters.COMMAND, manu)],
            CATEGORY:[MessageHandler(filters.TEXT,category)],
            DESCRIPTION:[MessageHandler(filters.TEXT,description)],
            PRODUCT:[MessageHandler(filters.TEXT,product)],
            FILES:[MessageHandler(filters.Document.ALL,files)],
            BRIG_MANU:[MessageHandler(filters.TEXT,brig_manu)],
            BRANCHES: [MessageHandler(filters.TEXT & ~filters.COMMAND, branches)],
            TYPE:[MessageHandler(filters.TEXT,type)],
            ORDERSTG:[MessageHandler(filters.TEXT,orderstg)],
            LOCATION_BRANCH:[MessageHandler(filters.TEXT,location_branch)],
            FINISHING:[MessageHandler(filters.TEXT,finishing)],
        },
        fallbacks=[CommandHandler("cancel", cancel),
                   CommandHandler('check',check)]
        
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()