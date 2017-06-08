import requests.exceptions as r_exceptions
import telebot
from telegram.ext import Updater, Job, dispatcher
import markups
import time
from configs import *
import postgresql as pg
from classes import *
from requests import ConnectionError
import logging

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    filename='ulog.log', level=logging.INFO)

# config your database here
db = pg.open(**db_configs)

bot = telebot.TeleBot(TOKEN)

upd = Updater(TOKEN)
queue = upd.job_queue


def check_new(bot_, job):
    for d in base.get_notifications():
        print(time.time(), d)
        for id_ in base.get_by_time((int(time.time())), (int(d[1])*60)):
            bot_.send_message(chat_id=id_[0], text=d[0])


queue.put(Job(check_new, interval=30), 0)

'''
# news_sender_block
def spam(bot_, job):
    for news in job.context[1]:
        for id_ in job.context[0]:
            bot_.send_message(chat_id=id_, text=news)

data = dict()


for d in base.get_daily_news():
    print(data)
    if d[1] not in data.keys():
        print('data.keys = ',data.keys())
        data.update({d[1]: [d[0]]})
    else:
        print('get = ', data.get(d[1]))
        data.update({d[1]: [*data.get(d[1]), d[0]]})

print([(data.get(key), key) for key in data.keys()])


for interval in data.keys():
    context_ = [
        base.get_all_user_id(),
        str(data.get(interval))
    ]
    job_sec = Job(spam, DAY * int(interval), context=context_)
    queue.put(job_sec, 0.0)
'''
queue.start()


def send_message(message, to_user_id):
    bot.send_message(to_user_id, message,
                     reply_markup=markups.end_markup(to_user_id))


@bot.message_handler(commands=['start'])
def handle_start(message):
    # base.get_tables_data()
    markup = markups.start_dia()
    base.authorize(message=message)
    bot.send_message(message.chat.id, base.get_text((1))[-1], reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == base.get_text((14))[-1][0], content_types=['text'])
def handle_quit(message):
    dia = Dialogue(user_id=message.from_user.id)
    user2 = dia.get_interlocutor(user_id=message.from_user.id)
    base.inc_user_dia((message.from_user.id))
    base.delete_dialogue((message.from_user.id))
    bot.send_message(message.chat.id, base.get_text((1))[-1], reply_markup=markups.main_menu())
    bot.send_message(user2.user_id, base.get_text((1))[-1], reply_markup=markups.main_menu())


@bot.message_handler(func=lambda message: message.text in [base.get_text((12))[-1][0], base.get_text((13))[-1][0]], content_types=['text'])
def handle_menu(message):
        if message.text == base.get_text((12))[-1][0]:
            task = bot.send_message(message.chat.id, base.get_text((2))[-1][0])
            bot.send_chat_action(message.chat.id, 'typing')
            signal = base.find(message.from_user.id)
            if signal == 0:
                interlocutor = (Dialogue(user_id=message.from_user.id)).get_interlocutor(message.from_user.id)
                interlocutor.inc_dia()
                user1 = User(user_id=message.from_user.id)
                user1.inc_dia()
                if not (interlocutor.sphere and interlocutor.salary and interlocutor.interests):
                    text = base.get_text((3))[-1][0]
                else:
                    text = ''.join([
                        str(base.get_text((3))[-1][0]), '\n',
                        str(base.get_text((21))[-1][0]),
                        str(interlocutor.sphere),
                        str(base.get_text((22))[-1][0]),
                        str(interlocutor.salary),
                        str(base.get_text((23))[-1][0]),
                        str(interlocutor.interests)
                    ])
                if not (user1.sphere and user1.salary and user1.interests):
                    text1 = base.get_text((3))[-1][0]
                else:
                    text1 = ''.join([
                        str(base.get_text((3))[-1][0]), '\n',
                        str(base.get_text((21))[-1][0]),
                        str(user1.sphere),
                        str(base.get_text((22))[-1][0]),
                        str(user1.salary),
                        str(base.get_text((23))[-1][0]),
                        str(user1.interests)
                    ])
                bot.send_message(message.chat.id, text,
                                 reply_markup=markups.end_markup(message.from_user.id))
                bot.send_message(interlocutor.user_id, text1,
                                 reply_markup=markups.end_markup(interlocutor.user_id))
            elif signal == -2:
                bot.send_message(message.chat.id, base.get_text((10))[-1][0])
            else:
                bot.send_chat_action(message.chat.id, 'typing')
        elif message.text == base.get_text((13))[-1][0]:
            bot.send_message(message.chat.id, base.get_text((4))[-1][0],
                             reply_markup=markups.make_inline_markup(2, 2, base.get_text((18))[-1][0], 3,
                                                                     base.get_text((19))[-1][0], 4))

