# Custom Framework Imports
from framework.fragment import Fragment
from framework.telegram import Telegram
from framework.processing import Processor

# Imports
import colorama
import threading
import json
import telebot
import random

# Conf. 1
clients = set()
proxies = set()
usernames = set()

with open('./input/proxies.txt', 'r') as PL:
    for proxy in PL.readlines():
        proxies.add(proxy.strip())

with open('./input/usernames.txt', 'r') as UL:
    for username in UL.readlines():
        usernames.add(username.strip())

# Conf. 2
settings = json.load(open('./settings.json', 'r', encoding = 'utf-8'))
processor = Processor(settings['threads'])

# Functions
class Functions:
    def getProxy() -> str | None:
        if proxies and settings.get('use_proxies', False):
            return random.choice(list(proxies))
        return None
        
    def telegramIsAvailable(client: Telegram, username: str) -> bool:
        try:
            response = client.getUsername(username)
            response_text = response.text

            if '<div class="tgme_page_extra">' in response_text:
                return True
            return False
        except Exception as E:
            return None
        
    def fragmentIsAvailable(client: Fragment, username: str) -> bool:
        try:
            response = client.getUsername(username)
            response_status_code = response.status_code

            if 302 == response_status_code: # ref. XT
                return True
            return False
        except Exception as E:
            return None
