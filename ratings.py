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



async def input_rating(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message:
        entered_data = update.message.text
        if entered_data == '⬅️ Назад':
            await update.message.reply_text(f"Главное меню",
                                            reply_markup=ReplyKeyboardMarkup(bot.manu_buttons, resize_keyboard=True))
            return bot.MANU
        else:
            crud.add_general_comment(user_id=context.user_data['user_id'],comment=entered_data)
            await update.message.reply_text(f"Главное меню",
                                            reply_markup=ReplyKeyboardMarkup(bot.manu_buttons, resize_keyboard=True))
            return bot.MANU

    else:
        # send message like please input text in russian
        await update.message.reply_text("Пожалуйста введите текст",reply_markup=ReplyKeyboardMarkup([['⬅️ Назад']],resize_keyboard=True))
        return bot.INPUTCOMMENT
