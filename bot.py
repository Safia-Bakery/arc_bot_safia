#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.
"""
First, a few callback functions are defined. Then, those functions are passed to
the Applisdcation and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import datetime
import json
import os
import re

from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup, Update, WebAppInfo, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton, ReplyKeyboardRemove, InputMediaDocument,InputMediaPhoto
from telegram.constants import ParseMode
from telegram.error import BadRequest
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler, PicklePersistence
)

import arc_factory
import cars
import comments
import crud
import food
import inventory
import coins
import ittech
import ratings
import uniforms
import video
from microser import confirmation_request, delete_from_chat, send_notification, timezonetash
from microser import send_iiko_document
from microser import transform_list, generate_text, data_transform, create_access_token, sendtotelegram, \
    is_time_between, generate_random_string, inlinewebapp, info_string, JobScheduler,sendtotelegramviewimage
import pytz
timezonetash = pytz.timezone("Asia/Tashkent")

# from .cars import choose_current_hour,choose_day,choose_month,choose_size,comment_car,month_list,input_image_car
# from .food import meal_bread_size,meal_size
load_dotenv()

# Base.metadata.create_all(bind=engine)
BOTTOKEN = os.environ.get('BOT_TOKEN')
IT_SUPERGROUP = os.environ.get('IT_SUPERGROUP')
job_scheduler = JobScheduler()

marketing_cat_dict = {
    'Проектная работа для дизайнеров': 1,
    'Видеография/Фото': 2,
    'Промо-продукция': 3,
    'POS-Материалы': 4,
    'Комплекты': 5,
    'Для Терр. Менеджеров': 6,
    'Внешний вид филиала': 7
}

offsett = 70

manu_buttons = [
    ['Подать заявку📝'],
    ['Инструкция подачи заявки 🧑‍💻', 'Информацияℹ️'],
    ['Оставить отзыв💬', 'Адреса Филиалов📍'],
    ['Настройки⚙️']
]
buttons_sphere = [['Фабрика', 'Розница']]
sphere_dict = {'Фабрика': 2, 'Розница': 1}

buttons_sphere_1 = [['Арс Розница🛠',"IT🧑‍💻"],['Маркетинг📈','Инвентарь Розница📦'],['Запрос машины🚛',"Заявка на форму🥼"],['Видеонаблюдение🎥','Монеты💰'], ['Официальное оформление 🧾'], ['⬅️ Назад']]
buttons_sphere_2 = [['Арс Фабрика🛠',"IT🧑‍💻"],['Инвентарь Фабрика📦','Запрос машины🚛'],['Видеонаблюдение🎥','Маркетинг📈'],['⬅️ Назад']]
backend_location = '/var/www/arc_backend/'
# backend_location='C:/Users/bbc43/Desktop/Жесткий диск - D/PROJECTS/Safia/arc_bot_safia/'
# backend_location = '/Users/gayratbekakhmedov/projects/backend/arc_backend/'

BASE_URL = 'https://api.service.safiabakery.uz/'
FRONT_URL = 'https://service.safiabakery.uz/'

PHONE, \
    FULLNAME, \
    MANU, \
    OFFICIAL_EMPLOYMENT, \
    BRANCHES, \
    CATEGORY, \
    DESCRIPTION, \
    PRODUCT, \
    FILES, \
    TYPE, \
    BRIG_MANU, \
    LOCATION_BRANCH, \
    ORDERSTG, \
    FINISHING, \
    CLOSEBUTTON, \
    MARKETINGCAT, \
    MARKETINGSTBUTTON, \
    SPHERE, \
    CHANGESPHERE, \
    CHOSENSPHERE, \
    ADDCOMMENT, \
    CHOOSESIZE, \
    INPUTIMAGECAR, \
    COMMENTCAR, \
    MEALSIZE, \
    MEALBREADSIZE, \
    CARSP, \
    CARSFROMLOC, \
    CARSTOLOC, \
    ITSPHERE, \
    ITCATEGORY, \
    ITPRODUCTS, \
    ITAMOUNT, \
    ITCOMMENT, \
    ITFILES, \
    ITFINISHING, \
    COMMENTTEXT, \
    COMMENTNAME, \
    COMMENTPHOTO, \
    INVETORY, \
    VIDCOMMENT, \
    VIDFROM, \
    VIDTO, \
    VIDFILES, \
    ITPHOTOREPORT, \
    VERIFYUSER, \
    UNIFORMCATEGORIES, \
    UNIFORMSIZE, \
    UNIFORMVERIFY, \
    UNIFORMNAME, \
    UNIFORMAMOUNT, \
    PHONENUMBER, \
    ITPHONENUMBER, \
    INPUTCOMMENT,\
    ARCFACTORYMANAGER,\
    ARCFACTORYDIVISIONS,\
    COINAMOUNT,\
    COINDESCRIPTION= range(58)

persistence = PicklePersistence(filepath='hello.pickle')



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about their gender."""
    user = crud.get_user_tel_id(id=update.message.from_user.id)
    # user_data = requests.post(f"{BASE_URL}tg/login",json={'telegram_id':update.message.from_user.id})

    if user:
        context.user_data['sphere_status'] = user.sphere_status
        await update.message.reply_text(f"Главное меню",
                                        reply_markup=ReplyKeyboardMarkup(manu_buttons, resize_keyboard=True))
        return MANU
    # else:
    #     await update.message.reply_text('Здравствуйте. Давайте сначала познакомимся ☺️\nКак Вас зовут? (в формате Ф.И.О)')
    #     return FULLNAME
    else:
       await update.message.reply_text(
           """Здравствуйте\n
Это корпоративный бот компании Safia\n
Пожалуйста введите пароль:\n\n

если у вас её нет, обратитесь к системному администратору вашей компании""",

       )
       return VERIFYUSER

#    else:
#        await update.message.reply_text(
#            """Здравствуйте\n
# Это корпоративный бот компании Safia\n
# Пожалуйста введите пароль:\n\n
#
# если у вас её нет, обратитесь к системному администратору вашей компании""",
#            
#        )
#        return VERIFYUSER


async def verify_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_input = update.message.text
    if user_input == '$af!a2005':

        await update.message.reply_text(
            "Здравствуйте. Давайте сначала познакомимся ☺️\nКак Вас зовут? (в формате Ф.И.О)",

        )
        return FULLNAME
    else:
        await update.message.reply_text("Пароль не верный❌\nПопробуйте еще раз")
        return VERIFYUSER


