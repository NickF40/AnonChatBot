"""
dialogues: user1_id INTEGER, user2_id INTEGER, start_time TEXT,
           messages_left INTEGER, user1_msg INTEGER, user2_msg INTEGER

queue_table: user_id INTEGER, start_time INTEGER

users_table: id SERIAL PRIMARY KEY, username TEXT, name TEXT, surname TEXT,
             user_id INTEGER, source TEXT, dialogues INTEGER, sphere TEXT,
             salary INTEGER, interests TEXT, registration_time INTEGER

news:   message TEXT, day_counter INTEGER, dia_counter INTEGER

texts_table: id SERIAL PRIMARY KEY, text Text

"""
# -*- coding: utf-8-*-
import postgresql as pg
from classes import *
from configs import *
import time

db = pg.open(**db_configs)


get_users = db.prepare("SELECT * FROM users_table ")

get_user_id = db.prepare('SELECT user_id FROM users_table')

get_dialogues = db.prepare("SELECT * FROM dialogues ")

get_queue = db.prepare("SELECT * FROM queue_table")

get_user = db.prepare("SELECT * FROM users_table WHERE user_id = $1 ")

inc_user_dia = db.prepare('UPDATE users_table SET dialogues = dialogues + 1 WHERE user_id = $1')


get_from_queue = db.prepare('SELECT user_id FROM queue_table '
                            'WHERE start_time = (SELECT min(start_time) FROM queue_table) LIMIT 1')

delete_queue = db.prepare('DELETE FROM queue_table WHERE user_id = $1 ')

get_dialogue = db.prepare("SELECT * FROM dialogues WHERE user1_id = $1 OR user2_id = $1")

get_notifications = db.prepare("SELECT * FROM notifications")

                        # $1 = time.time() , $2 =
get_by_time = db.prepare('SELECT user_id FROM users_table WHERE dialogues = 0 AND $1 - registration_time > $2 AND $1 - registration_time < $2 + 60 ')

delete_dialogue = db.prepare('DELETE FROM dialogues WHERE user1_id = $1 OR user2_id = $1')

insert_dialogue = db.prepare('INSERT INTO dialogues VALUES($1, $2, $3, $4, $5, $6)')

insert_in_queue = db.prepare('INSERT INTO queue_table VALUES($1, $2)')

insert_user = db.prepare('INSERT INTO users_table(username, name, surname,'
                         ' user_id, '
                         ' source, dialogues, registration_time)VALUES($1,$2,$3,$4,$5,$6,$7)')

get_last_day_users = db.prepare('SELECT * FROM users_table WHERE registration_time > ($1 - 60*60*24)')

get_last_week_users = db.prepare('SELECT * FROM users_table WHERE registration_time > ($1 - 60*60*24*7)')


get_daily_news = db.prepare("SELECT * FROM news WHERE day_counter > 0")

get_dia_news = db.prepare('SELECT * FROM news WHERE dia_counter = $1')

get_text = db.prepare('SELECT text FROM texts_table WHERE id = $1')


def get_all_user_id():
    data = get_user_id()
    # print(data)
    return [i[0] for i in data]


def get_tables_data():
    return ''.join([
        str(get_dialogues()), '\n',
        str(get_queue()), '\n',
        str(get_users())
    ])


def authorize(message=None, call=None):
    user_id = call.message.from_user.id if call else message.from_user.id
    data = get_user((user_id))
    if not data:
        insert_user((message.from_user.username,
                    message.from_user.first_name,
                    message.from_user.last_name,
                    message.from_user.id,
                    message.text[7:], 0,
                    int(time.mktime(time.localtime()))))

    else:
        User(message=message)


def check(user_id):
    return bool(get_dialogue((user_id)))


def find(user_id):
    if check(user_id):                  # keys
        return -2                       # 0: dialog successfully created
    data = get_from_queue()             # 1: user added in queue
    if not data:                        # -1: user repeated query
        insert_in_queue((user_id), (time.mktime(time.localtime())))
        return 1
    else:
        if data[-1][0] == user_id:
            return -1
        delete_queue((data[-1][0]))
        user1 = User(user_id=user_id)
        user2 = User(user_id=data[-1][0])
        Dialogue(user1=user1, user2=user2)          # create dialog
        return 0







