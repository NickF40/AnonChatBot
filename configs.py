"""
Edit your configs in this file

"""


TOKEN = '392293405:AAE2Hjy6zjj1qmx98VHGrHGiYduxYdGufz4'
DAY = 86400     # sec

WEBHOOK_HOST = 'localhost'                   # Write your host's IP
WEBHOOK_PORT = 8443                 # 443, 80, 88 or any free port
WEBHOOK_LISTEN = '0.0.0.0'          # Sometimes may need to write your host's IP again

WEBHOOK_SSL_CERTIFICATE = './webhook_cert.pem'  # Path to the ssl certificate
WEBHOOK_SSL_PRIVATE_KEY = './webhook_pkey.pem'  # Path to the ssl private key
WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % TOKEN

db_configs = dict(user='postgres', host='localhost', port='4077', password='89/b/3?!MK', database='postgres')
# 89/b/3?!MK