async def fullname(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the: photo and asks for a location."""
    # photo_file = await update.message.photo[-1].get_file()
    # await photo_file.download_to_drive("user_photo.jpg")
    # logger.info("Photo of %s: %s", user.first_name, "user_photo.jpg")
    context.user_data['full_name'] = update.message.text
    reply_keyboard = [[KeyboardButton(text='Поделиться контактом', request_contact=True)]]
    await update.message.reply_text(
        f"📱 Какой у Вас номер, {update.message.text}? Отправьте или введите ваш номер телефона.",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, input_field_placeholder="Поделиться контактом", resize_keyboard=True
        ),
    )
    return PHONE


async def phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    context.user_data['phone_number'] = update.message.contact.phone_number.replace('+', '')

    await update.message.reply_text(f"Пожалуйста выберите направление:",
                                    reply_markup=ReplyKeyboardMarkup(buttons_sphere, resize_keyboard=True))
    return SPHERE


async def sphere(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text in buttons_sphere[0]:
        context.user_data['sphere_status'] = sphere_dict[update.message.text]

    dat = crud.create_user(full_name=context.user_data['full_name'],
                           phone_number=str(context.user_data['phone_number']).replace('+', ''),
                           telegram_id=update.message.from_user.id,
                           sphere_status=int(context.user_data['sphere_status']), username=generate_random_string(10))
    # requests_data = requests.post(f"{BASE_URL}tg/create/user",json=body)
    await update.message.reply_text(f"Главное меню",
                                    reply_markup=ReplyKeyboardMarkup(manu_buttons, resize_keyboard=True))
    return MANU


async def manu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the location and asks for some info about the user."""
    text_manu = update.message.text
    if text_manu.lower() == 'подать заявку📝':
        if int(context.user_data['sphere_status']) == 2:
            reply_keyboard = buttons_sphere_2
            await update.message.reply_text(f"Пожалуйста выберите направление:",
                                            reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
        elif int(context.user_data['sphere_status']) == 1:
            reply_keyboard = buttons_sphere_1
            await update.message.reply_text(f"Пожалуйста выберите направление:",
                                            reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
        return TYPE



    elif text_manu == 'Инструкция подачи заявки 🧑‍💻':
        # await context.bot.send_video(chat_id=update.message.chat_id,video=open('/Users/gayratbekakhmedov/projects/backend/arc_bot/Untitled.mp4','rb'), supports_streaming=True)
        await update.message.reply_text(text="<a href='https://telegra.ph/Obuchenie-09-06-2'>Обучение🧑‍💻</a>",
                                        reply_markup=ReplyKeyboardMarkup(manu_buttons, resize_keyboard=True),
                                        parse_mode=ParseMode.HTML)
        return MANU
    if text_manu == 'Информацияℹ️':
        await update.message.reply_text(info_string,
                                        reply_markup=ReplyKeyboardMarkup(manu_buttons, resize_keyboard=True))
        return MANU
    if text_manu == 'Настройки⚙️':
        await update.message.reply_text(f"Пожалуйста выберите сферу в которой вы работаете",
                                        reply_markup=ReplyKeyboardMarkup([['Поменять сферу', '⬅️ Назад']],
                                                                         resize_keyboard=True), )
        return CHANGESPHERE
    elif text_manu == 'Адреса Филиалов📍':
        request_db = crud.get_branch_list_location()
        reply_keyboard = transform_list(request_db, 3, 'name')
        reply_keyboard.insert(0, ['⬅️ Назад'])
        await update.message.reply_text(f"Выберите филиал",
                                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
        return LOCATION_BRANCH
    elif text_manu == 'Оставить отзыв💬':
        await update.message.reply_text("Пожалуйста введите текст отзыва",
                                        reply_markup=ReplyKeyboardMarkup([['⬅️ Назад']], resize_keyboard=True))
        return INPUTCOMMENT
    else:
        await update.message.reply_text(f"Этот пункт в разработке",
                                        reply_markup=ReplyKeyboardMarkup(manu_buttons, resize_keyboard=True))
        return MANU


async def changesphere(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sphere_text = update.message.text
    if sphere_text == "⬅️ Назад":
        await update.message.reply_text(f"Главное меню",
                                        reply_markup=ReplyKeyboardMarkup(manu_buttons, resize_keyboard=True))
        return MANU
    elif sphere_text == 'Поменять сферу':
        await update.message.reply_text(f"Пожалуйста выберите сферу в которой вы работаете",
                                        reply_markup=ReplyKeyboardMarkup(buttons_sphere, resize_keyboard=True))
        return CHOSENSPHERE
    else:
        await update.message.reply_text(f"Пожалуйста выберите сферу в которой вы работаете",
                                        reply_markup=ReplyKeyboardMarkup([['Поменять сферу', '⬅️ Назад']],
                                                                         resize_keyboard=True), )
        return CHANGESPHERE


async def chosensphere(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chosen_sphere = update.message.text
    if chosen_sphere == "⬅️ Назад":
        await update.message.reply_text(f"Поменять сферу",
                                        reply_markup=ReplyKeyboardMarkup([['Поменять сферу', '⬅️ Назад']],
                                                                         resize_keyboard=True), )
        return CHANGESPHERE
    if chosen_sphere == "Фабрика":
        context.user_data['sphere_status'] = 2
        crud.update_user_sphere(tel_id=update.message.from_user.id, sphere_status=2)
        await update.message.reply_text(f"Вы успешно поменяли сферу",
                                        reply_markup=ReplyKeyboardMarkup(manu_buttons, resize_keyboard=True))
        return MANU

    elif chosen_sphere == 'Розница':
        context.user_data['sphere_status'] = 1
        crud.update_user_sphere(tel_id=update.message.from_user.id, sphere_status=1)
        await update.message.reply_text(f"Вы успешно поменяли сферу",
                                        reply_markup=ReplyKeyboardMarkup(manu_buttons, resize_keyboard=True))
        return MANU
    else:
        await update.message.reply_text(f"choose one",
                                        reply_markup=ReplyKeyboardMarkup(buttons_sphere, resize_keyboard=True), )
        return CHOSENSPHERE


async def types(update: Update, context: ContextTypes.DEFAULT_TYPE):
    type_name = update.message.text
    if 'Арс' in type_name:
        context.user_data['page_number'] = 0
        context.user_data['type'] = 1
        if context.user_data['sphere_status'] == 1:
            request_db = crud.get_branch_list(sphere_status=1)
            reply_keyboard = transform_list(request_db, 2, 'name')
            reply_keyboard.insert(0, ['⬅️ Назад'])
            reply_keyboard.append(['<<<Предыдущий', 'Следующий>>>'])
            await update.message.reply_text(f"Выберите филиал или отдел:",
                                            reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
            return BRANCHES
            # request_db = requests.get(f"{BASE_URL}fillials/list/tg").json()

        else:
            # request_db = crud.getfillialchildfabrica(offset=0)
            # request_db = requests.get(f"{BASE_URL}get/fillial/fabrica/tg").json()
            managers = crud.get_arc_factory_managers()
            reply_keyboard = transform_list(managers, 2, 'name')
            reply_keyboard.insert(0, ['⬅️ Назад'])
            await  update.message.reply_text(
                'Выберите своего Бригадира:',
                          reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
            return ARCFACTORYMANAGER




    elif type_name == '⬅️ Назад':
        await update.message.reply_text(f"Главное меню",
                                        reply_markup=ReplyKeyboardMarkup(manu_buttons, resize_keyboard=True))
        return MANU
    elif type_name == 'Маркетинг📈':
        context.user_data['type'] = 3

        request_db = crud.get_branch_list_location()
        reply_keyboard = transform_list(request_db, 3, 'name')
        reply_keyboard.insert(0, ['⬅️ Назад'])
        await update.message.reply_text(f"Выберите филиал или отдел:",
                                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
        return MARKETINGSTBUTTON
    elif type_name == "Запрос машины🚛":
        # reply_keyboard = [['Арс🛠',"IT🧑‍💻"],['Маркетинг📈','Инвентарь📦'],['Запрос машины🚛','⬅️ Назад']]
        # await update.message.reply_text(f"Пожалуйста выберите направление:",reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
        # return TYPE
        context.user_data['page_number'] = 0
        context.user_data['type'] = 5
        order_car = [['Запросить на филиал', 'С адреса на адрес'], ['⬅️ Назад']]
        await update.message.reply_text('Тип', reply_markup=ReplyKeyboardMarkup(order_car, resize_keyboard=True))
        return CARSP
    elif type_name == 'Стафф питание🥘':
        context.user_data['page_number'] = 0
        context.user_data['type'] = 6
        time_work = crud.get_work_time()
        if is_time_between(start_time=time_work.from_time, end_time=time_work.to_time) is False:
            reply_keyboard = buttons_sphere_1
            await update.message.reply_text(f"Заявки на Стафф питание принимаются с 07:00 до 17:00 🕓",
                                            reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
            return TYPE

        request_db = crud.get_branch_list(sphere_status=1)
        reply_keyboard = transform_list(request_db, 2, 'name')

        reply_keyboard.insert(0, ['⬅️ Назад'])
        reply_keyboard.append(['<<<Предыдущий', 'Следующий>>>'])
        await update.message.reply_text(f"Выберите филиал или отдел:",
                                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))

        return BRANCHES
    elif type_name == 'IT🧑‍💻':
        # if int(context.user_data['sphere_status'])==2:
        #    reply_keyboard = buttons_sphere_2
        #    await update.message.reply_text(f"Этот пункт в разработке",reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
        # elif int(context.user_data['sphere_status'])==1:
        #    reply_keyboard = buttons_sphere_1
        #    await update.message.reply_text(f"Бот для подачи заявок в IT Отдел ➡️ @Safiatech_uzbot",reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
        # await update.message.reply_text("Пожалуйста введите пароль для доступа в IT Отдел",reply_markup=ReplyKeyboardRemove())
        # return IT_PASSWORD
        reply_keyboard_back = ['⬅️ Назад']

        context.user_data['type'] = 4
        context.user_data['page_number'] = 0
        # if context.user_data['sphere_status']==1:
        if int(context.user_data['sphere_status']) == 1:
            request_db = crud.get_branch_list(sphere_status=1)
            # request_db = requests.get(f"{BASE_URL}fillials/list/tg").json()
        else:
            reply_keyboard_back.append('Учтепа фабрика New')
            request_db = crud.getfillialchildfabrica(offset=0)
            # request_db = requests.get(f"{BASE_URL}fillials/list/tg").json()
        # else:
        #    request_db = crud.getfillialchildfabrica(offset=0)
        #    #request_db = requests.get(f"{BASE_URL}get/fillial/fabrica/tg").json()

        reply_keyboard = transform_list(request_db, 2, 'name')

        reply_keyboard.insert(0, reply_keyboard_back)
        reply_keyboard.append(['<<<Предыдущий', 'Следующий>>>'])
        await update.message.reply_text(f"Выберите филиал или отдел:",
                                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
        return BRANCHES

    elif type_name == 'Отзывы гостей✍':
        text_tosend = "@complaints_uzbot"
        await update.message.reply_text(f"Бот для подачи отзывов ➡️ {text_tosend}",
                                        reply_markup=ReplyKeyboardMarkup(manu_buttons, resize_keyboard=True))
        return MANU


    elif  'Инвентарь' in type_name:
        user = crud.get_user_tel_id(id=update.message.from_user.id)
        if context.user_data['sphere_status']:
            if int(context.user_data['sphere_status']) == 1:
                department = 2
            else:
                department = 10
        else:
            context.user_data['sphere_status'] = 1
            department = 2

        await update.message.reply_text(
            f"Пожалуйста нажмите кнопку: Инвентарь📦",

            reply_markup=ReplyKeyboardMarkup.from_button(
                KeyboardButton(
                    text="Инвентарь📦",
                    web_app=WebAppInfo(
                        url=f"{FRONT_URL}tg/inventory-request-add?key={create_access_token(user.username)}&department={department}")
                ), resize_keyboard=True))
        return INVETORY
    elif type_name == 'Видеонаблюдение🎥':
        context.user_data['type'] = 8
        request_db = crud.get_branch_list(sphere_status=int(context.user_data['sphere_status']))
        reply_keyboard = transform_list(request_db, 2, 'name')

        reply_keyboard.insert(0, ['⬅️ Назад'])
        reply_keyboard.append(['<<<Предыдущий', 'Следующий>>>'])
        await update.message.reply_text(f"Выберите филиал или отдел:",
                                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
        return BRANCHES
    elif type_name == 'Заявка на форму🥼':
        context.user_data['type'] = 9
        context.user_data['card'] = []
        request_db = crud.get_branch_list(sphere_status=1)
        reply_keyboard = transform_list(request_db, 2, 'name')

        reply_keyboard.insert(0, ['⬅️ Назад'])
        reply_keyboard.append(['<<<Предыдущий', 'Следующий>>>'])
        await update.message.reply_text(f"Выберите филиал или отдел:",
                                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
        return BRANCHES

    elif type_name == 'Монеты💰':
        context.user_data['type'] = 11
        request_db = crud.get_branch_list(sphere_status=1)
        reply_keyboard = transform_list(request_db, 2, 'name')
        reply_keyboard.insert(0, ['⬅️ Назад'])
        reply_keyboard.append(['<<<Предыдущий', 'Следующий>>>'])
        await update.message.reply_text(f"Выберите филиал или отдел:",
                                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
        return BRANCHES


    elif type_name == 'Официальное оформление 🧾':
        user = crud.get_user_tel_id(id=update.message.from_user.id)
        # print("username: ", user.username)
        # department = 12
        await update.message.reply_text(
            "Пожалуйста, выберите действие: ",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(
                            text="Оформление  🧾",
                            web_app=WebAppInfo(url=f"{FRONT_URL}tg/hr-registery/main?key={create_access_token(user.username)}")
                        ),
                        KeyboardButton(text="Шаблоны документов")
                    ],
                    [
                        KeyboardButton(text="⬅️ Назад")
                    ]
                ],
                resize_keyboard=True
            )
        )
        return OFFICIAL_EMPLOYMENT

    else:
        if int(context.user_data['sphere_status']) == 2:
            reply_keyboard = buttons_sphere_2
            await update.message.reply_text(f"Этот пункт в разработке",
                                            reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
        elif int(context.user_data['sphere_status']) == 1:
            reply_keyboard = buttons_sphere_1
            await update.message.reply_text(f"Этот пункт в разработке",
                                            reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
        return TYPE


async def official_employment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_input = update.message.text
    chat_id = update.message.chat.id
    if user_input == '⬅️ Назад':
        reply_keyboard = buttons_sphere_1

        await update.message.reply_text(f"Пожалуйста выберите направление:",
                                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
        return TYPE

    elif user_input == 'Шаблоны документов':
        folder_path = "/var/www/arc_bot_safia/employment_files"  # Replace with your folder path
        # folder_path = "C:\\Users\\User\Desktop\Projects\Service_Desk\\arc_bot_safia\employment_files"  # Replace with your folder path
        try:
            file_list = [
                os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))
            ]
            if not file_list:
                await update.message.reply_text("Папка файлов пуста")
                return
            media_group = [InputMediaDocument(media=open(file_path, "rb")) for file_path in file_list]
            await context.bot.send_media_group(
                chat_id=chat_id,
                media=media_group
            )
            # send files
        except:
            await update.message.reply_text(text="Нет файлов")



async def marketingstbutton(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == '⬅️ Назад':
        reply_keyboard = buttons_sphere_2

        await update.message.reply_text(f"Пожалуйста выберите направление:",
                                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
        return TYPE
    context.user_data['branch'] = update.message.text
    reply_keyboard = [['Проектная работа для дизайнеров', 'Для Терр. Менеджеров'], ['Видеография/Фото', '⬅️ Назад']]
    await update.message.reply_text(f"Пожалуйста выберите категорию",
                                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
    return MARKETINGCAT


async def marketingcat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    type_name = update.message.text
    if type_name == 'Для Терр. Менеджеров':
        data = crud.get_user_role(telegram_id=update.message.from_user.id)
        if data is None:
            reply_keyboard = [['Проектная работа для дизайнеров', 'Для Терр. Менеджеров', ],
                              ['Видеография/Фото', '⬅️ Назад']]
            await update.message.reply_text(f"Для вас этот пункт недоступен ❌ Выберите другую категорию",
                                            reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
            return MARKETINGCAT
    if type_name == '⬅️ Назад':
        request_db = crud.get_branch_list_location()
        reply_keyboard = transform_list(request_db, 3, 'name')
        reply_keyboard.insert(0, ['⬅️ Назад'])
        await update.message.reply_text(f"Выберите филиал или отдел:",
                                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
        return MARKETINGSTBUTTON
    id_cat = marketing_cat_dict[type_name]
    request_db = crud.get_category_list(sub_id=id_cat, sphere_status=context.user_data['sphere_status'],
                                        department=context.user_data['type'])
    reply_keyboard = transform_list(request_db, 3, 'name')
    reply_keyboard.append(['⬅️ Назад'])
    await update.message.reply_text(f"Пожалуйста выберите категорию проблемы:",
                                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))

    return CATEGORY


async def branches(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the info about the user and ends the conversation."""
    user_text = update.message.text
    if update.message.text == '⬅️ Назад':
        if context.user_data['sphere_status'] == 1:
            reply_keyboard = buttons_sphere_1
        if context.user_data['sphere_status'] == 2:
            reply_keyboard = buttons_sphere_2

        await update.message.reply_text(f"Пожалуйста выберите направление:",
                                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
        return TYPE
    if user_text == 'Следующий>>>':
        context.user_data['page_number'] = int(context.user_data['page_number']) + 1
        if context.user_data['sphere_status'] == 1:
            request_db = crud.get_branch_list(sphere_status=1)
            # request_db = requests.get(f"{BASE_URL}fillials/list/tg").json()
        else:
            request_db = crud.getfillialchildfabrica(offset=int(context.user_data['page_number']) * offsett)
        # request_db = crud.getfillialchildfabrica(offset=int(context.user_data['page_number'])*offsett)
        reply_keyboard = transform_list(request_db, 2, 'name')

        reply_keyboard.insert(0, ['⬅️ Назад'])
        reply_keyboard.append(['<<<Предыдущий', 'Следующий>>>'])
        await update.message.reply_text(f"Выберите филиал или отдел:",
                                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))

        return BRANCHES
    if user_text == '<<<Предыдущий':
        if int(context.user_data['page_number']) > 0:
            context.user_data['page_number'] = int(context.user_data['page_number']) - 1
        else:
            context.user_data['page_number'] = 0
        if context.user_data['sphere_status'] == 1:
            request_db = crud.get_branch_list(sphere_status=1)
            # request_db = requests.get(f"{BASE_URL}fillials/list/tg").json()
        else:
            request_db = crud.getfillialchildfabrica(offset=int(context.user_data['page_number']) * offsett)
        reply_keyboard = transform_list(request_db, 2, 'name')

        reply_keyboard.insert(0, ['⬅️ Назад'])
        reply_keyboard.append(['<<<Предыдущий', 'Следующий>>>'])
        await update.message.reply_text(f"Выберите филиал или отдел:",
                                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))

        return BRANCHES

    context.user_data['branch'] = update.message.text

    if context.user_data['type'] == 5:
        sphere_status = None
    if context.user_data['type'] == 6:
        reply_keyboard = [['⬅️ Назад']]
        await update.message.reply_text('Укажите количество порции еды',
                                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
        return MEALSIZE
    if int(context.user_data['type']) == 4:
        data = crud.get_category_list(department=4, sphere_status=4)
        context.user_data['itsphere'] = 'Обслуживание и тех.поддержка'
        reply_keyboard = transform_list(data, 3, 'name')
        reply_keyboard.append(['⬅️ Назад'])
        await update.message.reply_text('Выберите категорию заявки',
                                        reply_markup=ReplyKeyboardMarkup(keyboard=reply_keyboard, resize_keyboard=True))
        return ITCATEGORY
    if int(context.user_data['type']) == 7:
        reply_keyboard = [['⬅️ Назад']]
        await update.message.reply_text('Оставьте отзыв в виде текстового сообщения',
                                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
        return COMMENTTEXT
    if int(context.user_data['type']) == 8:
        reply_keyboard = [['⬅️ Назад']]
        await update.message.reply_text('Опишите пожалуйста событие в деталях',
                                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
        return VIDCOMMENT
    if int(context.user_data['type']) == 9:
        category_tools = crud.get_category_list(department=9)
        reply_keyboard = transform_list(category_tools, 3, 'name')
        reply_keyboard.append(['⬅️ Назад'])
        await update.message.reply_text('Выберите тип формы',
                                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
        return UNIFORMCATEGORIES
    if int(context.user_data['type'])==11:
        reply_keyboard = [['⬅️ Назад']]
        await update.message.reply_text('Пожалуйста, введите количество монет в числовом формате.',
                                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))

        return COINAMOUNT

    else:
        sphere_status = context.user_data['sphere_status']
    request_db = crud.get_category_list(sphere_status=sphere_status, department=int(context.user_data['type']))

    reply_keyboard = transform_list(request_db, 3, 'name')
    reply_keyboard.append(['⬅️ Назад'])
    await update.message.reply_text(f"Пожалуйста выберите категорию:",
                                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))

    return CATEGORY


async def category(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    inserted_data = update.message.text
    if inserted_data == '⬅️ Назад':
        if context.user_data['type'] == 1:
            if context.user_data['sphere_status'] == 1:

                request_db = crud.get_branch_list(sphere_status=1)
                context.user_data['page_number'] = 0
                request_db = crud.getfillialchildfabrica(offset=0)
                reply_keyboard = transform_list(request_db, 3, 'name')
                reply_keyboard.insert(0, ['⬅️ Назад'])
                reply_keyboard.append(['<<<Предыдущий', 'Следующий>>>'])
                await update.message.reply_text(f"Выберите филиал или отдел:",
                                                reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
                return BRANCHES
            else:

                devisions = crud.get_manager_divisions(manager_id=context.user_data['manager'])

                reply_keyboard = transform_list(devisions, 3, 'name')
                reply_keyboard.append(['⬅️ Назад'])
                await update.message.reply_text(f"Выберите филиал или отдел:",
                                                reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
                return ARCFACTORYDIVISIONS


        elif int(context.user_data['type']) == 5:
            if context.user_data['sphere_status'] == 1:

                request_db = crud.get_branch_list(sphere_status=1)
            else:
                context.user_data['page_number'] = 0
                request_db = crud.getfillialchildfabrica(offset=0)
            reply_keyboard = transform_list(request_db, 3, 'name')
            reply_keyboard.insert(0, ['⬅️ Назад'])
            reply_keyboard.append(['<<<Предыдущий', 'Следующий>>>'])
            await update.message.reply_text(f"Выберите филиал или отдел:",
                                            reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))

            return BRANCHES
        else:
            reply_keyboard = [['Проектная работа для дизайнеров', 'Для Терр. Менеджеров'],
                              ['Видеография/Фото', '⬅️ Назад']]
            await update.message.reply_text(f"Пожалуйста выберите категорию",
                                            reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
            return MARKETINGCAT
    context.user_data['category'] = update.message.text

    if int(context.user_data['type']) == 1:
        get_category = crud.getcategoryname(name=inserted_data, department=int(context.user_data['type']))

        if get_category.is_child:
            pass
        else:
            categories = crud.get_child_categories(category_id=get_category.id)
            if categories:
                reply_keyboard = transform_list(categories, 3, 'name')
                reply_keyboard.append(['⬅️ Назад'])
                await update.message.reply_text(f"Пожалуйста выберите категорию:",
                                                reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
                return CATEGORY
        reply_keyboard = [['⬅️ Назад']]
        await update.message.reply_text('Пожалуйста укажите название/модель оборудования',
                                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
        return PRODUCT
    elif int(context.user_data['type']) == 5:
        await update.message.reply_text("Укажите вес/размер",
                                        reply_markup=ReplyKeyboardMarkup([['⬅️ Назад']], resize_keyboard=True))
        return CHOOSESIZE
        # return CHOOSEMONTH
    elif int(context.user_data['type']) == 3:
        data = crud.getcategoryname(name=update.message.text, department=int(context.user_data['type']))
        if data.file:
            file = open(f"{backend_location}{data.file}", 'rb')
            await context.bot.send_photo(chat_id=update.message.from_user.id, photo=file)
        reply_keyboard = [['⬅️ Назад']]
        await update.message.reply_text('Пожалуйста напишите комментарии к заявке ',
                                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
        return DESCRIPTION


async def product(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == '⬅️ Назад':
        request_db = crud.get_category_list(sphere_status=context.user_data['sphere_status'],
                                            department=context.user_data['type'])
        reply_keyboard = transform_list(request_db, 3, 'name')
        reply_keyboard.insert(0, ['⬅️ Назад'])
        await update.message.reply_text(f"Пожалуйста выберите категорию проблемы:",
                                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))

        return CATEGORY
    reply_keyboard = [['⬅️ Назад']]
    context.user_data['product'] = update.message.text
    await update.message.reply_text('Пожалуйста напишите комментарии к заявке ',
                                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
    return DESCRIPTION


async def description(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [['⬅️ Назад']]
    if update.message.text == '⬅️ Назад':
        if int(context.user_data['type']) == 1:
            await update.message.reply_text('Пожалуйста укажите название/модель оборудования',
                                            reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
            return PRODUCT
        if int(context.user_data['type']) == 3:
            reply_keyboard = [['Проектная работа для дизайнеров', 'Для Терр. Менеджеров'],
                              ['Видеография/Фото', '⬅️ Назад']]
            await update.message.reply_text(f"Пожалуйста выберите категорию",
                                            reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
            return MARKETINGCAT
    context.user_data['description'] = update.message.text
    await update.message.reply_text('Пожалуйста укажите ваш номер телефона',
                                    reply_markup=ReplyKeyboardMarkup([['⬅️ Назад']], resize_keyboard=True))
    return PHONENUMBER


async def phonenumber(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text:
        if update.message.text == '⬅️ Назад':
            reply_keyboard = [['⬅️ Назад']]
            await update.message.reply_text('Пожалуйста напишите комментарии к заявке ',
                                            reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
            return DESCRIPTION
    if update.message.contact:
        context.user_data['phone_number'] = update.message.contact.phone_number
    else:
        context.user_data['phone_number'] = update.message.text
    await update.message.reply_text('Отправьте фотографию или файл:',
                                    reply_markup=ReplyKeyboardMarkup([['⬅️ Назад', 'Далее➡️']], resize_keyboard=True))
    context.user_data['files'] = []
    return FILES


async def files(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text:
        if update.message.text == '⬅️ Назад':
            reply_keyboard = [['⬅️ Назад']]
            await update.message.reply_text('Пожалуйста напишите комментарии к заявке ',
                                            reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
            return DESCRIPTION
        if update.message.text == 'Далее➡️':
            if not context.user_data['files']:
                await update.message.reply_text('Пожалуйста отправьте фотографию или файл:',
                                                reply_markup=ReplyKeyboardMarkup([['⬅️ Назад', 'Далее➡️']],
                                                                                 resize_keyboard=True))
                return FILES

            category_query = crud.getcategoryname(name=context.user_data['category'],
                                                  department=int(context.user_data['type']))
            if int(context.user_data['type']) == 1 and int(context.user_data['sphere_status']) == 2:
                fillial_id = context.user_data['division_id']
            else:

                fillial_query = crud.getchildbranch(fillial=context.user_data['branch'],
                                                    type=int(context.user_data['type']),
                                                    factory=int(context.user_data['sphere_status']))
                fillial_id = fillial_query.id
            user_query = crud.get_user_tel_id(id=update.message.from_user.id)
            list_data = [None, 'АРС🛠', None, 'Маркетингу📈']
            if context.user_data['type'] == 3:
                product = None
            if context.user_data['type'] == 1:
                product = context.user_data['product']
            if category_query.ftime:
                finishing_time = datetime.datetime.now(tz=timezonetash)+datetime.timedelta(hours=category_query.ftime)
            else:
                finishing_time = None

            add_request = crud.add_request(is_bot=1, category_id=category_query.id, fillial_id=fillial_id,
                                           product=product, description=context.user_data['description'],
                                           user_id=user_query.id, phone_number=context.user_data['phone_number'],finishing_time=finishing_time)
            keyboard = [
            ]

            for file in context.user_data['files']:
                file_url = f"files/{file}"
                crud.create_files(request_id=add_request.id, filename=file_url)
                keyboard.append({'text': 'Посмотреть фото/видео', "url": f"{BASE_URL}{file_url}"})

            formatted_datetime_str = add_request.created_at.strftime("%d.%m.%Y %H:%M")
            formatted_finishing_time = (add_request.created_at + datetime.timedelta(hours=add_request.sla)).strftime("%d.%m.%Y %H:%M")
            if add_request.category_sphere_status == 1 and add_request.category_department == 1:
                fillial_name = f"📍*Филиал*: {add_request.parentfillial_name}"
            else:
                fillial_name = f"📍*Бригадир*: {add_request.manager_name}\n📍*Отдел*: {add_request.fillial_name}"

            text = (
                f"📑*Заявка №* {add_request.id}\n\n"
                f"{fillial_name}\n"
                f"🕘*Время поступления*: {formatted_datetime_str}\n"
                f"🕘*Время выполнения до*: {formatted_finishing_time}\n"
                f"🔰*Категория проблемы*: {add_request.category.name}\n"
                f"⚙️*Название оборудования*: {add_request.product}\n"
                f"💬*Комментарии*: {add_request.description}\n\n"
            )

            if add_request.category_sphere_status == 1 and add_request.category_department == 1:
                sendtotelegram(bot_token=BOTTOKEN, chat_id='-1001920671327', message_text=text, buttons=keyboard)
            if add_request.category.sphere_status == 2 and add_request.category.department == 1:
                sendtotelegram(bot_token=BOTTOKEN, chat_id='-1001831677963', message_text=text, buttons=keyboard)
            await update.message.reply_text(
                f"Спасибо, ваша заявка #{add_request.id}s по {list_data[context.user_data['type']]} принята. "
                f"Как ваша заявка будет назначена в работу ,вы получите уведомление.\n\n"
                f"Время поступления: {formatted_datetime_str}\n"
                f"Время выполнения до: {formatted_finishing_time}",
                reply_markup=ReplyKeyboardMarkup(manu_buttons, resize_keyboard=True))




            if add_request.category_department==3 and add_request.category_telegram is not None:
                text = f"Заказ: #{add_request.id}\n"
                group_photo = []
                as_reply = []
                suff_list = ['jpg', 'png','JPG']
                count = 0
                for file in context.user_data['files']:
                    if str(file).endswith(tuple(suff_list)) and count==0:
                        group_photo.append(InputMediaPhoto(open(f"{backend_location}files/{file}", 'rb'),caption=text))
                    if str(file).endswith(tuple(suff_list)) and count!=0:
                        group_photo.append(InputMediaPhoto(open(f"{backend_location}files/{file}", 'rb')))
                    else:

                        as_reply.append(file)
                    count+=1
                if group_photo:

                    sended_message = await context.bot.send_media_group(
                        media=group_photo,
                        chat_id=add_request.category_telegram,
                    )
                else:
                    sended_message = await context.bot.send_message(
                        chat_id=add_request.category_telegram,
                        text=text,
                    )

                if as_reply:
                    for i in as_reply:
                        with open(f"{backend_location}files/{i}", 'rb') as f:
                            await context.bot.send_document(
                                document=f,
                                reply_to_message_id=sended_message[0].message_id,
                                chat_id=add_request.category_telegram,
                            )

                # await context.bot.send_media_group(
                #     caption=
                # )



            context.user_data['files'] = []
            return MANU



    else:

        # ile = update.message.document.get_file()
        # with open(file, 'rb') as f:
        #    print(f)
        # update.message.document().get_file()
        if update.message.document:
            # context.user_data['file_url']=f"files/{update.message.document.file_name}"
            file_id = update.message.document.file_id
            file_name = update.message.document.file_name
            new_file = await context.bot.get_file(file_id=file_id)

            file_content = await new_file.download_as_bytearray()
            files_open = {'files': file_content}
        if update.message.photo:
            file_name = f"{update.message.photo[-1].file_id}.jpg"
            getFile = await context.bot.getFile(update.message.photo[-1].file_id)
            file_content = await getFile.download_as_bytearray()
            files_open = {'files': file_content}
        with open(f"{backend_location}files/{file_name}", 'wb+') as f:
            f.write(file_content)
            f.close()
        context.user_data['files'].append(file_name)
        await update.message.reply_text('Фото добавлено:', reply_markup=ReplyKeyboardMarkup([['⬅️ Назад', 'Далее➡️']],
                                                                                            resize_keyboard=True))
        return FILES


async def addcomment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_option = update.message.text
    user_id = update.message.from_user.id
    user = crud.get_user_tel_id(id=user_id)
    crud.addcomment(user_id=user.id, comment=user_option, request_id=context.user_data['request_id'])
    await update.message.reply_text(f"Главное меню",
                                    reply_markup=ReplyKeyboardMarkup(manu_buttons, resize_keyboard=True))
    return MANU


# -------------------------------BRIGADA MANU-----------------------------------------


async def brig_manu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_choose = update.message.text
    user_id = update.message.from_user.id
    if user_choose == 'Мои заказы 📋':
        user = crud.get_user_tel_id(id=update.message.from_user.id)
        request_db = crud.tg_get_request_list(brigada_id=user.brigada_id)
        message_brig = generate_text(request_db)

        reply_keyboard = transform_list(request_db, 3, 'id')
        if not reply_keyboard:
            reply_keyboard = [['Мои заказы 📋']]
            await update.message.reply_text(
                f"У вашей бригады на данный момент нет заявок !",
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
            return BRIG_MANU
        reply_keyboard.insert(0, ['⬅️ Назад'])
        await update.message.reply_text(message_brig,
                                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
        return ORDERSTG
    elif user_choose == 'Адреса Филиалов📍':
        request_db = crud.get_branch_list_location()
        reply_keyboard = transform_list(request_db, 3, 'name')
        reply_keyboard.insert(0, ['⬅️ Назад'])
        await update.message.reply_text(f"Выберите филиал",
                                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
        return LOCATION_BRANCH
    else:
        reply_keyboard = [['Мои заказы 📋']]
        await update.message.reply_text(
            f"Главное меню", reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
        return BRIG_MANU


isTrue = {0: 'No', 1: 'Yes'}


async def orderstg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uservalue = update.message.text
    if uservalue == '⬅️ Назад':
        reply_keyboard = [['Мои заказы 📋']]
        await update.message.reply_text("Главное меню",
                                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
        return BRIG_MANU
    uservalue = int(uservalue)
    context.user_data['last_request'] = uservalue
    request_db = crud.get_request_id(id=uservalue)
    reply_keyboard = [['Завершить ✅'], ['Забрать на ремонт 🛠'], ['⬅️ Назад']]
    if request_db.status == 2 or request_db.category_department == 4:
        reply_keyboard = [['Завершить ✅'], ['⬅️ Назад']]

    keyboard = [
    ]
    if request_db.file_url is not None:
        keyboard.append([InlineKeyboardButton('Посмотреть фото/видео', url=f"{BASE_URL}{request_db.file_url}")])

    if request_db.category_sphere_status == 1 and request_db.category_department == 1:
        fillial_name = f"📍*Филиал*: {request_db.parentfillial_name}"
    else:
        fillial_name = f"📍*Отдел*: {request_db.parentfillial_name}\n📍*Бригадир*:  {request_db.fillial_name}"



    # parsed_datetime = datetime.strptime(request_db.created_at,"%Y-%m-%dT%H:%M:%S.%f")

    formatted_datetime_str = request_db.created_at.strftime("%Y-%m-%d %H:%M")
    await update.message.reply_text(f"📑Заявка № {request_db.id}\n\n {fillial_name}\n" \
                                    f"🕘Дата поступления заявки: {formatted_datetime_str}\n\n" \
                                    f"🔰Категория проблемы: {request_db.category_name}\n" \
                                    f"⚙️Название оборудования: {request_db.product}\n" \
                                    f"📱Номер телефона: +{request_db.user_phone_number}\n" \
                                    f"🥷Имя: {request_db.user_full_name}\n" \
                                    f"💬Комментарии: {request_db.description}",
                                    reply_markup=InlineKeyboardMarkup(keyboard))
    await update.message.reply_text(f"📑Заявка #{request_db.id}s",
                                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
    # if request_db.file:
    #    for i in request_db.file:
    #        await update.message.reply_document(document=open(f"{backend_location}{i.url}",'rb'))
    return FINISHING


async def finishing(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_button = update.message.text
    if user_button == '⬅️ Назад':
        # user = crud.get_user_tel_id(id=update.message.from_user.id)
        reply_keyboard = [['Мои заказы 📋']]
        await update.message.reply_text(
            f"Главное меню", reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
        return BRIG_MANU

    # ------------------this is it request closing data-------------------

    if user_button == 'Завершить ✅':
        request_db = crud.get_request_id(id=context.user_data['last_request'])
        if request_db.category_department == 4:
            await update.message.reply_text("Входной фотоотчет",
                                            reply_markup=ReplyKeyboardMarkup([['⬅️ Назад', "Пропустить"]],
                                                                             resize_keyboard=True))
            return ITPHOTOREPORT

        # ------------------this is it end of request closing data-------------------

        user_data = crud.get_user_tel_id(id=update.message.from_user.id)
        reply_keyboard = [['Мои заказы 📋']]
        await update.message.reply_text(
            f"Пожалуйста внесите расход на заявку №{context.user_data['last_request']}",
            reply_markup=ReplyKeyboardMarkup.from_button(
                KeyboardButton(
                    text="Внести расход",
                    web_app=WebAppInfo(
                        url=f"https://admin.service.safiabakery.uz/tg/add-product/{context.user_data['last_request']}?key={create_access_token(user_data.username)}"),
                ), resize_keyboard=True)
        )
        return CLOSEBUTTON

        # requests.put(f"{BASE_URL}tg/request",json={'request_id':int(context.user_data['last_request']),'status':3})
    if user_button == 'Забрать на ремонт 🛠':
        crud.tg_update_requst_st(requestid=context.user_data['last_request'], status=2)

    reply_keyboard = [['Мои заказы 📋']]
    await update.message.reply_text(
        f"Главное меню", reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
    return BRIG_MANU


async def closebutton(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = json.loads(update.effective_message.web_app_data.data)
    reply_keyboard = [['Мои заказы 📋']]
    await update.message.reply_text("Главное меню",
                                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
    return BRIG_MANU


async def it_photo_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    request_db = crud.get_request_id(id=context.user_data['last_request'])

    if update.message.text:
        if update.message.text == '⬅️ Назад':
            reply_keyboard = [['Мои заказы 📋']]
            await update.message.reply_text("Главное меню",
                                            reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
            return BRIG_MANU


    else:

        if update.message.document:
            # context.user_data['file_url']=f"files/{update.message.document.file_name}"
            file_id = update.message.document.file_id
            file_name = update.message.document.file_name
            new_file = await context.bot.get_file(file_id=file_id)

            file_content = await new_file.download_as_bytearray()
        if update.message.photo:
            file_name = f"{update.message.photo[-1].file_id}.jpg"
            getFile = await context.bot.getFile(update.message.photo[-1].file_id)
            file_content = await getFile.download_as_bytearray()

        with open(f"{backend_location}files/{file_name}", 'wb+') as f:
            f.write(file_content)
            f.close()
        # request_db = crud.get_request_id(id=context.user_data['last_request'])
        add_file = crud.create_files(request_id=request_db.id, filename=f"files/{file_name}", status=1)

    # finish request data
    request_list = crud.tg_update_requst_st(requestid=context.user_data['last_request'], status=6)
    department = request_list.category_department
    if department == 4:
        await context.bot.delete_message(chat_id=IT_SUPERGROUP, message_id=request_list.tg_message_id)
        delete_job_id = f"delete_message_for_{request_list.id}"
        job_scheduler.remove_job(job_id=delete_job_id)
        send_job_id = f"send_message_for_{request_list.id}"
        job_scheduler.remove_job(job_id=send_job_id)

        formatted_created_time = request_list.created_at.strftime("%d.%m.%Y %H:%M")
        formatted_finishing_time = request_list.finishing_time.strftime("%d.%m.%Y %H:%M") if request_list.finishing_time is not None else None
        request_text = f"📑Заявка #{request_list.id}s\n\n" \
                       f"📍Филиал: {request_list.parentfillial_name}\n" \
                       f"👨‍💼Сотрудник: {request_list.user_full_name}\n" \
                       f"📱Номер телефона сотрудника: +{request_list.user_phone_number}\n" \
                       f"📱Номер телефона для заявки: {request_list.phone_number}\n" \
                       f"🔰Категория проблемы: {request_list.category_name}\n" \
                       f"🕘Дата поступления заявки: {formatted_created_time}\n" \
                       f"🕘Дата дедлайна заявки: {formatted_finishing_time}\n" \
                       f"❗️SLA: {request_list.sla} часов\n" \
                       f"💬Комментарии: {request_list.description}"
        text = f'{request_text}\n\n' \
               f'Статус вашей заявки:  Завершен ✅'

        keyboard = [
            [InlineKeyboardButton("Выполнен/Принимаю", callback_data='user_accept'),
             InlineKeyboardButton("Не выполнен/Не принимаю", callback_data='user_not_accept')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        user_message = await context.bot.send_message(chat_id=request_list.user_telegram_id, text=text,
                                                      reply_markup=reply_markup, parse_mode='HTML')
        context.user_data["user_message_id"] = user_message.message_id

    else:
        text_request = f"Уважаемый {request_list.user_full_name} , Ваша заявка #{request_list.id}s ИТ решена. \nПожалуйста, подтвердите, что она выполнена в соответствии с вашим запросом."
        # send message to request owner to rate request
        confirmation_request(bot_token=BOTTOKEN, chat_id=request_list.user_telegram_id, message_text=text_request)

    reply_keyboard = [['Мои заказы 📋']]
    await update.message.reply_text(
        f"Заявка решена", reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
    return BRIG_MANU


async def location_branch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chosen_branch = update.message.text
    if chosen_branch == '⬅️ Назад':
        await update.message.reply_text("Главное меню",
                                        reply_markup=ReplyKeyboardMarkup(manu_buttons, resize_keyboard=True))
        return MANU
    repsonsedata = crud.getfillialname(name=chosen_branch)

    await update.message.reply_location(latitude=repsonsedata.latitude, longitude=repsonsedata.longtitude,
                                        reply_markup=ReplyKeyboardMarkup(manu_buttons, resize_keyboard=True))

    return MANU


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    await update.message.reply_text(
        "bye", reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


async def check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_check_query = crud.get_user_tel_id(id=update.message.from_user.id)
    # user_check = requests.get(f"{BASE_URL}tg/check/user?telegram_id={update.message.from_user.id}")
    if user_check_query.brigada_id:

        reply_keyboard = [['Мои заказы 📋']]
        await update.message.reply_text(
            f"🧑‍🔧Ваша команда - {user_check_query.brigada_name}",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
        )
        return BRIG_MANU
    else:
        await update.message.reply_text(
            "Главное меню", reply_markup=ReplyKeyboardMarkup(manu_buttons, resize_keyboard=True)
        )
        return MANU


async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    # message = query.message.text
    blank_reply_murkup = [[]]
    text_of_order = query.message.text
    requests_id = re.findall(r'\d+', text_of_order)[0]
    context.user_data['request_id'] = requests_id
    # if selected_option is less than 0 it is about yes or no
    user = crud.get_user_tel_id(id=query.from_user.id)
    one_request = crud.get_request(id=requests_id)

    # if one_request.status== 3 and int(selected_option)==4:
    #    await context.bot.send_message(query.from_user.id,'please enter comment',reply_markup=ReplyKeyboardRemove())
    #    return ADDCOMMENT

    department = one_request.category_department
    if department == 4:
        callback_data = query.data
        request = crud.get_request_id(requests_id)
        finishing_time = request.finishing_time
        message_id = query.message.message_id
        sla = request.sla
        delta_minutes = 0
        if sla == 1:
            delta_minutes = 40
        elif sla == 1.5:
            delta_minutes = 60
        elif sla == 2:
            delta_minutes = 90
            # delta_minutes = 2
        elif sla == 8:
            delta_minutes = 360
        elif sla == 24:
            delta_minutes = 1200
        elif sla == 48:
            delta_minutes = 1920
        elif sla == 72:
            delta_minutes = 2880
        elif sla == 96:
            delta_minutes = 4320
        elif sla == 0.05:
            delta_minutes = 2

        delay = datetime.timedelta(minutes=delta_minutes)
        deleting_scheduled_time = request.created_at + delay - datetime.timedelta(seconds=2)
        sending_scheduled_time = request.created_at + delay

        formatted_created_time = request.created_at.strftime("%d.%m.%Y %H:%M")
        formatted_finishing_time = request.finishing_time.strftime("%d.%m.%Y %H:%M") if request.finishing_time is not None else None
        request_text = f"📑Заявка #{request.id}s\n\n" \
                       f"📍Филиал: {request.parentfillial_name}\n" \
                       f"👨‍💼Сотрудник: {request.user_full_name}\n" \
                       f"📱Номер телефона сотрудника: +{request.user_phone_number}\n" \
                       f"📱Номер телефона для заявки: {request.phone_number}\n" \
                       f"🔰Категория проблемы: {request.category_name}\n" \
                       f"🕘Дата поступления заявки: {formatted_created_time}\n" \
                       f"🕘Дата дедлайна заявки: {formatted_finishing_time}\n" \
                       f"❗️SLA: {request.sla} часов\n" \
                       f"💬Комментарии: {request.description}"

        if callback_data == "accept_action" or callback_data == "back_to_accept_action":
            new_keyboard = [
                [
                    InlineKeyboardButton("Подтвердить", callback_data='confirm_request'),
                    InlineKeyboardButton("Изменить категорию", callback_data='change_request_category')
                ],
                [InlineKeyboardButton("Назад ⬅️", callback_data='cancel_action')]
            ]
            new_reply_markup = InlineKeyboardMarkup(new_keyboard)

            # Edit only the inline buttons (reply markup)
            await query.edit_message_reply_markup(reply_markup=new_reply_markup)

        elif callback_data == "change_request_category" or callback_data == "back_to_change_request_category":
            category_list = crud.get_category_list(department=4, sphere_status=4)
            new_keyboard = [[InlineKeyboardButton(f"{item.name}", callback_data=f'{item.id}') for item in category_list[i:i + 3]] for i in range(0, len(category_list), 3)]
            new_keyboard.append([InlineKeyboardButton("Назад ⬅️", callback_data='back_to_accept_action')])
            new_reply_markup = InlineKeyboardMarkup(new_keyboard)
            await query.edit_message_reply_markup(reply_markup=new_reply_markup)

        elif callback_data.isdigit():
            category_id = int(callback_data)
            category_list = crud.get_child_category(parent_id=category_id)
            if not category_list:
                request = crud.update_it_request(id=request.id, category_id=category_id)
                formatted_created_time = request.created_at.strftime("%d.%m.%Y %H:%M")
                formatted_finishing_time = request.finishing_time.strftime("%d.%m.%Y %H:%M") if request.finishing_time is not None else None
                request_text = f"📑Заявка #{request.id}s\n\n" \
                               f"📍Филиал: {request.parentfillial_name}\n" \
                               f"👨‍💼Сотрудник: {request.user_full_name}\n" \
                               f"📱Номер телефона сотрудника: +{request.user_phone_number}\n" \
                               f"📱Номер телефона для заявки: {request.phone_number}\n" \
                               f"🔰Категория проблемы: {request.category_name}\n" \
                               f"🕘Дата поступления заявки: {formatted_created_time}\n" \
                               f"🕘Дата дедлайна заявки: {formatted_finishing_time}\n" \
                               f"❗️SLA: {request.sla} часов\n" \
                               f"💬Комментарии: {request.description}"
                new_keyboard = [
                    [
                        InlineKeyboardButton("Подтвердить", callback_data='confirm_request'),
                        InlineKeyboardButton("Изменить категорию", callback_data='change_request_category')
                    ],
                    [InlineKeyboardButton("Назад ⬅️", callback_data='cancel_action')]
                ]
                new_reply_markup = InlineKeyboardMarkup(new_keyboard)
                await query.edit_message_text(text=request_text, reply_markup=new_reply_markup)

                message_text = f"Уважаемый {request.user_full_name}, категория вашей заявки #{request.id}s " \
                               f"изменен на: {request.category_name}\n" \
                               f"Время выполнения: {request.sla} часов"

                try:
                    await context.bot.send_message(chat_id=request.user_telegram_id, text=message_text)
                except:
                    pass

                await query.answer("Категория успешно изменена!")
            else:
                try:
                    new_keyboard = [
                        [InlineKeyboardButton(f"{item.name}", callback_data=f'{item.id}') for item in category_list[i:i + 3]]
                        for i in range(0, len(category_list), 3)
                    ]
                    new_keyboard.append([InlineKeyboardButton("Назад ⬅️", callback_data='back_to_change_request_category')])
                    new_reply_markup = InlineKeyboardMarkup(new_keyboard)
                    await query.edit_message_reply_markup(reply_markup=new_reply_markup)
                except BadRequest as e:
                    request = crud.update_it_request(id=request.id, category_id=category_id)
                    formatted_created_time = request.created_at.strftime("%d.%m.%Y %H:%M")
                    formatted_finishing_time = request.finishing_time.strftime("%d.%m.%Y %H:%M") if request.finishing_time is not None else None
                    request_text = f"📑Заявка #{request.id}s\n\n" \
                                   f"📍Филиал: {request.parentfillial_name}\n" \
                                   f"👨‍💼Сотрудник: {request.user_full_name}\n" \
                                   f"📱Номер телефона сотрудника: +{request.user_phone_number}\n" \
                                   f"📱Номер телефона для заявки: {request.phone_number}\n" \
                                   f"🔰Категория проблемы: {request.category_name}\n" \
                                   f"🕘Дата поступления заявки: {formatted_created_time}\n" \
                                   f"🕘Дата дедлайна заявки: {formatted_finishing_time}\n" \
                                   f"❗️SLA: {request.sla} часов\n" \
                                   f"💬Комментарии: {request.description}"
                    new_keyboard = [
                        [
                            InlineKeyboardButton("Подтвердить", callback_data='confirm_request'),
                            InlineKeyboardButton("Изменить категорию", callback_data='change_request_category')
                        ],
                        [InlineKeyboardButton("Назад ⬅️", callback_data='cancel_action')]
                    ]
                    new_reply_markup = InlineKeyboardMarkup(new_keyboard)
                    await query.edit_message_text(text=request_text, reply_markup=new_reply_markup)

                    message_text = f"Уважаемый {request.user_full_name}, категория вашей заявки #{request.id}s " \
                                   f"изменен на: {request.category_name}\n" \
                                   f"Время выполнения: {request.sla} часов"

                    try:
                        await context.bot.send_message(chat_id=request.user_telegram_id, text=message_text)
                    except:
                        pass

                    await query.answer("Категория успешно изменена!")

        elif callback_data == "confirm_request":
            if user.brigada_id:
                request = crud.update_it_request(id=request.id, brigada_id=user.brigada_id, status=1)
                topic_id = request.topic_id
                message_text = f"Уважаемый {request.user_full_name}, статус вашей заявки #{request.id}s " \
                               f"назначен специалист👨‍💻: {request.brigada_name}\n" \
                               f"Время выполнения: {request.sla} часов"

                try:
                    await context.bot.send_message(chat_id=request.user_telegram_id, text=message_text)
                except:
                    pass

                delete_from_chat(message_id=request.tg_message_id, topic_id=topic_id)
                message_id = send_notification(
                    topic_id=topic_id,
                    text=request_text,
                    finishing_time=finishing_time,
                    request_id=request.id,
                    url=request.file_url
                )
                if delta_minutes > 0:
                    delete_job_id = f"delete_message_for_{request.id}"
                    job_scheduler.add_delete_message_job(
                        job_id=delete_job_id,
                        scheduled_time=deleting_scheduled_time,
                        message_id=message_id,
                        topic_id=topic_id
                    )
                    send_job_id = f"send_message_for_{request.id}"
                    job_scheduler.add_send_message_job(
                        job_id=send_job_id,
                        scheduled_time=sending_scheduled_time,
                        topic_id=topic_id,
                        request_text=request_text,
                        finishing_time=finishing_time,
                        request_id=request.id,
                        request_file=request.file_url
                    )

            else:
                await query.answer(text="Вы не можете принять заявку, вы не являетесь исполнителем!", show_alert=True)

        elif callback_data == "cancel_action":
            new_keyboard = [
                [InlineKeyboardButton("Принять заявку", callback_data='accept_action')],
                [InlineKeyboardButton("Посмотреть фото", url=f"{BASE_URL}{request.file_url}")]
            ]
            new_reply_markup = InlineKeyboardMarkup(new_keyboard)
            # Edit only the inline buttons (reply markup)
            await query.edit_message_reply_markup(reply_markup=new_reply_markup)

        elif callback_data == "complete_request":
            if user.brigada_id == request.brigada_id:
                await query.delete_message()
                request = crud.update_it_request(id=requests_id, status=6)
                delete_job_id = f"delete_message_for_{request.id}"
                job_scheduler.remove_job(job_id=delete_job_id)
                send_job_id = f"send_message_for_{request.id}"
                job_scheduler.remove_job(job_id=send_job_id)

                text = f'{request_text}\n\n' \
                       f'Статус вашей заявки:  Завершен ✅'

                keyboard = [
                    [InlineKeyboardButton("Выполнен/Принимаю", callback_data='user_accept'),
                     InlineKeyboardButton("Не выполнен/Не принимаю", callback_data='user_not_accept')]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)

                user_message = await context.bot.send_message(chat_id=request.user_telegram_id, text=text,
                                                              reply_markup=reply_markup, parse_mode='HTML')
                context.user_data["user_message_id"] = user_message.message_id
            else:
                await query.answer(text="Вы не можете завершить заявку, вы не являетесь исполнителем этой заявки!\n"
                                        f"Исполнитель: {request.brigada_name}", show_alert=True)

            # if user.brigada_id == request.brigada_id:
            #     request = crud.update_it_request(id=requests_id, status=6)
            #     started_at = request.started_at
            #     finished_at = datetime.datetime.now(tz=ittech.timezonetash)
            #     finished_time = finished_at - started_at
            #
            #     job_id = f"delete_send_message_for_{request.id}"
            #     try:
            #         scheduler.remove_job(job_id=job_id)
            #         # print(f"'{job_id}' job was removed before scheduling")
            #     except JobLookupError:
            #         print(f"'{job_id}' job not found or already has completed !")
            #
            #     text = f"<s>{request_text}</s>\n\n" \
            #            f"<b> ✅ Вы завершили заявку за:</b>  {str(finished_time).split('.')[0]}"
            #     new_keyboard = [
            #         [InlineKeyboardButton("Возобновить", callback_data='resume_request')]
            #     ]
            #     new_reply_markup = InlineKeyboardMarkup(new_keyboard)
            #     await query.edit_message_text(text=text, reply_markup=new_reply_markup, parse_mode='HTML')
            #
            #     text = f'{request_text}\n\n' \
            #            f'Статус вашей заявки:  Завершен ✅'
            #
            #     keyboard = [
            #         [InlineKeyboardButton("Выполнен/Принимаю", callback_data='user_accept'),
            #          InlineKeyboardButton("Не выполнен/Не принимаю", callback_data='user_not_accept')]
            #     ]
            #     reply_markup = InlineKeyboardMarkup(keyboard)
            #
            #     user_message = await context.bot.send_message(chat_id=request.user_telegram_id, text=text,
            #                                                   reply_markup=reply_markup, parse_mode='HTML')
            #     context.user_data["user_message_id"] = user_message.message_id
            # else:
            #     await query.answer(text="Вы не можете завершить заявку, вы не являетесь исполнителем этой заявки!\n"
            #                             f"Исполнитель: {request.brigada_name}", show_alert=True)

        elif callback_data == "cancel_request":
            if user.brigada_id == request.brigada_id:
                keyboard = [
                    [InlineKeyboardButton("Не правильная заявка", callback_data='deny_reason=Не правильная заявка')],
                    [InlineKeyboardButton("Повторная заявка", callback_data='deny_reason=Повторная заявка')],
                    [InlineKeyboardButton("Тестовая заявка", callback_data='deny_reason=Тестовая заявка')],
                    [InlineKeyboardButton("Не смогли дозвониться 5 раз за 30мин", callback_data='deny_reason=Не смогли дозвониться')],
                    # [InlineKeyboardButton("Другое", callback_data='deny_reason=Другое')],
                    [InlineKeyboardButton("⬅️ Назад", callback_data='deny_reason=Назад к командам')]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await query.edit_message_reply_markup(reply_markup=reply_markup)
            else:
                await query.answer(text="Вы не можете отменить заявку, вы не являетесь исполнителем этой заявки!\n"
                                        f"Исполнитель: {request.brigada_name}", show_alert=True)

        elif callback_data.startswith("deny_reason"):
            deny_reason = callback_data.split(sep="=")[1]
            if deny_reason == "Назад к командам":
                keyboard = [
                    [InlineKeyboardButton("Завершить заявку", callback_data='complete_request'),
                     InlineKeyboardButton("Отменить", callback_data='cancel_request')],
                    [InlineKeyboardButton("Посмотреть фото", url=f"{BASE_URL}{request.file_url}")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await query.edit_message_reply_markup(reply_markup=reply_markup)
            else:
                if deny_reason == 'Не смогли дозвониться':
                    deny_reason += ' 5 раз за 30мин'
                await query.delete_message()
                request = crud.update_it_request(id=request.id, status=8, deny_reason=deny_reason)
                delete_job_id = f"delete_message_for_{request.id}"
                job_scheduler.remove_job(job_id=delete_job_id)
                send_job_id = f"send_message_for_{request.id}"
                job_scheduler.remove_job(job_id=send_job_id)

                context.user_data['request_id'] = request.id

                # text = f"{request_text}\n\n" \
                #        f"<b>Заявка отменена 🚫</b>\n" \
                #        f"Причина отмены: {deny_reason}"
                # await query.edit_message_text(text=text, reply_markup=None, parse_mode='HTML')

                message_text = f"❌Ваша заявка #{request.id}s по IT👨🏻‍💻 отменена по причине: {request.deny_reason}\n\n" \
                               f"Если Вы с этим не согласны, поставьте, пожалуйста, " \
                               f"рейтинг нашему решению по Вашей заявке от 1 до 5, и напишите свои комментарий."

                url = f"{FRONT_URL}tg/order-rating/{request.id}?user_id={request.user_id}&department={request.category_department}&sub_id={request.category_sub_id}"
                inlinewebapp(
                    bot_token=BOTTOKEN,
                    chat_id=request.user_telegram_id,
                    message_text=message_text,
                    url=url
                )

        # elif callback_data == "resume_request":
        #     if user.brigada_id == request.brigada_id:
        #         request = crud.update_it_request(id=request.id, status=7)
        #         user_text = f'{request_text}\n\n' \
        #                     f'Статус вашей заявки:  Возобновлен 🔄'
        #         await context.bot.edit_message_text(text=user_text, chat_id=request.user_telegram_id,
        #                                             message_id=context.user_data['user_message_id'], reply_markup=None)
        #
        #         now = datetime.datetime.now(tz=ittech.timezonetash)
        #         remaining_time = finishing_time - now
        #         late_time = now - finishing_time
        #         if finishing_time >= now:
        #             text = f"{request_text}\n\n" \
        #                    f"<b> ‼️ Оставщиеся время:</b>  {str(remaining_time).split('.')[0]}"
        #         else:
        #             text = f"{request_text}\n\n" \
        #                    f"<b> ‼️ Просрочен на:</b>  {str(late_time).split('.')[0]}"
        #
        #         keyboard = [
        #             [InlineKeyboardButton("Завершить заявку", callback_data='complete_request'),
        #              InlineKeyboardButton("Отменить", callback_data='cancel_request')]
        #         ]
        #         reply_markup = InlineKeyboardMarkup(keyboard)
        #         await query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode='HTML')
        #
        #         if delta_minutes > 0:
        #             job_id = f"delete_send_message_for_{request.id}"
        #             try:
        #                 scheduler.add_job(ittech.request_notification, 'date', run_date=scheduled_time,
        #                                   args=[message_id, topic_id, request_text, finishing_time, request.id,
        #                                         request.file_url],
        #                                   id=job_id, replace_existing=True)
        #             except ConflictingIdError:
        #                 print(f"Job '{job_id}' already scheduled or was missed by time. Skipping ...")
        #
        #     else:
        #         await query.answer(text="Вы не можете завершить заявку, вы не являетесь исполнителем этой заявки!\n"
        #                                 f"Исполнитель: {request.brigada_name}", show_alert=True)

        elif callback_data == "user_accept":
            new_keyboard = [
                [InlineKeyboardButton("Подтвердить", callback_data='user_confirm'),
                 InlineKeyboardButton("Отменить", callback_data='user_cancel')]
            ]
            new_reply_markup = InlineKeyboardMarkup(new_keyboard)

            # Edit only the inline buttons (reply markup)
            await query.edit_message_reply_markup(reply_markup=new_reply_markup)

        elif callback_data == "user_confirm":
            status = request.status
            if status == 6:
                request = crud.update_it_request(id=request.id, status=3)
                await query.edit_message_reply_markup(reply_markup=None)
                # await context.bot.edit_message_reply_markup(chat_id=IT_SUPERGROUP, message_id=request.tg_message_id,
                #                                             reply_markup=None)
                message_text = f"Уважаемый {request.user_full_name}, статус вашей заявки #{request.id}s по IT: Закрыт." \
                               f"\n\nПожалуйста нажмите на кнопку Оставить отзыв🌟и  оцените заявку"
                url = f"{FRONT_URL}tg/order-rating/{request.id}?user_id={request.user_id}&department={request.category_department}&sub_id={request.category_sub_id}"
                inlinewebapp(bot_token=BOTTOKEN,
                             chat_id=request.user_telegram_id,
                             message_text=message_text,
                             url=url)
            elif status == 3:
                await query.edit_message_reply_markup(reply_markup=None)
                await query.answer(text="Данная заявка уже закрыта!", show_alert=True)

        elif callback_data == "user_cancel":
            keyboard = [
                [InlineKeyboardButton("Выполнен/Принимаю", callback_data='user_accept'),
                 InlineKeyboardButton("Не выполнен/Не принимаю", callback_data='user_not_accept')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_reply_markup(reply_markup=reply_markup)

        elif callback_data == "user_not_accept":
            status = request.status
            if status == 6:
                topic_id = request.topic_id
                now = datetime.datetime.now(tz=ittech.timezonetash)
                remaining_time = finishing_time - now
                late_time = now - finishing_time
                if finishing_time >= now:
                    text = f"{request_text}\n\n" \
                           f"<b> ‼️ Оставщиеся время:</b>  {str(remaining_time).split('.')[0]}"
                else:
                    text = f"{request_text}\n\n" \
                           f"<b> ‼️ Просрочен на:</b>  {str(late_time).split('.')[0]}"
                keyboard = [
                    [
                        InlineKeyboardButton("Завершить заявку", callback_data='complete_request'),
                        InlineKeyboardButton("Отменить", callback_data='cancel_request')
                    ],
                    [InlineKeyboardButton("Посмотреть фото", url=f"{BASE_URL}{request.file_url}")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                # await context.bot.edit_message_text(chat_id=IT_SUPERGROUP, text=text,
                #                                     message_id=message_id,
                #                                     reply_markup=reply_markup, parse_mode='HTML')
                message = await context.bot.send_message(chat_id=IT_SUPERGROUP, message_thread_id=topic_id, text=text,
                                                         reply_markup=reply_markup, parse_mode='HTML')
                message_id = message.message_id
                request = crud.update_it_request(id=request.id, status=7, message_id=message_id)
                text = f'{request_text}\n\n' \
                       f'Статус вашей заявки:  Возобновлен 🔄'
                await query.edit_message_text(text=text, reply_markup=None)
                text_request = "Спасибо за обратную связь.\n" \
                               "Специалист свяжется с вами для решения вашей заявки.\n" \
                               "Статус вашей заявки: Возобновлен 🔄"
                await context.bot.send_message(chat_id=query.message.chat.id, text=text_request)

                if delta_minutes > 0:
                    delete_job_id = f"delete_message_for_{request.id}"
                    job_scheduler.add_delete_message_job(
                        job_id=delete_job_id,
                        scheduled_time=deleting_scheduled_time,
                        message_id=message_id,
                        topic_id=topic_id
                    )
                    send_job_id = f"send_message_for_{request.id}"
                    job_scheduler.add_send_message_job(
                        job_id=send_job_id,
                        scheduled_time=sending_scheduled_time,
                        topic_id=topic_id,
                        request_text=request_text,
                        finishing_time=finishing_time,
                        request_id=request.id,
                        request_file=request.file_url
                    )

            elif status == 3:
                await query.edit_message_reply_markup(reply_markup=None)
                await query.answer(text="Данная заявка уже закрыта!", show_alert=True)

    else:
        selected_option = int(query.data)
        if one_request.status == 0 and user:
            if selected_option < 0:
                if selected_option == -1:
                    if one_request.category_department == 1:

                        db_query = crud.getlistbrigada(sphere_status=one_request.category_sphere_status,
                                                       department=one_request.category_department)
                    else:
                        db_query = crud.getlistbrigada(department=one_request.category_department, sphere_status=None)
                    reply_murkup = data_transform(db_query)
                    await query.message.edit_text(text=text_of_order, reply_markup=InlineKeyboardMarkup(reply_murkup))
                if selected_option == -2:
                    request_rejected = crud.reject_request(status=4, id=requests_id)
                    await context.bot.send_message(chat_id=request_rejected.user_telegram_id,
                                                   text=f"Ваша заявка по Арс🛠  #{request_rejected.id}s  была отменена по причине: < причина >")
                    await query.message.edit_text(text=text_of_order,
                                                  reply_markup=InlineKeyboardMarkup(blank_reply_murkup))

            # if this value is about more than one it is about it is brigada id
            else:
                request_list = crud.accept_request(id=requests_id, brigada_id=selected_option,
                                                   user_manager=user.full_name)

                await query.message.edit_text(text=f"{text_of_order} \n\nкоманда🚙: {request_list.brigada_name}",
                                              reply_markup=InlineKeyboardMarkup(blank_reply_murkup))
                try:
                    brigada_id = request_list.brigada_id
                    # brigader_telid = crud.get_brigada_id(session,id=brigada_id)
                except:
                    pass
                if request_list.category_department == 1:
                    try:
                        await context.bot.send_message(chat_id=request_list.brigada_telegram_id,
                                                       text=f"{request_list.brigada_name} вам назначена заявка, #{request_list.id}s {request_list.fillial_name}")
                    except:
                        pass
                    try:
                        await context.bot.send_message(chat_id=request_list.user.telegram_id,
                                                       text=f"Уважаемый {request_list.user_full_name}, на вашу заявку #{request_list.id}s назначена команда🚙: {request_list.brigada_name}")
                    except:
                        pass
                else:
                    try:
                        await context.bot.send_message(chat_id=request_list.user.telegram_id,
                                                       message_text=f"Уважаемый {request_list.user.full_name}, статус вашей заявки #{request_list.id}s по Маркетингу: В процессе.")
                    except:
                        pass
        elif one_request.status == 6 and user:
            if selected_option == 10:

                request_list = crud.tg_update_only_status(requestid=requests_id, status=3)

                if request_list.category_department == 1:
                    # send_iiko_document(request_id=requests_id)
                    message_text = f'Уважаемый {request_list.user_full_name}, статус вашей заявки #{request_list.id}s по APC: Завершен.\n\nПожалуйста нажмите на кнопку Оставить отзыв🌟и  оцените заявку'
                elif request_list.category_department == 4:
                    message_text = f"Уважаемый {request_list.user_full_name}, статус вашей заявки #{request_list.id}s по IT: Завершен.\n\nПожалуйста нажмите на кнопку Оставить отзыв🌟и  оцените заявку"
                elif request_list.category_department == 2:
                    # send_iiko_document(request_id=requests_id)
                    message_text = f"Уважаемый {request_list.user_full_name}, статус вашей заявки #{request_list.id}s по инвентарь: Завершен.\n\nПожалуйста нажмите на кнопку Оставить отзыв🌟и  оцените заявку"
                else:
                    message_text = f"Уважаемый {request_list.user_full_name}, статус вашей заявки #{request_list.id}s Завершен.\n\nПожалуйста нажмите на кнопку Оставить отзыв🌟и  оцените заявку"
                url = f"{FRONT_URL}tg/order-rating/{request_list.id}?user_id={request_list.user_id}&department={request_list.category_department}&sub_id={request_list.category_sub_id}"
                # await context.bot.send_message(chat_id=request_list.user_telegram_id,text=message_text,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Оставить отзыв🌟',url=url)]]),parse_mode= ParseMode.MARKDOWN)

                await query.message.edit_text(text=text_of_order, reply_markup=InlineKeyboardMarkup(blank_reply_murkup))
                inlinewebapp(bot_token=BOTTOKEN,
                             chat_id=request_list.user_telegram_id,
                             message_text=message_text,
                             url=url)

            elif selected_option == 11:
                request_list = crud.tg_update_requst_st(requestid=requests_id, status=7)
                await query.message.edit_text(text=text_of_order, reply_markup=InlineKeyboardMarkup(blank_reply_murkup))

                text_request = "Спасибо что обратную связь. Специалист по  свяжется с вами для решения вашей заявки. Статус вашей заявки: В процессе"
                try:
                    await context.bot.send_message(chat_id=request_list.user_telegram_id, text=text_request)
                except:
                    pass
            else:
                await query.message.edit_text(text=text_of_order, reply_markup=InlineKeyboardMarkup(blank_reply_murkup))

        elif one_request.status is None and user:
            if selected_option == 100:
                crud.tg_update_only_status(requestid=one_request.id, status=0)
                crud.update_expenditures(request_id=one_request.id)
                text_of_order += '\n\nОдобрено✅'

            elif selected_option == 101:
                text_of_order += '\n\nОтклонено🚫'

            await query.edit_message_text(text=text_of_order, reply_markup=None)
            await context.bot.send_message(
                chat_id=one_request.user_telegram_id,
                text=text_of_order
            )

        else:
            await query.message.edit_text(text=text_of_order, reply_markup=InlineKeyboardMarkup(blank_reply_murkup))

    return -1


async def reply_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    reply_text = message.text
    original_message = message.reply_to_message.text
    # response = f"You replied to: '{original_message}' with '{reply_text}'"
    # request_id = context.user_data['request_id']
    request_id = re.findall(r'\d+', original_message)[0]
    request = crud.get_request_id(id=request_id)
    user = crud.get_user_tel_id(id=message.from_user.id)
    deny_reason = reply_text
    if request.status == 1 or request.status == 7:
        if user.brigada_id == request.brigada_id:
            # formatted_created_time = request.created_at.strftime("%d.%m.%Y %H:%M")
            # formatted_finishing_time = request.finishing_time.strftime("%d.%m.%Y %H:%M") if request.finishing_time is not None else None
            # request_text = f"📑Заявка #{request.id}s\n\n" \
            #                f"📍Филиал: {request.parentfillial_name}\n" \
            #                f"👨‍💼Сотрудник: {request.user_full_name}\n" \
            #                f"📱Номер телефона сотрудника: +{request.user_phone_number}\n" \
            #                f"📱Номер телефона для заявки: {request.phone_number}\n" \
            #                f"🔰Категория проблемы: {request.category_name}\n" \
            #                f"🕘Дата поступления заявки: {formatted_created_time}\n" \
            #                f"🕘Дата дедлайна заявки: {formatted_finishing_time}\n" \
            #                f"❗️SLA: {request.sla} часов\n" \
            #                f"💬Комментарии: {request.description}"

            await message.reply_to_message.delete()
            request = crud.update_it_request(id=request.id, status=4, deny_reason=deny_reason)
            delete_job_id = f"delete_message_for_{request.id}"
            job_scheduler.remove_job(job_id=delete_job_id)

            send_job_id = f"send_message_for_{request.id}"
            job_scheduler.remove_job(job_id=send_job_id)

            # text = f"{request_text}\n\n" \
            #        f"<b>Заявка отменена 🚫</b>\n" \
            #        f"Причина отмены: {deny_reason}"
            # await update.edit_message_text(text=text, reply_markup=None, parse_mode='HTML')
            # await message.reply_to_message.edit_text(text=text, reply_markup=None, parse_mode='HTML')

            message_text = f"❌Ваша заявка #{request.id}s по IT👨🏻‍💻 отменена по причине: {request.deny_reason}\n\n" \
                           f"Если Вы с этим не согласны, поставьте, пожалуйста, " \
                           f"рейтинг нашему решению по Вашей заявке от 1 до 5, и напишите свои комментарий."

            url = f"{FRONT_URL}tg/order-rating/{request.id}?user_id={request.user_id}&department={request.category_department}&sub_id={request.category_sub_id}"
            inlinewebapp(
                bot_token=BOTTOKEN,
                chat_id=request.user_telegram_id,
                message_text=message_text,
                url=url
            )
        else:
            await update.message.reply_text(text=f"Вы не можете отменить заявку #{request.id}s, вы не являетесь исполнителем этой заявки!\n"
                                                 f"Исполнитель: {request.brigada_name}")
    else:
        await update.message.reply_text(f"Заявка #{request.id}s не была ещё принята или уже отменена/завершена !")


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    persistence = PicklePersistence(filepath="conversationbot")
    application = Application.builder().token(BOTTOKEN).persistence(persistence).build()
    application.add_handler(CallbackQueryHandler(handle_callback_query)) # pattern=r'^(?!deny_reason=other$).+'
    # application.add_handler(MessageHandler(filters.REPLY, reply_message_handler))
    # add states phone fullname category desction and others
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            PHONE: [MessageHandler(filters.CONTACT, phone)],
            FULLNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, fullname)],
            MANU: [MessageHandler(filters.TEXT & ~filters.COMMAND, manu)],
            CATEGORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, category)],
            DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, description)],
            PRODUCT: [MessageHandler(filters.TEXT & ~filters.COMMAND, product)],
            FILES: [MessageHandler(filters.ALL,files)],
            # FILES: [MessageHandler(
            #     filters.PHOTO | filters.Document.DOCX | filters.Document.IMAGE | filters.Document.PDF | filters.TEXT | filters.Document.MimeType(
            #         'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')  | filters.Document.MimeType('zz-application/zz-winassoc-psd') & ~filters.COMMAND, files)],
            BRIG_MANU: [MessageHandler(filters.TEXT & ~filters.COMMAND, brig_manu)],
            BRANCHES: [MessageHandler(filters.TEXT & ~filters.COMMAND, branches)],
            TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, types)],
            ORDERSTG: [MessageHandler(filters.TEXT & ~filters.COMMAND, orderstg)],
            LOCATION_BRANCH: [MessageHandler(filters.TEXT & ~filters.COMMAND, location_branch)],
            FINISHING: [MessageHandler(filters.TEXT & ~filters.COMMAND, finishing)],
            CLOSEBUTTON: [MessageHandler(filters.StatusUpdate.WEB_APP_DATA & ~filters.COMMAND, closebutton)],
            MARKETINGCAT: [MessageHandler(filters.TEXT & ~filters.COMMAND, marketingcat)],
            MARKETINGSTBUTTON: [MessageHandler(filters.TEXT & ~filters.COMMAND, marketingstbutton)],
            SPHERE: [MessageHandler(filters.TEXT & ~filters.COMMAND, sphere)],
            CHANGESPHERE: [MessageHandler(filters.TEXT & ~filters.COMMAND, changesphere)],
            CHOSENSPHERE: [MessageHandler(filters.TEXT & ~filters.COMMAND, chosensphere)],
            ADDCOMMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, addcomment)],
            # CHOOSEMONTH:[MessageHandler(filters.TEXT& ~filters.COMMAND,cars.choose_month)],
            # CHOOSEDAY:[MessageHandler(filters.TEXT& ~filters.COMMAND,cars.choose_day)],
            # CHOOSEHOUR:[MessageHandler(filters.TEXT& ~filters.COMMAND,cars.choose_current_hour)],
            CHOOSESIZE: [MessageHandler(filters.TEXT & ~filters.COMMAND, cars.choose_size)],
            INPUTIMAGECAR: [MessageHandler(
                filters.PHOTO | filters.Document.DOCX | filters.Document.IMAGE | filters.Document.PDF | filters.TEXT | filters.Document.MimeType(
                    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet') & ~filters.COMMAND,
                cars.input_image_car)],
            COMMENTCAR: [MessageHandler(filters.TEXT & ~filters.COMMAND, cars.comment_car)],
            MEALSIZE: [MessageHandler(filters.TEXT & ~filters.COMMAND, food.meal_size)],
            MEALBREADSIZE: [MessageHandler(filters.TEXT & ~filters.COMMAND, food.meal_bread_size)],
            CARSP: [MessageHandler(filters.TEXT, cars.car_sphere)],
            CARSFROMLOC: [MessageHandler(filters.TEXT | filters.LOCATION, cars.cars_from_loc)],
            CARSTOLOC: [MessageHandler(filters.TEXT | filters.LOCATION, cars.cars_to_loc)],
            ITSPHERE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ittech.it_sphere)],
            ITCATEGORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, ittech.it_category)],
            ITPRODUCTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, ittech.it_products)],
            ITAMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, ittech.it_amount)],
            ITCOMMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, ittech.it_comment)],
            ITFILES: [MessageHandler(
                filters.PHOTO | filters.Document.DOCX | filters.Document.IMAGE | filters.Document.PDF | filters.TEXT | filters.Document.MimeType(
                    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet') & ~filters.COMMAND,
                ittech.it_files)],
            ITFINISHING: [MessageHandler(filters.TEXT & ~filters.COMMAND, ittech.it_finishing)],
            COMMENTNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, comments.commentname)],
            COMMENTTEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, comments.commenttext)],
            COMMENTPHOTO: [MessageHandler(
                filters.PHOTO | filters.Document.DOCX | filters.Document.IMAGE | filters.Document.PDF | filters.TEXT | filters.Document.MimeType(
                    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet') & ~filters.COMMAND,
                comments.commentphoto)],
            INVETORY: [MessageHandler(filters.StatusUpdate.WEB_APP_DATA & ~filters.COMMAND, inventory.close_invetory)],
            VIDCOMMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, video.vidcomment)],
            VIDFILES: [MessageHandler(
                filters.PHOTO | filters.Document.DOCX | filters.Document.IMAGE | filters.Document.PDF | filters.TEXT | filters.Document.MimeType(
                    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet') & ~filters.COMMAND,
                video.vidfiles)],
            VIDFROM: [MessageHandler(filters.TEXT & ~filters.COMMAND, video.vidfrom)],
            VIDTO: [MessageHandler(filters.TEXT & ~filters.COMMAND, video.vidto)],
            ITPHOTOREPORT: [MessageHandler(
                filters.PHOTO | filters.Document.DOCX | filters.Document.IMAGE | filters.Document.PDF | filters.TEXT | filters.Document.MimeType(
                    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet') & ~filters.COMMAND,
                it_photo_report)],
            UNIFORMNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, uniforms.uniformname)],
            UNIFORMSIZE: [MessageHandler(filters.TEXT & ~filters.COMMAND, uniforms.uniformsize)],
            UNIFORMAMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, uniforms.uniformamount)],
            UNIFORMVERIFY: [MessageHandler(filters.TEXT & ~filters.COMMAND, uniforms.uniformverify)],
            UNIFORMCATEGORIES: [MessageHandler(filters.TEXT & ~filters.COMMAND, uniforms.uniformcategories)],
            VERIFYUSER: [MessageHandler(filters.TEXT & ~filters.COMMAND, verify_user)],
            ITPHONENUMBER: [MessageHandler(filters.TEXT & ~filters.COMMAND, ittech.itphonenumber)],
            PHONENUMBER: [MessageHandler(filters.TEXT & ~filters.COMMAND, phonenumber)],
            INPUTCOMMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, ratings.input_rating)],
            ARCFACTORYMANAGER : [MessageHandler(filters.TEXT & ~filters.COMMAND,arc_factory.arc_factory_managers)],
            ARCFACTORYDIVISIONS: [MessageHandler(filters.TEXT & ~filters.COMMAND,arc_factory.arc_factory_divisions)],
            COINAMOUNT:[MessageHandler(filters.TEXT & ~filters.COMMAND, coins.coin_amount)],
            COINDESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, coins.coin_description)],
            OFFICIAL_EMPLOYMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, official_employment)]

            # CALLBACK_STATE: [CallbackQueryHandler(handle_callback_query)],  # pattern=r'^deny_reason=other$'
            # DENY_REASON: [
            #     # [CallbackQueryHandler(deny_reason_handle_callback_query, filters.Regex(r'^deny_reason=other$'))],
            #     MessageHandler(filters.TEXT & ~filters.COMMAND, ittech.it_deny_reason)
            # ]

            # IT_PASSWORD:[MessageHandler(filters.TEXT& ~filters.COMMAND,it_password)],
        },
        fallbacks=[CommandHandler("cancel", cancel),
                   CommandHandler('check', check),
                   CommandHandler('start', start)],
        allow_reentry=True,
        name="my_conversation",
        persistent=True,
        per_chat=True
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()

