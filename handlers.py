import base
import markups
import telebot
import classes
from configs import *
import postgresql as pg

db = pg.open(**db_configs)

bot = telebot.AsyncTeleBot(TOKEN)


def send_message(message, to_user_id):
    bot.send_message(to_user_id, message,
                     reply_markup=markups.end_markup(to_user_id))
