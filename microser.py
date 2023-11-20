
from database import session
from datetime import datetime,timedelta
from typing import Union, Any
from jose import jwt
import requests
import os
import pytz
from dotenv import load_dotenv
load_dotenv()
timezonetash = pytz.timezone("Asia/Tashkent")
ACCESS_TOKEN_EXPIRE_MINUTES = 60*24  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')   # should be kept secret
JWT_REFRESH_SECRET_KEY =  os.environ.get('JWT_REFRESH_SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')

def get_db():
    db = session
    return db


def transform_list(lst, size, key):
    if key=='id':
    
        return [[f"{item.id}" for item in lst[i:i+size]] for i in range(0, len(lst), size)]
    if key=='name':
        return [[f"{item.name}" for item in lst[i:i+size]] for i in range(0, len(lst), size)]


def generate_text(lst):
    data = {}
    isin = []
    sending_text = f"Мои заказы: "
    a = 0
    for i in lst:
        if i.fillial.name not in isin:
            isin.append(i.fillial.name)
            data[i.fillial.name]=f"#{i.id}s"
        else:
            data[i.fillial.name]=data[i.fillial.name]+f", #{i.id}s"
    
    for inf in data.keys():
        a+=1
        sending_text = sending_text+f"\n\n{a}) {inf} - ( {data[inf]} )"
    sending_text = sending_text.replace('АРС','')
    return sending_text

def data_transform(lst):
    return [[{"text":i.name,'callback_data':i.id}] for i in lst]


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt


def sendtotelegram(bot_token,chat_id,message_text,buttons):
    keyboard = {
        'inline_keyboard': [
            [{'text': 'Yes', 'callback_data': '-1'}],
            [{'text': 'No', 'callback_data': '-2'}],
            buttons
        ]
    }

    # Create the request payload
    payload = {
        'chat_id': chat_id,
        'text': message_text,
        'reply_markup': keyboard,
        'parse_mode': 'HTML'
    }

    # Send the request to send the inline keyboard message
    response = requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json=payload,)

    # Check the response status
    if response.status_code == 200:
        return response
    else:
        return False
    

def is_time_between(start_time, end_time, current_time=None):
    if current_time is None:
        current_time = datetime.now(timezonetash).time()
    
    # Convert time strings to time objects
    start = start_time#datetime.strptime(start_time, '%H:%M').time()
    end = end_time#datetime.strptime(end_time, '%H:%M').time()

    # Check if current time is between start and end time
    if start <= current_time <= end:
        return True
    else:
        return False
    

def sendtotelegram(bot_token,chat_id,message_text):
    keyboard = {
        'inline_keyboard': [
            [{'text': 'Yes', 'callback_data': 'accepted'}],
            [{'text': 'No', 'callback_data': 'denied'}]
        ]
    }

    # Create the request payload
    payload = {
        'chat_id': chat_id,
        'text': message_text,
        'reply_markup': keyboard,
        'parse_mode': 'HTML'
    }

    # Send the request to send the inline keyboard message
    response = requests.post(f'https://api.telegram.org/bot{bot_token}/sendMessage', json=payload,)

    # Check the response status
    if response.status_code == 200:
        return response
    else:
        return False