@bot.callback_query_handler(func=lambda call: int(call.data) == 3)
def handle_yes(call):
    bot.send_message(call.message.chat.id, base.get_text((5))[-1], reply_markup=None)
    bot.register_next_step_handler(call.message, get_1_answer)


def get_1_answer(message):
    db.execute("UPDATE users_table SET sphere = '{0}' WHERE user_id = '{1}'".format(message.text, message.from_user.id))
    print(base.get_text((6)))
    bot.send_message(message.chat.id, base.get_text((6))[-1])
    bot.register_next_step_handler(message, get_2_answer)


def get_2_answer(message):
    try:
        data = int(message.text)
    except Exception as e:
        bot.send_message(message.chat.id,
                         "Упс.. Что-то пошло не так, напишите цифру без пробелов - в формате '100000'")
        bot.register_next_step_handler(message, get_2_answer)
        return
    db.execute(
        "UPDATE users_table SET salary = '{0}' WHERE user_id = '{1}'".format(int(message.text), message.from_user.id))
    bot.send_message(message.chat.id, base.get_text((7))[-1][0])
    bot.register_next_step_handler(message, get_3_answer)


def get_3_answer(message):
    db.execute("UPDATE users_table SET interests = '{0}' WHERE user_id = '{1}'".format(message.text, message.from_user.id))
    print(base.get_text(8))
    bot.send_message(message.chat.id, base.get_text((8))[-1], reply_markup=markups.main_menu())


@bot.callback_query_handler(func=lambda call: int(call.data) == 4)
def handle_yes(call):
    bot.send_message(call.message.chat.id, base.get_text((9))[-1][0], reply_markup=markups.main_menu())




@bot.message_handler(commands=['status'])
def handle_status(message):
    text = ''.join([
        str(len(base.get_dialogues())*2 + (len(base.get_queue()))), base.get_text((20))[-1][0],
        str(len(base.get_last_day_users(time.mktime(time.localtime())))), base.get_text((16))[-1][0],
        str(len(base.get_last_day_users(time.mktime(time.localtime())))), base.get_text((17))[-1][0]
    ])
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['help'])
def handle_help(message):
    if base.check(message.from_user.id):
        bot.send_message(message.chat.id, base.get_text((10))[-1][0])
    else:
        bot.send_message(message.chat.id, base.get_text((1))[-1][0], reply_markup=markups.main_menu())


@bot.message_handler(content_types=['text'])
def handle_messages(message):
    logging.log(20,' : '.join([str(message.from_user.id),message.from_user.username,message.text]))
    print('-------------------------------')
    start_time = time.time()
    print('start_time = ', start_time)
    user = message.from_user.id
    if base.get_dialogue((user)):
        dia = Dialogue(user_id=message.from_user.id)
        print('start_receive_message', time.time())
        dia.forward_message(message)
        print('finish_receive_message', time.time())
   # else:
    #    handlers.handle(telebot.types.CallbackQuery(id=0, from_user=message.from_user,data=1,chat_instance=message.chat,message=message))
    print('-------------------------------')



@bot.message_handler(content_types=['video'])
def handle_video(message):
    pass


while True:
    try:
        bot.polling(none_stop=True, interval=0)
    except ConnectionError as e:
        logging.critical(u'FATAL CONNECTION ERROR')
        time.sleep(30)
        continue
    except r_exceptions.Timeout as e:
        time.sleep(5)
        continue
