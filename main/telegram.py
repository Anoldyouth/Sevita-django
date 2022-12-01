import os

import requests
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)


def send_contacts(text: str):
    token = os.getenv("TOKEN")
    url = "https://api.telegram.org/bot"
    channel_id = os.getenv("CHANNEL_ID")
    url += token
    method = url + "/sendMessage"

    r = requests.post(method, data={
        "chat_id": channel_id,
        "text": text
    })

    if r.status_code != 200:
        raise Exception("Ошибка отправки!")
