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


async def vidcomment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    entered_data = update.message.text
    reply_keyboard = [['⬅️ Назад']]
    if entered_data == '⬅️ Назад':
        context.user_data['page_number'] =0
        request_db = crud.get_branch_list(db=bot.session,sphere_status=1)
        reply_keyboard = bot.transform_list(request_db,2,'name')
        reply_keyboard.insert(0,['⬅️ Назад'])
        reply_keyboard.append(['<<<Предыдущий','Следующий>>>'])
        await update.message.reply_text(f"Выберите филиал или отдел:",reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
        return bot.BRANCHES
    context.user_data['comment'] = entered_data
    await update.message.reply_text(f"Введите дату и время начала события пример: 01.01.2024  7:00",reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
    return bot.VIDFROM



async def vidfrom(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    entered_data = update.message.text
    reply_keyboard = [['⬅️ Назад']]
    if entered_data == '⬅️ Назад':
        await update.message.reply_text('Опишите пожалуйста событие в деталях',reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
        return bot.VIDCOMMENT
    context.user_data['vidfrom'] = entered_data
    await update.message.reply_text(f"Введите дату и время конца события пример: 01.01.2024  10:00",reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
    return bot.VIDTO


async def vidto(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    entered_data = update.message.text
    reply_keyboard = [['⬅️ Назад']]
    if entered_data == '⬅️ Назад':
        await update.message.reply_text("Введите дату и время начала события пример: 01.01.2024  7:00",reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
        return bot.VIDFROM
    context.user_data['vidto'] = entered_data
    reply_keyboard.append(['Пропустить'])
    await update.message.reply_text(f"При желании отправьте фото",reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
    #await update.message.reply_text(f"Manu",reply_markup=ReplyKeyboardMarkup(bot.manu_buttons,resize_keyboard=True))
    #fillial_query = crud.getchildbranch(db=bot.session,fillial=context.user_data['branch'],type=int(context.user_data['type']),factory=int(context.user_data['sphere_status']))
    #user_query = crud.get_user_tel_id(db=bot.session,id=update.message.from_user.id)
    #data = crud.add_video_request(db=bot.session,category_id=,fillial_id=fillial_query.id,user_id=user_query.id,comment=context.user_data['comment'],vidfrom=context.user_data['vidfrom'],vidto=context.user_data['vidto'])
    return bot.VIDFILES

async def vidfiles(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [['⬅️ Назад']]
    if update.message.text:
        entered_data = update.message.text

        if entered_data == '⬅️ Назад':
            await update.message.reply_text('Введите дату и время начала события пример: 01.01.2024  7:00',reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
            return bot.VIDFROM
        else:
            photo_vid = None
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
        photo_vid = f"{bot.backend_location}files/{file_name}"
        with open(photo_vid,'wb+') as f:
            f.write(file_content)
            f.close()
        context.user_data['image_car']='files/'+file_name
        photo_vid = f"files/{file_name}"

        
    
    
    
    await update.message.reply_text(f"Manu",reply_markup=ReplyKeyboardMarkup(bot.manu_buttons,resize_keyboard=True))
    fillial_query = crud.getchildbranch(db=bot.session,fillial=context.user_data['branch'],type=int(context.user_data['type']),factory=int(context.user_data['sphere_status']))
    user_query = crud.get_user_tel_id(db=bot.session,id=update.message.from_user.id)
    data = crud.add_video_request(db=bot.session,category_id=60,fillial_id=fillial_query.id,user_id=user_query.id,comment=context.user_data['comment'],vidfrom=context.user_data['vidfrom'],vidto=context.user_data['vidto'])
    if photo_vid is not None:
        add_files = crud.create_files(db=bot.session,request_id=data.id,filename=photo_vid)
    formatted_datetime_str = data.created_at.strftime("%d.%m.%Y %H:%M")
    keyboard_button = []
    if photo_vid is not None:
        keyboard_button = [{'text':'Посмотреть фото/видео',"url":f"{bot.BASE_URL}{photo_vid}"}]
    bot.sendtotelegramviewimage(bot_token=bot.BOTTOKEN,chat_id='-1002124172379',message_text="📑Заявка № "+str(data.id)+"\n\n📍Филиал: "+str(data.fillial.parentfillial.name)+"\n\nИмя: "+str(user_query.full_name)+"\nНомер: "+user_query.phone_number+"\nТелеграм: "+f"https://t.me/{update.message.from_user.username}"+"\n🕘Дата поступления заявки: "+str(formatted_datetime_str)+"\n\n🏳️Дата и время начало события: "+data.update_time['vidfrom']+"\n🏁Дата и время конца события: "+data.update_time['vidto']+"\n\n💬Комментарии: "+str(data.description),buttons=keyboard_button)
    await update.message.reply_text(f"Спасибо, ваша заявка #{data.id}s по Видеонаблюдение принята. Как ваша заявка будет назначена в работу ,вы получите уведомление.",reply_markup=ReplyKeyboardMarkup(bot.manu_buttons,resize_keyboard=True))
    #await update.message.reply_text(f"Главное меню",reply_markup=ReplyKeyboardMarkup(manu_buttons,resize_keyboard=True))
    return bot.MANU