from telebot import *
import base


def make_inline_markup(width, length, *args):
    markup = types.InlineKeyboardMarkup(row_width=width)
    buts = [types.InlineKeyboardButton(str(args[i]), callback_data=str(args[i + 1])) for i in range(0, length * 2, 2)]
    markup.add(*buts)
    return markup


def make_markup(width, length, is_one_time, *args):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=is_one_time, row_width=width)
    markup.add(*[types.KeyboardButton(args[i]) for i in range(length)])
    return markup


def main_menu():
    return make_markup(1, 2,True, base.get_text((12))[-1][0], base.get_text((13))[-1][0])


def start_dia():
    return make_inline_markup(1, 1, base.get_text((12))[-1][0], 1)


def end_markup(user_id):
    return make_markup(1, 1, True, base.get_text((14))[-1][0])

