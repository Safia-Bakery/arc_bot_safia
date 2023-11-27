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
from microser import transform_list

import datetime
import calendar
month_list = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]

month_button = [[ "January", "February", "March", ],
                ["April","May", "June"],
                ["July", "August","September"],
                ["October", "November", "December"],['⬅️ Назад']]
"""
async def choose_month(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chosen_data = update.message.text
    if chosen_data=='⬅️ Назад':
            if context.user_data['type']==5:
                sphere_status =None
            else:
                sphere_status=context.user_data['sphere_status']
            request_db =  crud.get_category_list(db=bot.session,sphere_status=sphere_status,department=int(context.user_data['type']))
            reply_keyboard = bot.transform_list(request_db,3,'name')

            reply_keyboard.append(['⬅️ Назад'])
            await update.message.reply_text(f"Пожалуйста выберите категорию:",reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))

            return bot.CATEGORY
    if chosen_data in month_list:
        month_index = month_list.index(chosen_data)+1

        
        current_date = datetime.date.today()
        current_month = current_date.month
        context.user_data['choose_month'] = month_index
        num  = calendar.monthrange(2023,month_index)[1]
        context.user_data['month_length'] = num

        if current_month ==month_index:

            date_list = [list(map(str, range(start, min(start + 3, num + 1)))) for start in range(current_date.day, num + 1, 3)]
            date_list.append(['⬅️ Назад'])
        else:
            date_list = [list(map(str, range(start, min(start + 3, num + 1)))) for start in range(1, num + 1, 3)]
            date_list.append(['⬅️ Назад'])
        await update.message.reply_text('Пожалуйста выберите день, когда вам нужна машина',reply_markup=ReplyKeyboardMarkup(date_list,resize_keyboard=True))

        return bot.CHOOSEDAY

async def choose_day(update:Update,context:ContextTypes.DEFAULT_TYPE) ->int:
    chosen_day = update.message.text
    current_date = datetime.date.today()
    if chosen_day=='⬅️ Назад':
        current_month = current_date.month-1
        next_month = current_date.replace(day=1) + datetime.timedelta(days=32)
        next_month = next_month.replace(day=1).month-1
        months_buttons = [[month_list[current_month],month_list[next_month]],['⬅️ Назад']]
        await update.message.reply_text('Укажите в какое время вам нужна машина',reply_markup=ReplyKeyboardMarkup(months_buttons,resize_keyboard=True))
        return bot.CHOOSEMONTH
    
    if int(chosen_day) <=context.user_data['choose_month']:
        context.user_data['choose_day']= chosen_day
        if int(chosen_day)==int(current_date.day):
            time_hour = datetime.datetime.now().hour
            num = 24
            date_list = date_list = [list(map(lambda x: f"{x:02d}:00", range(start, min(start + 3, num + 1)))) for start in range(time_hour, num + 1, 3)]
        else:
            time_hour = 1
            num=24
            date_list = date_list = [list(map(lambda x: f"{x:02d}:00", range(start, min(start + 3, num + 1)))) for start in range(time_hour, num + 1, 3)]
        date_list.append(['⬅️ Назад'])
        await update.message.reply_text('Пожалуйста выберите время',reply_markup=ReplyKeyboardMarkup(date_list,resize_keyboard=True))
        return bot.CHOOSEHOUR
    


async def choose_current_hour(update:Update,context:ContextTypes.DEFAULT_TYPE) ->int:
    chosen_data = update.message.text
    if chosen_data=='⬅️ Назад':
        current_date = datetime.date.today()
        current_month = current_date.month
        num= context.user_data['month_length']
        month_index = context.user_data['choose_month']
        if current_month ==month_index:

            date_list = [list(map(str, range(start, min(start + 3, num + 1)))) for start in range(current_date.day, num + 1, 3)]
            date_list.append(['⬅️ Назад'])
        else:
            date_list = [list(map(str, range(start, min(start + 3, num + 1)))) for start in range(1, num + 1, 3)]
            date_list.append(['⬅️ Назад'])
        await update.message.reply_text('Укажите в какое время вам нужна машина',reply_markup=ReplyKeyboardMarkup(date_list,resize_keyboard=True))

        return bot.CHOOSEDAY
    context.user_data['choose_hour']=chosen_data
    await update.message.reply_text("Укажите вес/размер",reply_markup=ReplyKeyboardMarkup([['⬅️ Назад']],resize_keyboard=True))
    return bot.CHOOSESIZE

"""

