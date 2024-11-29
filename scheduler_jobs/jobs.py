import json
from typing import Optional
import pytz
import requests
from datetime import datetime
import crud
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = 'https://api.service.safiabakery.uz/'
BOTTOKEN = os.environ.get('BOT_TOKEN')
IT_SUPERGROUP = os.environ.get('IT_SUPERGROUP')
timezonetash = pytz.timezone("Asia/Tashkent")


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
