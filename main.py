# -*- coding: utf-8 -*-

from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, MessageService
from telethon.tl.functions.messages import GetHistoryRequest

from User import User

import csv
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']


print("Введите пароль двухфакторной аутентификации")
print("(если он не используется или сессия")
password = input("уже существует, нажмите Enter): ")
client = TelegramClient('telegramAPI', api_id, api_hash,  system_version="4.16.30-vxCUSTOM")
client.start(password=password)

chats = []
last_date = None
chunk_size = 200
groups = []
list_of_users = list()
users_reactions = dict()
users_comments = dict()

result = client(GetDialogsRequest(
    offset_date=last_date,
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=chunk_size,
    hash=0
))

chats.extend(result.chats)
for chat in chats:
    try:
        if chat.broadcast:
            groups.append(chat)
    except:
        continue

print("Выберите чат для анализа сообщений:")
i = 1
for g in groups:
    print(str(i) + " - " + g.title)
    # print(g)
    i += 1

g_index = -1
while 0 > g_index or g_index > len(groups) - 1:
    try:
        g_index = int(input("Введите номер группы, о которой вам нужно получить информацию: "))
    except:
        print("Введите целочисленное значение от 0 до ", len(groups) - 1)

target_group = groups[int(g_index)]
# print("Parsing users...")
all_participants = []
all_participants = client.get_participants(target_group)

for user in all_participants:
    user_id = user.id
    if user.username:
        username = user.username
    else:
        username = ""
    if user.first_name:
        first_name = user.first_name
    else:
        first_name = ""
    if user.last_name:
        last_name = user.last_name
    else:
        last_name = ""
    list_of_users.append(User(user_id, username, first_name, last_name))
    users_comments[user_id] = 0
    users_reactions[user_id] = 0

# print("Parsing of group members successfully completed")

offset_id = 0
limit = 100
all_log_messages = []
total_messages = 0
total_count_limit = 0

print("Парсинг сообщений...")
while True:
    history = client(GetHistoryRequest(
        peer=target_group,
        offset_id=offset_id,
        offset_date=None,
        add_offset=0,
        limit=limit,
        max_id=0,
        min_id=0,
        hash=0
    ))

    # messages = client.get_messages(target_group, limit=400)
    # messages.reverse()
    # for message in tqdm(messages):
    #     print(message.date)
    #     message.download_media('./media/')

    if not history.messages:
        break
    messages = history.messages
    for message in messages:
        if isinstance(message, MessageService):
            continue
        # from_user = message.from_id
        # if from_user is not None and not isinstance(from_user, PeerChannel):
        #     from_user_id = from_user.user_id
        #     if from_user_id in users_comments:
        #         users_comments[from_user_id] += 1
        # if from_user is not None:
        #     from_user_id = from_user.user_id
        #     if from_user_id in users_comments:
        #         users_comments[from_user_id] += 1
        # if message.reactions is not None and message.reactions.recent_reactions is not None:
        #     for reaction in message.reactions.recent_reactions:
        #         if reaction.peer_id.user_id in users_reactions: # Проверяем, что пользователь подписан на чат
        #             users_reactions[reaction.peer_id.user_id] += 1
        all_log_messages.append(message)
    offset_id = messages[len(messages) - 1].id
    if total_count_limit != 0 and total_messages >= total_count_limit:
        break

for user in list_of_users:
    user.num_of_reactions = users_reactions[user.user_id]
    user.num_of_comments = users_comments[user.user_id]
    user.num_of_all_activities = user.num_of_reactions + user.num_of_comments

print("Парсинг сообщений успешно завершен")
print("Сохранение данных в файлах...")

with open("csv/messages_log.csv", "w", encoding="utf-8-sig") as f:
    writer = csv.writer(f, delimiter=",", lineterminator="\n")
    for message in all_log_messages:
        writer.writerow([message])

print("Сохранение данных успешно завершено")
