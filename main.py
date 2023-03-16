from configparser import ConfigParser
import os.path
import conf
import mail
import telegram
import time
from models import messages
import flask_conn
import random
import string
import sys
import os
import markdown

config_path = 'settings.ini'

def sendMassagesUrl(message, parser, token_telegram, chat_id):
    domain = parser.get('accounts', 'domain')
    key = get_random_string(20)
    text = ('**От кого:** {} \n**Тема письма:** {} \n**Текст письма:** {}').format(message['from'], message['subject'], (domain + "?key=" + key))

    with flask_conn.app.app_context():
        flask_conn.db.session.add(messages.Messages(text_message=message['body'],from_message=message['from'],subject_message=message['subject'],key=key))
        flask_conn.db.session.commit()
        telegram.send_messages(token_telegram, dict(text=text, chat_id=chat_id, parse_mode='Markdown'))

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    print("Random string of length", length, "is:", result_str)
    return result_str

def main():
    parser = ConfigParser() 
    parser.read(config_path)
    email = parser.get('accounts', 'email')
    imap = parser.get('accounts', 'imap')
    password = parser.get('accounts', 'password')
    token_telegram = parser.get('accounts', 'token_telegram')
    chat_id = parser.get('accounts', 'chat_id')
    db = parser.get('accounts', 'db')
    imap = mail.imap_connect(imap, email, password)
    messagesList = mail.messages_list(imap)
    for message in messagesList:
        if (db == "False"):
                text = ('**От кого:** {} \n**Тема письма:** {} \n**Текст письма:** {}').format(message['from'], message['subject'], message['body'])
                chunks = [text[i:i+4096] for i in range(0, len(text), 4096)]
                for chunk in chunks:
                    res = telegram.send_messages(token_telegram, dict(text=chunk.replace('*', ''), chat_id=chat_id, parse_mode='Markdown'))
                    if (res['ok'] == False):
                         sendMassagesUrl(message, parser, token_telegram, chat_id)
        else:
            sendMassagesUrl(message, parser, token_telegram, chat_id)


if os.path.isfile(config_path):
    os.system("python wsgi.py &")
    while True:
        main()
        time.sleep(30)
else:
    domain = ''
    imap = sys.argv[1]
    email = sys.argv[2]
    password = sys.argv[3]
    token_telegram = sys.argv[4]
    chat_id = sys.argv[5]
    db = sys.argv[6]
    if (db == "True"):
        domain =  sys.argv[7]
    conf.createConfig(config_path, imap, email, password, token_telegram, chat_id, db, domain)
    main()