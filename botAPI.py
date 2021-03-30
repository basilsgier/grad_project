import requests
from config import connection, TOKEN, TELEGRAM_SEND_MESSAGE_URL
from parent import ask_question, ask_question2
from teacher import *

role_ = ""
class_2 = -1
asker_id_ = None
ques = None
last_similar_questions = None
parent_last_question = None


def what_can_i_do(chat_id):
    requests.get(
        TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id,
                                         "You are the boss 😎 you can do one of the following things:\n"
                                         "/announce <Announcement> to send an announcement to every parent in the class you "
                                         "are in\n"
                                         "/add_question <Question> to add a general question"))


def parse_command(com, chat_id, name):
    global role_, asker_id_, ques
    global class_2
    global last_similar_questions, parent_last_question
    class_ = None
    role = None
    parsed = com.split(" ", 1)  # maxsplit = 1
    first_command = parsed[0]
    with connection.cursor() as cursor:
        sql = "SELECT * FROM `users` where `chat_id`=%s"
        cursor.execute(sql, chat_id)
        result = cursor.fetchone()
        if result is not None:
            role = result['role']
            class_ = result['class']
        else:
            role = role_
            class_ = class_2
    if first_command == "/start":
        start(chat_id)
    elif first_command.lower() == "teacher" or first_command.lower() == "parent":
        role_ = first_command.lower()
        requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "What class are you in?\nWrite class <number>, "
                                                                      "so I can know to which class I should add you 😉"))
    elif first_command.lower() == "class":
        class_2 = parsed[1]
        if role_ == "teacher":
            requests.get(
                TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id,
                                                 "Okay good!\nOne more thing, are you the main teacher or not ? (yes/no)"))
        else:
            add_user(chat_id, role_, class_2, None)
            requests.get(
                TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "Welcome!! " + name + " you have been registered as"
                                                                                       " " + role_ + " in class " + class_2))
    elif first_command.lower() == "yes":
        if role_ == "teacher":
            add_user(chat_id, role_, class_2, "main teacher")
            requests.get(
                TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "Welcome!! " + name + " you have been registered as"
                                                                                       " the main teacher" + " in class " + class_2))
            what_can_i_do(chat_id)
    elif first_command.lower() == "no":
        if role_ == "teacher":
            add_user(chat_id, role_, class_2, "teacher")
            requests.get(
                TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "Welcome!! " + name + " you have been registered as"
                                                                                       " " + role_ + " In class " + class_2))
            what_can_i_do(chat_id)
    # elif first_command == "/answer":
    #     if role == "parent":
    #         requests.get(
    #             TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "You are a parent you can not answer a question 😉"))
    #     else:
    #         if len(parsed) <= 1:
    #             requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "You should write /answer "
    #                                                                           "and after it your answer"))
    #         else:
    #             answer_the_last_question(parsed[1], chat_id)
    # elif first_command == "/ask":
    #     if len(parsed) <= 1:
    #         requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "You should write /ask "
    #                                                                       "and after it your question"))
    #     else:
    #         ask_question(parsed[1], chat_id)
    # elif first_command == "/ask_privately":
    #     if len(parsed) <= 1:
    #         requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "You should write /ask_privately "
    #                                                                       "and after it your question"))
    #     else:
    #         asker_id_ = ask_question2(parsed[1], chat_id, class_)
    elif first_command == "@ans":
        if role == "parent":
            requests.get(
                TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "You are a parent you can not answer a question 😉"))
        else:
            if len(parsed) <= 1:
                requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "You should write @ans "
                                                                              "and after it your answer"))
            else:
                ques = answer_question(chat_id, asker_id_, parsed[1])
    elif first_command == "/add_question":
        if role == "parent":
            requests.get(
                TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "You are a parent you can not add a question 😔"))
        else:
            if len(parsed) <= 1:
                requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "You should write /add_question "
                                                                              "and after it your question"))
            else:
                add_question(parsed[1], chat_id)
    elif first_command == "@answer":
        if role == "parent":
            requests.get(
                TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "You are a parent you can not answer a question 😉"))
        else:
            if len(parsed) <= 1:
                requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "You should write @answer "
                                                                              "and after it your answer"))
            else:
                answer_add_question(parsed[1], chat_id)
    elif first_command == "/announce":
        if role == "parent":
            requests.get(
                TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "You are a parent you can not send announcement 🙃"))
        else:
            if len(parsed) <= 1:
                requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "You should write /announce "
                                                                              "and after it your announcement"))
            else:
                add_announcement(parsed[1], class_)
    elif first_command.lower() == "general":
        requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "Saved in FAQ"))
    elif first_command.lower() == "private":
        remove_question(chat_id, ques)
    elif first_command.lower() == "hello" or first_command.lower() == "hey" or first_command.lower() == "hi" or first_command.lower() == "sup":
        requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, f"Hey!! {name},\n"
                                                                      "My name is Tam how can I help you? \n"))
        if role == "teacher":
            what_can_i_do(chat_id)
    elif first_command[0] == '%':
        if 0 <= int(first_command[1:]) < len(last_similar_questions):
            with connection.cursor() as cursor:
                query = f"SELECT * FROM QA WHERE question = '{last_similar_questions[int(first_command[1:])]}'"
                cursor.execute(query)
                res = cursor.fetchone()
                if res is not None:
                    requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "The answer is:\n" + res['answer']))
    elif first_command.lower() == 'none':
        with connection.cursor() as cursor:
            query = f"INSERT INTO parentsQuestions VALUES({chat_id},'{parent_last_question}')"
            cursor.execute(query)
            ask_question2(parent_last_question, class_)
            requests.get(
                TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "There is no answer yet, I will check with the "
                                                                 "teacher and get back to you"))
            connection.commit()
    elif first_command.lower() == "help":
        requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "Contact technical support:\n"
                                                                      "Abeer Dow,  Phone: 0547570104\n"
                                                                      "Basil Sgier,  Phone: 0533013218\n"
                                                                      "Aseel Nassar,  Phone: 0509091207\n"
                                                                      "❤ Tam Team ❤"))
    else:
        if role == "teacher":
            requests.get(
                TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "Unavailable command you can do the following:\n"))
            what_can_i_do(chat_id)
        else:
            asker_id_, parent_last_question, last_similar_questions = ask_question(com, chat_id, class_)
    return ""


def add_user(chat_id, role, class_, has_job):
    with connection.cursor() as cursor:
        if has_job is None:
            sql = "INSERT INTO `Users` VALUES (%s,%s,%s,NULL)"
            cursor.execute(sql, (role, class_, chat_id))
        else:
            sql = "INSERT INTO `Users` VALUES (%s,%s,%s,%s)"
            cursor.execute(sql, (role, class_, chat_id, has_job))
        connection.commit()


def start(chat_id):
    with connection.cursor() as cursor:
        sql = "SELECT * FROM `users` where `chat_id`=%s"
        cursor.execute(sql, chat_id)
        result = cursor.fetchone()
        if result is not None:
            requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "Hi, what would you like to do today?\n"
                                                                          "It seems you are already registered.\n"
                                                                          "Contact technical support if you want to change your registration\n"
                                                                          "Basil Sgier,  Phone: 0533013218\n"
                                                                          "Aseel Hussien,  Phone: 0505577407\n"
                                                                          "❤ Tam Team ❤"))
        else:
            requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "Are you a parent or a teacher?"))
