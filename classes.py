import base
import handlers
import time


class User:
    username = None
    name = None
    surname = None
    user_id = None
    registration_time = None
    source = None
    dialogues = 0
    sphere = None
    salary = None
    interests = None

    def inc_dia(self):
        self.dialogues += 1
        base.inc_user_dia((self.user_id))
        data = base.get_dia_news((self.dialogues))
        if data:
            for news in data:
                handlers.send_message(news[0], self.user_id)

    def __init__(self, message=None, user_id=None):
        if message or user_id:
            args = base.get_user((int(message.from_user.id) if message else int(user_id)))
            if not args and message:
                base.authorize(message)
                return
            args = args[-1]
            self.username = args[1]
            self.name = args[2]
            self.surname = args[3]
            self.user_id = args[4]
            self.source = args[5]
            self.dialogues = args[6]
            self.sphere = args[7]
            self.salary = args[8]
            self.interests = args[9]
            self.registration_time = args[10]


class Dialogue:
    user1 = User()      # отправлял поиск
    user2 = User()      # откликнулся
    start_time = None
    messages_left = None
    from_f_user = None      # отправлено первым юзером
    from_s_user = None      # отправлено вторым юзером

    def __init__(self, user1=None, user2=None, user_id=None):
        if user_id:
            print('start_access_to_base', time.time())
            data = base.get_dialogue(user_id)
            print('finish_access_to_base', time.time())
            if not data:
                return None
            print(data)
            print('handle_data_start', time.time())
            self.user1 = User(user_id=data[-1][0])
            self.user2 = User(user_id=data[-1][1])
            self.start_time = data[-1][2]
            self.messages_left = data[-1][3]
            self.from_f_user = data[-1][4]
            self.from_s_user = data[-1][5]
            print('handle_data_finish', time.time())

        else:
            self.user1 = user1
            self.user2 = user2
            self.start_time = time.mktime(time.localtime())
            self.messages_left = 0
            self.from_f_user = 0
            self.from_s_user = 0
            base.insert_dialogue((self.user1.user_id), (self.user2.user_id), (str(self.start_time)), (0), (0), (0))

    def get_interlocutor(self, user_id):
        return self.user2 if self.user1.user_id == user_id else self.user1

    def forward_message(self, message):
        print('start_get_data_from_object', time.time())
        to_user = self.get_interlocutor(message.from_user.id)
        print('finish_get_data_from_object , start_send_message', time.time())
        handlers.send_message(message.text, to_user.user_id)
        print('finish_send_message', time.time())







