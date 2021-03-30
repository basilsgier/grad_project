import pymysql

TOKEN = '1606894599:AAF2ejrSQiw02xQ7mKfX9w69_BnsTSC-Hwc'
NKROG_URL = "https://34fc19a3a62b.ngrok.io"
TELEGRAM_INIT_WEBHOOK_URL = 'https://api.telegram.org/bot{}/setWebhook?url={}/message'.format(TOKEN, NKROG_URL)
TELEGRAM_SEND_MESSAGE_URL = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"


connection = pymysql.connect(
    host="localhost",
    user="root",
    password="zaq123",
    db="maindb_1",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)

if connection.open:
    print("the connection is opened")