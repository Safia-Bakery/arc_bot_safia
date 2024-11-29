from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.jobstores.base import JobLookupError, ConflictingIdError
import datetime
import json
import re
from datetime import datetime, timedelta
from typing import Union, Any, Optional
from jose import jwt
import requests
import string
import random
import pytz
import crud
import os
from dotenv import load_dotenv

load_dotenv()

SCHEDULER_DATABASE_URL = os.environ.get('SCHEDULER_DATABASE_URL')
BASE_URL = 'https://api.service.safiabakery.uz/'
BOTTOKEN = os.environ.get('BOT_TOKEN')
IT_SUPERGROUP = os.environ.get('IT_SUPERGROUP')
timezonetash = pytz.timezone("Asia/Tashkent")

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')  # should be kept secret
JWT_REFRESH_SECRET_KEY = os.environ.get('JWT_REFRESH_SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')
backend_base_url = os.environ.get('BACKEND_BASE_URL')
backend_pass = os.environ.get('BACKEND_PASS')


def validate_phone_number(phone):
    # Шаблон для проверки, чтобы номер содержал только "+" в начале (если есть) и цифры
    # pattern = r"^\+?\d{9,}$"  # Начинается с "+" (если есть), за которым следуют не менее 9 цифр
    pattern = r"^\+?\d+$"  # Номер содержит только "+" в начале (если есть) и цифры
    if re.fullmatch(pattern, phone):
        # Убираем "+" (если есть) и проверяем количество цифр
        digit_count = len(re.sub(r"\D", "", phone))  # Убираем все символы, кроме цифр
        if digit_count == 9 or digit_count == 12:  # Проверка строго на 9 или 12 цифр
            return True

    return False


def clean_and_format_phone_number(phone):
    # Удаляем все символы, кроме цифр и плюса
    cleaned = re.sub(r"[^\d+]", "", phone)

    # Добавляем "+" в начало, если его нет
    if not cleaned.startswith('998') and len(cleaned) < 10:
        cleaned = '+998' + cleaned
    elif cleaned.startswith('998') and len(cleaned) > 10:
        cleaned = '+' + cleaned

    return cleaned


def transform_list(lst, size, key):
    if key == 'id':
        return [[f"{item.id}" for item in lst[i:i + size]] for i in range(0, len(lst), size)]
    if key == 'name':
        return [[f"{item.name}" for item in lst[i:i + size]] for i in range(0, len(lst), size)]


def generate_text(lst):
    data = {}
    isin = []
    sending_text = f"Мои заказы: "
    a = 0
    for i in lst:
        if i.fillial.parentfillial.name not in isin:
            isin.append(i.fillial.parentfillial.name)
            data[i.fillial.parentfillial.name] = f"#{i.id}s"
        else:
            data[i.fillial.parentfillial.name] = data[i.fillial.parentfillial.name] + f", #{i.id}s"
    for inf in data.keys():
        a += 1
        sending_text = sending_text + f"\n\n{a}) {inf} - ( {data[inf]} )"
    sending_text = sending_text.replace('АРС', '')
    return sending_text


def data_transform(lst):
    return [[{"text": i.name, 'callback_data': i.id}] for i in lst]


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt


def sendtotelegram(bot_token, chat_id, message_text, buttons):
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
        'parse_mode': 'Markdown'
    }

    # Send the request to send the inline keyboard message
    response = requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json=payload, )

    # Check the response status
    if response.status_code == 200:
        return response
    else:
        return False


