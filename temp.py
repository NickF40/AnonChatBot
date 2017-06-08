import time
import postgresql as pg
from configs import *

db = pg.open(**db_configs)


# get_by_time = db.prepare('SELECT user_id FROM users_table WHERE dialogues = 0 AND $1 - registration_time > $2 AND $1 - registration_time < $2 + 60 ')

print(db.prepare('SELECT * FROM texts_table')())