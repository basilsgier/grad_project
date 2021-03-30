from flask import Flask, request, Response
from config import TELEGRAM_INIT_WEBHOOK_URL, TOKEN, TELEGRAM_SEND_MESSAGE_URL
from botAPI import parse_command
import requests

app = Flask(__name__)

requests.get(TELEGRAM_INIT_WEBHOOK_URL)


@app.route('/message', methods=["POST"])
def handle_message():
    if request.get_json().get('edited_message'):
        msg = request.get_json()['edited_message']['text']
        chat_id = request.get_json()['edited_message']['chat']['id']
        chat_name = request.get_json()['edited_message']['from']['first_name']
    else:
        msg = request.get_json()['message']['text']
        chat_id = request.get_json()['message']['chat']['id']
        chat_name = request.get_json()['message']['from']['first_name']
    res = requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, parse_command(msg, chat_id, chat_name)))
    return Response("success")


if __name__ == "__main__":
    app.run(port=3002)
