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



async def commenttext(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    entered_data = update.message.text
    reply_keyboard = [['⬅️ Назад']]
    if entered_data == '⬅️ Назад':
        context.user_data['page_number'] =0
        request_db = crud.get_branch_list(db=bot.session,sphere_status=1)
        reply_keyboard = transform_list(request_db,2,'name')
        reply_keyboard.insert(0,['⬅️ Назад'])
        reply_keyboard.append(['<<<Предыдущий','Следующий>>>'])
        await update.message.reply_text(f"Выберите филиал или отдел:",reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
        return bot.BRANCHES
    await  update.message.reply_text('Пожалуйста укажите номер и имя гостя',reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
    context.user_data['comment_text'] = entered_data
    return bot.COMMENTNAME

    
async def commentname(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    entered_data = update.message.text
    reply_keyboard = [['⬅️ Назад']]
    if entered_data == '⬅️ Назад':
        await update.message.reply_text('Пожалуйста укажите номер и имя гостя',reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
        return bot.COMMENTTEXT
    reply_keyboard = [['⬅️ Назад']]
    context.user_data['comment_name'] = entered_data
    await  update.message.reply_text('Пожалуйста отправьте фото из Книги жалоб',reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
    return bot.COMMENTPHOTO

async def commentphoto(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text:
        entered_data = update.message.text
        reply_keyboard = [['⬅️ Назад']]
        if entered_data == '⬅️ Назад':
            await update.message.reply_text('Пожалуйста укажите номер и имя гостя',reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
            return bot.COMMENTTEXT
        else:
            await update.message.reply_text('Пожалуйста отправьте фото из Книги жалоб',reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
            return bot.COMMENTPHOTO
    else:
        
        if update.message.document:
           #context.user_data['file_url']=f"files/{update.message.document.file_name}"
            file_id = update.message.document.file_id
            file_name = update.message.document.file_name
            new_file = await context.bot.get_file(file_id=file_id)
            file_content = await new_file.download_as_bytearray()
            context.user_data['image_comment']='files/'+file_name
            #files_open = {'files':file_content}
        if update.message.photo:
            file_name = f"{update.message.photo[-1].file_id}.jpg"
            getFile = await context.bot.getFile(update.message.photo[-1].file_id)
            file_content = await getFile.download_as_bytearray()
            context.user_data['image_comment']='files/'+file_name
            #files_open = {'files':file_content}
        with open(f"{bot.backend_location}files/{file_name}",'wb+') as f:
            f.write(file_content)
            f.close()

    fillial_query = crud.getchildbranch(fillial=context.user_data['branch'],type=int(context.user_data['type']),factory=int(context.user_data['sphere_status'])).id
    category_id = 56
    user_query = crud.get_user_tel_id(id=update.message.from_user.id)
    data = crud.add_comment_request(category_id=category_id,fillial_id=fillial_query,user_id=user_query.id,comment=context.user_data['comment_text'],name=context.user_data['comment_name'])
    if context.user_data['image_comment'] is not None:
        crud.create_files(request_id=data.id,filename=context.user_data['image_comment'])
    await update.message.reply_text('Спасибо ваш отзыв принят✍',reply_markup=ReplyKeyboardMarkup(bot.manu_buttons,resize_keyboard=True))
    return bot.MANU
    