async def car_sphere(update:Update,context:ContextTypes.DEFAULT_TYPE) ->int:
    chosen_data = update.message.text
    if chosen_data=='⬅️ Назад':
        if int(context.user_data['sphere_status'])==2:
            reply_keyboard = [['Арс🛠',"IT🧑‍💻"],['Инвентарь📦','Запрос машины🚛'],['⬅️ Назад']]
            await update.message.reply_text(f"Этот пункт в разработке",reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
        elif int(context.user_data['sphere_status'])==1:
            reply_keyboard = [['Арс🛠',"IT🧑‍💻"],['Маркетинг📈','Инвентарь📦'],['Запрос машины🚛','Заказать еду🥘'],['⬅️ Назад']]
            await update.message.reply_text(f"Этот пункт в разработке",reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
        return bot.TYPE
    if chosen_data== 'Запросить на филиал':
        context.user_data['carssp'] = 'Запросить на филиал'
        context.user_data
        if context.user_data['sphere_status']==1:
            request_db = crud.get_branch_list(db=bot.session,sphere_status=1)
            #request_db = requests.get(f"{BASE_URL}fillials/list/tg").json()
        else:
            request_db = crud.getfillialchildfabrica(db=bot.session,offset=0)
            #request_db = requests.get(f"{BASE_URL}get/fillial/fabrica/tg").json()
 
        reply_keyboard = transform_list(request_db,2,'name')

        reply_keyboard.insert(0,['⬅️ Назад'])
        reply_keyboard.append(['<<<Предыдущий','Следующий>>>'])
        await update.message.reply_text(f"Выберите филиал или отдел:",reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
        return bot.BRANCHES
    if chosen_data == 'С адреса на адрес':
        await update.message.reply_text('Пожалуйста отправьте геолокацию или введите текстом куда нужно отвезти',reply_markup=ReplyKeyboardMarkup([['⬅️ Назад']],resize_keyboard=True))
        context.user_data['carssp'] = 'С адреса на адрес'
        return bot.CARSFROMLOC

    else:

        order_car = [['Запросить на филиал','С адреса на адрес'],['⬅️ Назад']]
        await update.message.reply_text('Тип',reply_markup=ReplyKeyboardMarkup(order_car,resize_keyboard=True))
        return bot.CARSP

async def cars_from_loc(update:Update,context:ContextTypes.DEFAULT_TYPE) ->int:
    chosen_data  = update.message.text
    if chosen_data=='⬅️ Назад':
        order_car = [['Запросить на филиал','С адреса на адрес'],['⬅️ Назад']]
        await update.message.reply_text('Тип',reply_markup=ReplyKeyboardMarkup(order_car,resize_keyboard=True))
        return bot.CARSP
    if update.message.location:

        user_location = update.message.location
        latitude = user_location.latitude
        longitude = user_location.longitude

        # Generate a Google Maps URL
        map_url = f"https://www.google.com/maps?q={latitude},{longitude}"
    else:
        map_url = update.message.text
    context.user_data['cars_from_loc'] = map_url
    await update.message.reply_text('Пожалуйста отправьте геолокацию или введите текстом куда нужно отвезти',reply_markup=ReplyKeyboardMarkup([['⬅️ Назад']],resize_keyboard=True))
    return bot.CARSTOLOC


async def cars_to_loc(update:Update,context:ContextTypes.DEFAULT_TYPE) ->int:
    chosen_data  = update.message.text
    if chosen_data=='⬅️ Назад':
        await update.message.reply_text('Пожалуйста отправьте геолокацию или введите текстом куда нужно отвезти')
        context.user_data['carssp'] = 'С адреса на адрес'
        return bot.CARSFROMLOC
    if update.message.location:

        user_location = update.message.location
        latitude = user_location.latitude
        longitude = user_location.longitude

        # Generate a Google Maps URL
        map_url = f"https://www.google.com/maps?q={latitude},{longitude}"
    if update.message.text:
        map_url = update.message.text
    context.user_data['cars_to_loc'] = map_url
    await update.message.reply_text("Укажите вес/размер",reply_markup=ReplyKeyboardMarkup([['⬅️ Назад']],resize_keyboard=True))
    return bot.CHOOSESIZE


async def choose_size(update:Update,context:ContextTypes.DEFAULT_TYPE) ->int:
    chosen_data = update.message.text
    if chosen_data=='⬅️ Назад':

        #chosen_day = context.user_data['choose_day']
        #current_date = datetime.date.today()
        #if int(chosen_day)==int(current_date.day):
        #    time_hour = datetime.datetime.now().hour
        #    num = 24
        #    date_list =date_list = [list(map(lambda x: f"{x:02d}:00", range(start, min(start + 3, num + 1)))) for start in range(time_hour, num + 1, 3)]
        #else:
        #    num=24
        #    date_list = date_list = [list(map(lambda x: f"{x:02d}:00", range(start, min(start + 3, num + 1)))) for start in range(time_hour, num + 1, 3)]
        #date_list.append(['⬅️ Назад'])
        #await update.message.reply_text('Пожалуйста выберите время',reply_markup=ReplyKeyboardMarkup(date_list,resize_keyboard=True))
        #return bot.CHOOSEHOUR
        if context.user_data['type']==5:
                sphere_status =None
        else:
            sphere_status=context.user_data['sphere_status']
        if context.user_data['carssp'] =='Запросить на филиал':
            request_db =  crud.get_category_list(db=bot.session,sphere_status=sphere_status,department=int(context.user_data['type']))
            reply_keyboard = bot.transform_list(request_db,3,'name')
            reply_keyboard.append(['⬅️ Назад'])
            await update.message.reply_text(f"Пожалуйста выберите категорию:",reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
            return bot.CATEGORY
        else:
            await update.message.reply_text('Пожалуйста отправьте геолокацию или введите текстом куда нужно отвезти',reply_markup=ReplyKeyboardMarkup([['⬅️ Назад']],resize_keyboard=True))
            return bot.CARSTOLOC
    try:
        int(chosen_data)
    except:
        await update.message.reply_text("Укажите вес/размер",reply_markup=ReplyKeyboardMarkup([['⬅️ Назад']],resize_keyboard=True))
        return bot.CHOOSESIZE
    context.user_data["size_delivery"]=chosen_data
    await update.message.reply_text('Пожалуйста отправьте фото',reply_markup=ReplyKeyboardMarkup([['⬅️ Назад']],resize_keyboard=True))
    return bot.INPUTIMAGECAR



async def input_image_car(update:Update,context:ContextTypes.DEFAULT_TYPE) ->int:
    entered_dat = update.message.text
    if update.message.text:
        if entered_dat=='⬅️ Назад':
            await update.message.reply_text("Укажите вес/размер",reply_markup=ReplyKeyboardMarkup([['⬅️ Назад']],resize_keyboard=True))
            return bot.CHOOSESIZE
        else:
            await update.message.reply_text('Пожалуйста отправьте фото',reply_markup=ReplyKeyboardMarkup([['⬅️ Назад']],resize_keyboard=True))
            return bot.INPUTIMAGECAR
        

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
        with open(f"files/{file_name}",'wb+') as f:
            f.write(file_content)
            f.close()
        context.user_data['image_car']='files/'+file_name
        reply_keyboard = [['⬅️ Назад']]
        await update.message.reply_text('При желании добавьте комментарии',reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True))
        return bot.COMMENTCAR

async def comment_car(update:Update,context:ContextTypes.DEFAULT_TYPE) ->int:
    entered_data = update.message.text
    if entered_data =='⬅️ Назад':
        await update.message.reply_text('Пожалуйста отправьте фото',reply_markup=ReplyKeyboardMarkup([['⬅️ Назад']],resize_keyboard=True))
        return bot.INPUTIMAGECAR
    today_date = datetime.date.today()
    #if context.user_data['choose_month']==1 and today_date.month==12:
    #    year_chosen = int(today_date.year)+1
    #else:
    #    year_chosen=today_date.year
    #hour_part = str(context.user_data['choose_hour']).split(':')[0]
    #arrival_date = datetime.datetime(year=int(year_chosen),
    #                  month=int(context.user_data['choose_month']),
    #                  day=int(context.user_data['choose_day']),
    #                  hour=int(hour_part),
    #                  minute=0
    #                  )
    if context.user_data['carssp'] =='Запросить на филиал':
        category_query = crud.getcategoryname(db=bot.session,name=context.user_data['category']).id
        fillial_query = crud.getchildbranch(db=bot.session,fillial=context.user_data['branch'],type=int(context.user_data['type']),factory=int(context.user_data['sphere_status'])).id
        location = None
    else:
        category_query = None
        fillial_query = None
        location = {'from_loc':context.user_data['cars_from_loc'],'to_loc':context.user_data['cars_to_loc']}

    context.user_data['car_comment'] = entered_data
    
    user_query = crud.get_user_tel_id(db=bot.session,id=update.message.from_user.id)
    data = crud.add_car_request(db=bot.session,category_id=category_query,fillial_id=fillial_query,user_id=user_query.id,size=context.user_data["size_delivery"],time_delivery=None,comment=entered_data,location=location)
    if context.user_data['image_car'] is not None:
        crud.create_files(db=bot.session,request_id=data.id,filename=context.user_data['image_car'])
    await update.message.reply_text(f"Спасибо, ваша заявка #{data.id}s по Запрос машины принята. Как ваша заявка будет назначена в работу ,вы получите уведомление.",reply_markup=ReplyKeyboardMarkup(bot.manu_buttons,resize_keyboard=True))
    #await update.message.reply_text(f"Главное меню",reply_markup=ReplyKeyboardMarkup(manu_buttons,resize_keyboard=True))
    return bot.MANU