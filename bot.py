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
import json
import re
from telegram.constants import ParseMode
from sqlalchemy.orm import Session

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
from datetime import datetime
from microser import get_db,transform_list,generate_text,data_transform,create_access_token,sendtotelegram
import requests

import crud
import os 
from dotenv import load_dotenv
load_dotenv()

from database import engine,session
#Base.metadata.create_all(bind=engine)
BOTTOKEN = os.environ.get('BOT_TOKEN')
marketing_cat_dict ={
    'Проектная работа для дизайнеров':1,
    'Локальный маркетинг':2,
    'Промо-продукция':3,
    'POS-Материалы':4,
    'Комплекты':5
}

offsett = 70

manu_buttons = [['Подать заявку📝'],['Обучение🧑‍💻','Информацияℹ️'],['Оставить отзыв💬','Настройки⚙️']]
buttons_sphere = [['Фабрика','Розница']]
sphere_dict = {'Фабрика':2,'Розница':1}
backend_location = '/var/www/safia/arc_backend/'
#backend_location='/Users/gayratbekakhmedov/projects/backend/arc_backend/'

BASE_URL = 'https://backend.service.safiabakery.uz/'

PHONE, FULLNAME, MANU, BRANCHES,CATEGORY,DESCRIPTION,PRODUCT,FILES, TYPE,BRIG_MANU,LOCATION_BRANCH,ORDERSTG,FINISHING,CLOSEBUTTON,MARKETINGCAT,MARKETINGSTBUTTON,SPHERE,CHANGESPHERE,CHOSENSPHERE,ADDCOMMENT= range(20)

