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
import pytz

time_zone = pytz.timezone('Asia/Tashkent')


async def input_rating(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message:
        entered_data = update.message.text
        if entered_data == '⬅️ Назад':
            await update.message.reply_text(f"Главное меню",
                                            reply_markup=ReplyKeyboardMarkup(bot.manu_buttons, resize_keyboard=True))
            return bot.MANU
        else:
            get_user_id = crud.get_user_tel_id(id=update.message.from_user.id)

            rating_created= crud.add_general_comment(user_id=get_user_id.id,comment=entered_data)

            await update.message.reply_text(f"Главное меню",
                                            reply_markup=ReplyKeyboardMarkup(bot.manu_buttons, resize_keyboard=True))
            #send message to another group by chat id
            current_formatted_date =  datetime.datetime.now(time_zone).strftime("%d.%m.%Y %H:%M")
            text_to_send = f"💬 Новый отзыв #{rating_created.id}s\nАвтор: {get_user_id.full_name}\nНомер: +{get_user_id.phone_number}\nОтзыв: {entered_data}\nДата: {current_formatted_date}\n\n✍️Комментарии:  {entered_data}"

            await context.bot.send_message(chat_id='-1002223465896', text=text_to_send)
            return bot.MANU

    else:
        # send message like please input text in russian
        await update.message.reply_text("Пожалуйста введите текст",reply_markup=ReplyKeyboardMarkup([['⬅️ Назад']],resize_keyboard=True))
        return bot.INPUTCOMMENT
