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
import json
import pytz 
from datetime import datetime,timedelta

async def close_invetory(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    data = json.loads(update.effective_message.web_app_data.data)
    await update.message.reply_text(f"Спасибо, ваша заявка по Inventary принята. Как ваша заявка будет назначена в работу, вы получите уведомление",reply_markup=ReplyKeyboardMarkup(keyboard=bot.manu_buttons,resize_keyboard=True))
    return bot.MANU