persistence = PicklePersistence(filepath='hello.pickle')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about their gender."""
    user= crud.get_user_tel_id(db=session,id=update.message.from_user.id)
    #user_data = requests.post(f"{BASE_URL}tg/login",json={'telegram_id':update.message.from_user.id})

    if user:
        context.user_data['sphere_status']=user.sphere_status
        await update.message.reply_text(f"Главное меню",reply_markup=ReplyKeyboardMarkup(manu_buttons,resize_keyboard=True))
        return MANU
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
            reply_keyboard, input_field_placeholder="Поделиться контактом",resize_keyboard=True
        ),
    )

    return PHONE

async def phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    context.user_data['phone_number'] = update.message.contact.phone_number.replace('+','')

    await update.message.reply_text(f"Пожалуйста выберите направление:",reply_markup=ReplyKeyboardMarkup(buttons_sphere,resize_keyboard=True))
    return SPHERE



async def sphere(update:Update,context:ContextTypes.DEFAULT_TYPE)->int:

    if update.message.text in buttons_sphere[0]:
        context.user_data['sphere_status']=sphere_dict[update.message.text]

    dat = crud.create_user(db=session,full_name=context.user_data['full_name'],phone_number=str(context.user_data['phone_number']).replace('+',''),telegram_id=update.message.from_user.id,sphere_status=int(context.user_data['sphere_status']))
    #requests_data = requests.post(f"{BASE_URL}tg/create/user",json=body)
    await update.message.reply_text(f"Главное меню",reply_markup=ReplyKeyboardMarkup(manu_buttons,resize_keyboard=True))
    return MANU


async def manu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the location and asks for some info about the user."""
    text_manu = update.message.text
    if text_manu.lower() =='подать заявку📝':
        if int(context.user_data['sphere_status'])==2:
            reply_keyboard = [['Арс🛠',"IT🧑‍💻"],['Инвентарь📦','⬅️ Назад']]
            await update.message.reply_text(f"Пожалуйста выберите направление:",reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
        elif int(context.user_data['sphere_status'])==1:
            reply_keyboard = [['Арс🛠',"IT🧑‍💻"],['Маркетинг📈','Инвентарь📦'],['⬅️ Назад']]
            await update.message.reply_text(f"Пожалуйста выберите направление:",reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
        return TYPE


    
    elif text_manu =='Обучение🧑‍💻':
        #await context.bot.send_video(chat_id=update.message.chat_id,video=open('/Users/gayratbekakhmedov/projects/backend/arc_bot/Untitled.mp4','rb'), supports_streaming=True)
        await update.message.reply_text(text="<a href='https://telegra.ph/Obuchenie-09-06-2'>Обучение🧑‍💻</a>",reply_markup=ReplyKeyboardMarkup(manu_buttons,resize_keyboard=True),parse_mode = ParseMode.HTML)
        return MANU
    if text_manu =='Информацияℹ️':
        await update.message.reply_text(f"🔘 Отдел: АРС Розница -  +998(90)432-93-00\n\n🔘 Отдел: АРС Учтепа -  ************\n\n🔘 Отдел: Маркетинг -  +998(88)333-00-23\n\n🔘 Отдел: Инвентарь -  ************\n\n🔘 Отдел: IT -  +998(78)113-77-11",reply_markup=ReplyKeyboardMarkup(manu_buttons,resize_keyboard=True))
        return MANU
    if text_manu =='Настройки⚙️':
        await update.message.reply_text(f"Пожалуйста выберите сферу в которой вы работаете",reply_markup=ReplyKeyboardMarkup([['Поменять сферу','⬅️ Назад']],resize_keyboard=True),)
        return CHANGESPHERE
    else:
        await update.message.reply_text(f"Этот пункт в разработке",reply_markup=ReplyKeyboardMarkup(manu_buttons,resize_keyboard=True))
        return MANU




async def changesphere(update:Update,context:ContextTypes.DEFAULT_TYPE):
    sphere_text = update.message.text
    if sphere_text=="⬅️ Назад":
        await update.message.reply_text(f"Главное меню",reply_markup=ReplyKeyboardMarkup(manu_buttons,resize_keyboard=True))
        return MANU
    elif sphere_text == 'Поменять сферу':
        await update.message.reply_text(f"Пожалуйста выберите сферу в которой вы работаете",reply_markup=ReplyKeyboardMarkup(buttons_sphere,resize_keyboard=True))
        return CHOSENSPHERE
    else:
        await update.message.reply_text(f"Пожалуйста выберите сферу в которой вы работаете",reply_markup=ReplyKeyboardMarkup([['Поменять сферу','⬅️ Назад']],resize_keyboard=True),)
        return CHANGESPHERE

async def chosensphere(update:Update,context:ContextTypes.DEFAULT_TYPE):
    chosen_sphere = update.message.text
    if chosen_sphere=="⬅️ Назад":
        await update.message.reply_text(f"Поменять сферу",reply_markup=ReplyKeyboardMarkup([['Поменять сферу','⬅️ Назад']],resize_keyboard=True),)
        return CHANGESPHERE
    if chosen_sphere =="Фабрика":
        context.user_data['sphere_status']=2
        crud.update_user_sphere(db=session,tel_id=update.message.from_user.id,sphere_status=2)
        await update.message.reply_text(f"Вы успешно поменяли сферу",reply_markup=ReplyKeyboardMarkup(manu_buttons,resize_keyboard=True))
        return MANU

    elif chosen_sphere=='Розница':
        context.user_data['sphere_status']=1
        crud.update_user_sphere(db=session,tel_id=update.message.from_user.id,sphere_status=1)
        await update.message.reply_text(f"Вы успешно поменяли сферу",reply_markup=ReplyKeyboardMarkup(manu_buttons,resize_keyboard=True))
        return MANU
    else:
        await update.message.reply_text(f"choose one",reply_markup=ReplyKeyboardMarkup(buttons_sphere,resize_keyboard=True),)
        return CHOSENSPHERE

async def types(update: Update, context: ContextTypes.DEFAULT_TYPE):
    type_name = update.message.text
    if type_name.lower() =='арс🛠':
        context.user_data['page_number'] =0
        context.user_data['type'] = 1
        if context.user_data['sphere_status']==1:
            request_db = crud.get_branch_list(db=session,sphere_status=1)
            #request_db = requests.get(f"{BASE_URL}fillials/list/tg").json()
        else:
            request_db = crud.getfillialchildfabrica(db=session,offset=0)
            #request_db = requests.get(f"{BASE_URL}get/fillial/fabrica/tg").json()
 
        reply_keyboard = transform_list(request_db,2,'name')

        reply_keyboard.insert(0,['⬅️ Назад'])
        reply_keyboard.append(['<<<Предыдущий','Следующий>>>'])
        await update.message.reply_text(f"Выберите филиал или отдел:",reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))

        return BRANCHES
    elif type_name=='⬅️ Назад':
        await update.message.reply_text(f"Главное меню",reply_markup=ReplyKeyboardMarkup(manu_buttons,resize_keyboard=True))
        return MANU
    elif type_name=='Маркетинг📈':
        context.user_data['type'] = 2

        request_db = crud.get_branch_list_location(db=session)
        reply_keyboard = transform_list(request_db,3,'name')
        reply_keyboard.insert(0,['⬅️ Назад'])
        await update.message.reply_text(f"Выберите филиал или отдел:",reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))

        return MARKETINGSTBUTTON
    else:
        if int(context.user_data['sphere_status'])==2:
            reply_keyboard = [['Арс🛠',"IT🧑‍💻"],['Инвентарь📦','⬅️ Назад']]
            await update.message.reply_text(f"Пожалуйста выберите направление:",reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
        elif int(context.user_data['sphere_status'])==1:
            reply_keyboard = [['Арс🛠',"IT🧑‍💻"],['Маркетинг📈','Инвентарь📦'],['⬅️ Назад']]
            await update.message.reply_text(f"Пожалуйста выберите направление:",reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
        return TYPE



async def marketingstbutton(update:Update,context:ContextTypes.DEFAULT_TYPE) ->int:
    if update.message.text == '⬅️ Назад':
        reply_keyboard = [['Арс🛠',"IT🧑‍💻"],['Маркетинг📈','Инвентарь📦'],['⬅️ Назад']]
        
        await update.message.reply_text(f"Пожалуйста выберите направление:",reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
        return TYPE
    context.user_data['branch'] = update.message.text
    reply_keyboard = [['Проектная работа для дизайнеров','Локальный маркетинг'],['Промо-продукция','POS-Материалы'],['Комплекты','⬅️ Назад']]
    await update.message.reply_text(f"Пожалуйста выберите категорию",reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
    return MARKETINGCAT



async def marketingcat(update:Update,context:ContextTypes.DEFAULT_TYPE) -> int:
    type_name = update.message.text

    if update.message.text == '⬅️ Назад':
        request_db = crud.get_branch_list_location(db=session)
        reply_keyboard = transform_list(request_db,3,'name')
        reply_keyboard.insert(0,['⬅️ Назад'])
        await update.message.reply_text(f"Выберите филиал или отдел:",reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))

        return MARKETINGSTBUTTON
    id_cat = marketing_cat_dict[type_name]
    request_db = crud.get_category_list(db=session,sub_id=id_cat,sphere_status=context.user_data['sphere_status'])
    reply_keyboard = transform_list(request_db,3,'name')
    reply_keyboard.append(['⬅️ Назад'])
    await update.message.reply_text(f"Пожалуйста выберите категорию проблемы:",reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
    return CATEGORY



async def branches(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the info about the user and ends the conversation."""
    user_text = update.message.text
    if update.message.text == '⬅️ Назад':
        if context.user_data['sphere_status']==1:

            reply_keyboard = [['Арс🛠',"IT🧑‍💻"],['Маркетинг📈','Инвентарь📦'],['⬅️ Назад']]
        if context.user_data['sphere_status']==2:
            reply_keyboard = [['Арс🛠',"IT🧑‍💻"],['Инвентарь📦','⬅️ Назад']]
        

        await update.message.reply_text(f"Пожалуйста выберите направление:",reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
        return TYPE
    if user_text=='Следующий>>>':
        context.user_data['page_number']=int(context.user_data['page_number'])+1
        if context.user_data['sphere_status']==1:
            request_db = crud.get_branch_list(db=session,sphere_status=1)
            #request_db = requests.get(f"{BASE_URL}fillials/list/tg").json()
        else:
            request_db = crud.getfillialchildfabrica(db=session,offset=int(context.user_data['page_number'])*offsett)
        #request_db = crud.getfillialchildfabrica(db=session,offset=int(context.user_data['page_number'])*offsett)
        reply_keyboard = transform_list(request_db,2,'name')

        reply_keyboard.insert(0,['⬅️ Назад'])
        reply_keyboard.append(['<<<Предыдущий','Следующий>>>'])
        await update.message.reply_text(f"Выберите филиал или отдел:",reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))

        return BRANCHES
    if user_text=='<<<Предыдущий':
        if int(context.user_data['page_number']) >0:
            context.user_data['page_number']=int(context.user_data['page_number'])-1
        else:
            context.user_data['page_number']=0
        if context.user_data['sphere_status']==1:
            request_db = crud.get_branch_list(db=session,sphere_status=1)
            #request_db = requests.get(f"{BASE_URL}fillials/list/tg").json()
        else:
            request_db = crud.getfillialchildfabrica(db=session,offset=int(context.user_data['page_number'])*offsett)
        reply_keyboard = transform_list(request_db,2,'name')

        reply_keyboard.insert(0,['⬅️ Назад'])
        reply_keyboard.append(['<<<Предыдущий','Следующий>>>'])
        await update.message.reply_text(f"Выберите филиал или отдел:",reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))

        return BRANCHES



    context.user_data['branch'] = update.message.text

    request_db =  crud.get_category_list(db=session,sphere_status=context.user_data['sphere_status'])
    categoryies = request_db
    reply_keyboard = transform_list(request_db,3,'name')

    reply_keyboard.append(['⬅️ Назад'])
    await update.message.reply_text(f"Пожалуйста выберите категорию проблемы:",reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))

    return CATEGORY



async def category(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == '⬅️ Назад':
        if context.user_data['type']==1:
            if context.user_data['sphere_status']==1:
                
                request_db = crud.get_branch_list(db=session,sphere_status=1)
            else:
                context.user_data['page_number']=0
                request_db = crud.getfillialchildfabrica(db=session,offset=0)
            reply_keyboard = transform_list(request_db,3,'name')
            reply_keyboard.insert(0,['⬅️ Назад'])
            reply_keyboard.append(['<<<Предыдущий','Следующий>>>'])
            await update.message.reply_text(f"Выберите филиал или отдел:",reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))

            return BRANCHES
        else:
            reply_keyboard = [['Проектная работа для дизайнеров','Локальный маркетинг'],['Промо-продукция','POS-Материалы'],['Комплекты','⬅️ Назад']]
            await update.message.reply_text(f"Пожалуйста выберите категорию",reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
            return MARKETINGCAT
    context.user_data['category']=update.message.text
    if int(context.user_data['type'])==1:
        reply_keyboard = [['⬅️ Назад']]
        await update.message.reply_text('Пожалуйста укажите название/модель оборудования',reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
        return PRODUCT
    elif int(context.user_data['type'])==2:
        reply_keyboard = [['⬅️ Назад']]
        await update.message.reply_text('Пожалуйста напишите комментарии к заявке ',reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
        return DESCRIPTION



async def product(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == '⬅️ Назад':
        request_db = crud.get_category_list(db=session,sphere_status=context.user_data['sphere_status'])
        reply_keyboard = transform_list(request_db,3,'name')
        reply_keyboard.insert(0,['⬅️ Назад'])
        await update.message.reply_text(f"Пожалуйста выберите категорию проблемы:",reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))

        return CATEGORY
    reply_keyboard = [['⬅️ Назад']]
    context.user_data['product'] = update.message.text
    await update.message.reply_text('Пожалуйста напишите комментарии к заявке ',reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
    return DESCRIPTION



async def description(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [['⬅️ Назад']]
    if update.message.text == '⬅️ Назад':
        if int(context.user_data['type'])==1:
            await update.message.reply_text('Пожалуйста укажите название/модель оборудования',reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
            return PRODUCT
        if int(context.user_data['type'])==2:
            reply_keyboard = [['Проектная работа для дизайнеров','Локальный маркетинг'],['Промо-продукция','POS-Материалы'],['Комплекты','⬅️ Назад']]
            await update.message.reply_text(f"Пожалуйста выберите категорию",reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
            return MARKETINGCAT
    context.user_data['description'] = update.message.text
    await update.message.reply_text('Отправьте фотографию или файл:',reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
    return FILES



async def files(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text:
        if update.message.text=='⬅️ Назад':
            reply_keyboard = [['⬅️ Назад']]
            await update.message.reply_text('Пожалуйста напишите комментарии к заявке ',reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
            return DESCRIPTION

    else:
        
        #ile = update.message.document.get_file()
        #with open(file, 'rb') as f:
        #    print(f)
        #update.message.document().get_file()
        if update.message.document:
           #context.user_data['file_url']=f"files/{update.message.document.file_name}"
            file_id = update.message.document.file_id
            file_name = update.message.document.file_name
            new_file = await context.bot.get_file(file_id=file_id)
            
            file_content = await new_file.download_as_bytearray()
            files_open = {'files':file_content}
        if update.message.photo:
            file_name = f"{update.message.photo[-1].file_id}.jpg"
            getFile = await context.bot.getFile(update.message.photo[-1].file_id)
            file_content = await getFile.download_as_bytearray()
            files_open = {'files':file_content}
        with open(f"{backend_location}files/{file_name}",'wb+') as f:
            f.write(file_content)
            f.close()
        #data = {'description':context.user_data['description'],
        #        'product':context.user_data['product'],
        #        'category':context.user_data['category'],
        #        'fillial':context.user_data['branch'],
        #        'type':int(context.user_data['type']),
        #        'telegram_id':update.message.from_user.id,
        #        'file_name':file_name,
        #        'factory':int(context.user_data['sphere_status'])}
        #responsefor = requests.post(url=f"{BASE_URL}tg/request",data=data)

        #file_name = update.message.document.file_name
        #with open(f"files/{file_name}", 'wb') as f:
        #    context.bot.get_file(update.message.document).download(out=f)
        #responsefor = requests.post(url=f"{BASE_URL}tg/request",data=data,files=files_open).json()
        category_query = crud.getcategoryname(db=session,name=context.user_data['category'])
        fillial_query = crud.getchildbranch(db=session,fillial=context.user_data['branch'],type=int(context.user_data['type']),factory=int(context.user_data['sphere_status']))
        user_query = crud.get_user_tel_id(db=session,id=update.message.from_user.id)
        list_data = [None,'АРС🛠','Маркетигну📈']
        if context.user_data['type']==2:
            product=None
        if context.user_data['type']==1:
            product=context.user_data['product']
        add_request = crud.add_request(db=session,is_bot=1,category_id=category_query.id,fillial_id=fillial_query.id,product=product,description=context.user_data['description'],user_id=user_query.id)
        
        crud.create_files(db=session,request_id=add_request.id,filename=f"files/{file_name}")
        formatted_datetime_str = add_request.created_at.strftime("%Y-%m-%d %H:%M")
        text  = f"📑Заявка № {add_request.id}\n\n📍Филиал: {add_request.fillial.parentfillial.name}\n"\
                        f"🕘Дата поступления заявки: {formatted_datetime_str}\n\n"\
                        f"🔰Категория проблемы: {add_request.category.name}\n"\
                        f"⚙️ Название оборудования: {add_request.product}\n"\
                        f"💬Комментарии: {add_request.description}"
        keyboard = [
        ]
        if add_request.file:
            for i in add_request.file:
                keyboard.append({'text':'Посмотреть фото/видео',"url":f"{BASE_URL}{i.url}"})
        if add_request.category.sphere_status==1 and add_request.category.department==1:
                sendtotelegram(bot_token=BOTTOKEN,chat_id='-1001920671327',message_text=text,buttons=keyboard)
        if add_request.category.sphere_status==2 and add_request.category.department==1:
                sendtotelegram(bot_token=BOTTOKEN,chat_id='-1001831677963',message_text=text,buttons=keyboard)
        await update.message.reply_text(f"Спасибо, ваша заявка №{add_request.id} по {list_data[context.user_data['type']]} принята. Как ваша заявка будет назначена в работу ,вы получите уведомление.",reply_markup=ReplyKeyboardMarkup(manu_buttons,resize_keyboard=True))
        return MANU
    




async def addcomment(update:Update,context:ContextTypes.DEFAULT_TYPE):
    user_option = update.message.text 
    print('come to add comment')
    user_id = update.message.from_user.id
    user = crud.get_user_tel_id(db=session,id=user_id)
    crud.addcomment(db=session,user_id=user.id,comment=user_option,request_id=context.user_data['request_id'])
    await update.message.reply_text(f"Главное меню",reply_markup=ReplyKeyboardMarkup(manu_buttons,resize_keyboard=True))
    return MANU






#-------------------------------BRIGADA MANU-----------------------------------------



async def brig_manu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_choose = update.message.text
    user_id = update.message.from_user.id
    if user_choose == 'Мои заказы 📋':
        user = crud.get_user_tel_id(db=session,id=update.message.from_user.id)
        request_db = crud.tg_get_request_list(db=session,brigada_id=user.brigada_id)
        message_brig = generate_text(request_db)

        reply_keyboard = transform_list(request_db,3,'id')
        if not reply_keyboard:
            reply_keyboard = [['Мои заказы 📋'],['Адреса Филиалов📍']]
            await update.message.reply_text(
            f"У вашей бригады на данный момент нет заявок !", reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
            return BRIG_MANU
        reply_keyboard.insert(0,['⬅️ Назад'])
        await update.message.reply_text(message_brig,reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
        return ORDERSTG
    elif user_choose == 'Адреса Филиалов📍':
        request_db = crud.get_branch_list_location(db=session)
        reply_keyboard = transform_list(request_db,3,'name')
        reply_keyboard.insert(0,['⬅️ Назад'])
        await update.message.reply_text(f"Выберите филиал",reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
        return LOCATION_BRANCH
    else:
        reply_keyboard = [['Мои заказы 📋'],['Адреса Филиалов📍']]
        await update.message.reply_text(
        f"Главное меню", reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
        return BRIG_MANU


isTrue = {0:'No',1:'Yes'}

async def orderstg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uservalue = update.message.text
    if uservalue == '⬅️ Назад':
        reply_keyboard = [['Мои заказы 📋'],['Адреса Филиалов📍']]
        await update.message.reply_text("Главное меню",reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
        return BRIG_MANU
    uservalue = int(uservalue)
    context.user_data['last_request'] = uservalue
    request_db = crud.get_request_id(db=session,id=uservalue)
    reply_keyboard = [['Завершить ✅'],['Забрать на ремонт 🛠'],['⬅️ Назад']]
    if request_db.status == 2:
        reply_keyboard = [['Завершить ✅'],['⬅️ Назад']]

    keyboard = [
    ]
    if request_db.file:
        for i in request_db.file:
            keyboard.append([InlineKeyboardButton('Посмотреть фото/видео',url=f"{BASE_URL}{i.url}")])

    #parsed_datetime = datetime.strptime(request_db.created_at,"%Y-%m-%dT%H:%M:%S.%f")
    
    formatted_datetime_str = request_db.created_at.strftime("%Y-%m-%d %H:%M")
    await update.message.reply_text(f"📑Заявка № {request_db.id}\n\n📍Филиал: {request_db.fillial.parentfillial.name}\n"\
                                    f"🕘Дата поступления заявки: {formatted_datetime_str}\n\n"\
                                    f"🔰Категория проблемы: {request_db.category.name}\n"\
                                    f"⚙️ Название оборудования: {request_db.product}\n"\
                                    f"💬Комментарии: {request_db.description}",reply_markup=InlineKeyboardMarkup(keyboard))
    await update.message.reply_text(f"📑Заявка № {request_db.id}",reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
    if request_db.file:
        for i in request_db.file:
            await update.message.reply_document(document=open(f"{backend_location}{i.url}",'rb'))
    return FINISHING




async def finishing(update:Update,context:ContextTypes.DEFAULT_TYPE):
    user_button = update.message.text
    if user_button=='Завершить ✅':
    
        user_data = crud.get_user_tel_id(db=session,id=update.message.from_user.id)
        access_token  = create_access_token(user_data.username)
        reply_keyboard = [['Мои заказы 📋'],['Адреса Филиалов📍']]
        await update.message.reply_text(
        f"Пожалуйста внесите расход на заявку №{context.user_data['last_request']}",
        reply_markup=ReplyKeyboardMarkup.from_button(
            KeyboardButton(
                text="Внести расход",
                web_app=WebAppInfo(url=f"https://service.safiabakery.uz/tg-add-product/{context.user_data['last_request']}?key={access_token}"),
            ),resize_keyboard=True)
        )
        return CLOSEBUTTON
    
    
        #requests.put(f"{BASE_URL}tg/request",json={'request_id':int(context.user_data['last_request']),'status':3})
    if user_button=='Забрать на ремонт 🛠':
        crud.tg_update_requst_st(db=session,requestid=context.user_data['last_request'],status=2)
        
        
    
    reply_keyboard = [['Мои заказы 📋'],['Адреса Филиалов📍']]
    await update.message.reply_text(
    f"Главное меню", reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
    return BRIG_MANU

async def closebutton(update:Update,context:ContextTypes.DEFAULT_TYPE):
    data = json.loads(update.effective_message.web_app_data.data)
    reply_keyboard = [['Мои заказы 📋'],['Адреса Филиалов📍']]
    await update.message.reply_text("Главное меню",reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
    return BRIG_MANU


async def location_branch(update:Update,context:ContextTypes.DEFAULT_TYPE):
    chosen_branch  = update.message.text
    if chosen_branch == '⬅️ Назад':
        reply_keyboard = [['Мои заказы 📋'],['Адреса Филиалов📍']]
        await update.message.reply_text("Главное меню",reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
        return BRIG_MANU 
    repsonsedata = crud.getfillialname(db=session,name=chosen_branch)
    reply_keyboard = [['Мои заказы 📋'],['Адреса Филиалов📍']]
    await update.message.reply_html(text=f"{repsonsedata.name.capitalize()} - <a href='https://maps.google.com/?q={repsonsedata.latitude},{repsonsedata.longtitude}'>Fillial manzili</a>",reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
    return BRIG_MANU
    
    



async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    await update.message.reply_text(
        "Главное меню", reply_markup=ReplyKeyboardMarkup(manu_buttons,resize_keyboard=True)
    )
    
    return MANU






async def check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_check_query = crud.get_user_tel_id(db=session,id=update.message.from_user.id)
    #user_check = requests.get(f"{BASE_URL}tg/check/user?telegram_id={update.message.from_user.id}")
    if user_check_query.brigada_id:

        reply_keyboard = [['Мои заказы 📋'],['Адреса Филиалов📍']]
        await update.message.reply_text(
        f"🧑‍🔧Ваша команда - {user_check_query.brigader.name}", reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True)
        )
        return BRIG_MANU
    else:
        await update.message.reply_text(
        "Главное меню", reply_markup=ReplyKeyboardMarkup(manu_buttons,resize_keyboard=True)
        )
        return MANU


async def handle_callback_query(update:Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    query = update.callback_query
    selected_option = int(query.data)
    message = query.message
    blank_reply_murkup = [[]]
    text_of_order = query.message.text
    requests_id = re.findall(r'\d+',text_of_order)[0]
    context.user_data['request_id'] = requests_id

    #if selected_option is less than 0 it is about yes or no
    user = crud.get_user_tel_id(db=session,id=query.from_user.id)
    one_request = crud.get_request(db=session,id=requests_id)
    if one_request.status== 3 and int(selected_option)==4:
        await context.bot.send_message(query.from_user.id,'please enter comment',reply_markup=ReplyKeyboardRemove())
        return ADDCOMMENT

    elif one_request.status ==0 and user:
        if selected_option <0:
            if selected_option == -1:
                db_query  = crud.getlistbrigada(db=session,sphere_status=one_request.category.sphere_status)
                reply_murkup = data_transform(db_query)
                await query.message.edit_text(text=text_of_order,reply_markup=InlineKeyboardMarkup(reply_murkup))
            if selected_option== -2:
                request_rejected = crud.reject_request(db=session,status=4,id=requests_id)
                await context.bot.send_message(chat_id=request_rejected.user.telegram_id,text=f"Ваша заявка по Арс🛠  {request_rejected.id}  была отменена по причине: < причина >")
                await query.message.edit_text(text=text_of_order,reply_markup=InlineKeyboardMarkup(blank_reply_murkup))

        #if this value is about more than one it is about it is brigada id
        else:
            request_list = crud.accept_request(db = session,id=requests_id,brigada_id=selected_option,user_manager = user.full_name)
            await query.message.edit_text(text=f"{text_of_order} \n\nкоманда🚙: {request_list.brigada.name}",reply_markup=InlineKeyboardMarkup(blank_reply_murkup))
            try:
                brigada_id = request_list.brigada.id
                brigader_telid = crud.get_brigada_id(session,id=brigada_id)
            except:
                pass
            if request_list.category.department==1:
                try:
                    await context.bot.send_message(chat_id=brigader_telid.user[0].telegram_id,text=f"{request_list.brigada.name} вам назначена заявка, №{request_list.id} {request_list.fillial.name}")
                except:
                    pass
                try:
                    await context.bot.send_message(chat_id=request_list.user.telegram_id,text=f"Уважаемый {request_list.user.full_name}, на вашу заявку №{request_list.id} назначена команда🚙: {request_list.brigada.name}")
                except:
                    pass
            else:
                try:
                    await context.bot.send_message(chat_id=request_list.user.telegram_id,message_text=f"Уважаемый {request_list.user.full_name}, статус вашей заявки №{request_list.id} по Маркетингу: В процессе.")
                except:
                    pass
    else:
        await query.message.edit_text(text=text_of_order,reply_markup=InlineKeyboardMarkup(blank_reply_murkup))



def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    callback_query_handler = CallbackQueryHandler(handle_callback_query)
    persistence = PicklePersistence(filepath="conversationbot")
    application = Application.builder().token(BOTTOKEN).persistence(persistence).build()
    application.add_handler(callback_query_handler)
    #add states phone fullname category desction and others 
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            PHONE: [MessageHandler(filters.CONTACT, phone)],
            FULLNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, fullname)],
            MANU: [MessageHandler(filters.TEXT & ~filters.COMMAND, manu)],
            CATEGORY:[MessageHandler(filters.TEXT & ~filters.COMMAND,category)],
            DESCRIPTION:[MessageHandler(filters.TEXT & ~filters.COMMAND,description)],
            PRODUCT:[MessageHandler(filters.TEXT & ~filters.COMMAND,product)],
            FILES:[MessageHandler(filters.PHOTO | filters.Document.DOCX|filters.Document.IMAGE|filters.Document.PDF|filters.TEXT|filters.Document.MimeType('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet') & ~filters.COMMAND,files)],
            BRIG_MANU:[MessageHandler(filters.TEXT & ~filters.COMMAND,brig_manu)],
            BRANCHES: [MessageHandler(filters.TEXT & ~filters.COMMAND, branches)],
            TYPE:[MessageHandler(filters.TEXT & ~filters.COMMAND,types)],
            ORDERSTG:[MessageHandler(filters.TEXT & ~filters.COMMAND,orderstg)],
            LOCATION_BRANCH:[MessageHandler(filters.TEXT & ~filters.COMMAND,location_branch)],
            FINISHING:[MessageHandler(filters.TEXT & ~filters.COMMAND,finishing)],
            CLOSEBUTTON:[MessageHandler(filters.StatusUpdate.WEB_APP_DATA & ~filters.COMMAND,closebutton)],
            MARKETINGCAT:[MessageHandler(filters.TEXT& ~filters.COMMAND,marketingcat)],
            MARKETINGSTBUTTON:[MessageHandler(filters.TEXT& ~filters.COMMAND,marketingstbutton)],
            SPHERE:[MessageHandler(filters.TEXT& ~filters.COMMAND,sphere)],
            CHANGESPHERE:[MessageHandler(filters.TEXT&~filters.COMMAND,changesphere)],
            CHOSENSPHERE:[MessageHandler(filters.TEXT& ~filters.COMMAND,chosensphere)],
            ADDCOMMENT:[MessageHandler(filters.TEXT& ~filters.COMMAND,addcomment)]
        },
        fallbacks=[CommandHandler("cancel", cancel),
                   CommandHandler('check',check),
                   CommandHandler('start',start)],
        allow_reentry=True,
        name="my_conversation",
        persistent=True,

        
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()