def sendtotelegramviewimage(bot_token, chat_id, message_text, buttons):
    keyboard = {
        'inline_keyboard': [
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
    response = requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json=payload, )

    # Check the response status
    if response.status_code == 200:
        return response
    else:
        return False


def is_time_between(start_time, end_time, current_time=None):
    if current_time is None:
        current_time = datetime.now(timezonetash).time()

    # Convert time strings to time objects
    start = start_time  # datetime.strptime(start_time, '%H:%M').time()
    end = end_time  # datetime.strptime(end_time, '%H:%M').time()

    # Check if current time is between start and end time
    if start <= current_time <= end:
        return True
    else:
        return False


def generate_random_string(length=10):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


def inlinewebapp(bot_token, chat_id, message_text, url):
    keyboard = {
        "inline_keyboard": [
            [{"text": "Оставить отзыв🌟", "web_app": {"url": url}}],
        ]
    }

    # Create the request payload
    payload = {
        "chat_id": chat_id,
        "text": message_text,
        "reply_markup": keyboard,
        "parse_mode": "Markdown",
    }

    # Send the request to send the inline keyboard message
    response = requests.post(
        f"https://api.telegram.org/bot{bot_token}/sendMessage",
        json=payload,
    )
    # Check the response status
    if response.status_code == 200:
        return response
    else:
        return False


info_string = f"""🔘 Отдел: АРС Розница -  +998(90)432-93-00\n\n
🔘 Отдел: АРС Учтепа -  +998(99)875-90-93\n\n
🔘 Отдел: Маркетинг -  +998(33)334-00-23\n\n
🔘 Отдел: Инвентарь -  +998(97)740-06-16\n\n
🔘 Отдел: IT - +998(77)133-00-11, @safiasupport\n\n
🔘 Отдел: Логистика (Учтепа) - +998(95)475-14-15"""


def confirmation_request(bot_token, chat_id, message_text):
    keyboard = {
        'inline_keyboard': [
            [{'text': 'Подтвердить', 'callback_data': '10'}],
            [{'text': 'Не сделано', 'callback_data': '11'}],
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
    response = requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json=payload, )

    # Check the response status
    if response.status_code == 200:
        return response
    else:
        return False


def send_iiko_document(request_id):
    url = f"{backend_base_url}/v2/iiko_transfer"
    headers = {
        'Authorization': f'Bearer {backend_pass}'
    }
    data = {
        'id': request_id
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()


def delete_from_chat(message_id, topic_id: Optional[int] = None):
    url = f'https://api.telegram.org/bot{BOTTOKEN}/deleteMessage'
    payload = {
        'chat_id': IT_SUPERGROUP,
        'message_id': message_id
    }
    if topic_id:
        payload["message_thread_id"] = topic_id

    # Send a POST request to the Telegram API to delete the message
    response = requests.post(url, json=payload)
    response_data = response.json()
    # Check the response status
    if response.status_code == 200:
        return response_data
    else:
        return False


def send_notification(topic_id, text, finishing_time, request_id: Optional[int] = None,
                      url: Optional[str] = None):
    inline_keyboard = {
        "inline_keyboard": [
            [
                {"text": "Завершить заявку", "callback_data": "complete_request"},
                {"text": "Отменить", "callback_data": "cancel_request"}
            ],
            [{"text": "Посмотреть фото", "url": f"{BASE_URL}{url}"}]
        ]
    }
    now = datetime.now(tz=timezonetash)
    if finishing_time is not None:
        remaining_time = finishing_time - now
        late_time = now - finishing_time

        if finishing_time >= now:
            text = f"{text}\n\n" \
                   f"<b> ‼️ Оставщиеся время:</b>  {str(remaining_time).split('.')[0]}"
        else:
            text = f"{text}\n\n" \
                   f"<b> ‼️ Просрочен на:</b>  {str(late_time).split('.')[0]}"

    url = f'https://api.telegram.org/bot{BOTTOKEN}/sendMessage'
    payload = {
        'chat_id': IT_SUPERGROUP,
        'text': text,
        'reply_markup': json.dumps(inline_keyboard),
        'parse_mode': 'HTML'
    }
    if topic_id:
        payload["message_thread_id"] = topic_id
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        response_data = response.json()
        new_message_id = response_data["result"]["message_id"]
        crud.update_it_request(id=request_id, message_id=new_message_id)
        return new_message_id
    else:
        return None


class JobScheduler:
    def __init__(self):
        # Configure job store
        jobstores = {
            "default": SQLAlchemyJobStore(url=SCHEDULER_DATABASE_URL)
        }
        self.scheduler = BackgroundScheduler(jobstores=jobstores)
        self.scheduler.start()

    def add_delete_message_job(self, job_id, scheduled_time, message_id, topic_id):
        try:
            self.scheduler.add_job("scheduler_jobs.jobs:delete_from_chat", 'date', run_date=scheduled_time,
                                   args=[message_id, topic_id], id=job_id, replace_existing=True)
        except JobLookupError:
            print(f"'{job_id}' job not found or already has completed !")

    def add_send_message_job(self, job_id, scheduled_time, topic_id, request_text, finishing_time, request_id, request_file):
        try:
            self.scheduler.add_job("scheduler_jobs.jobs:send_notification", 'date', run_date=scheduled_time,
                                   args=[topic_id, request_text, finishing_time, request_id, request_file],
                                   id=job_id, replace_existing=True)
        except JobLookupError:
            print(f"'{job_id}' job not found or already has completed !")

    def remove_job(self, job_id):
        try:
            self.scheduler.remove_job(job_id=job_id)
        except JobLookupError:
            print(f"'{job_id}' job not found or already has completed !")
