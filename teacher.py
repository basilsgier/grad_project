from config import connection, TELEGRAM_SEND_MESSAGE_URL, TOKEN
import requests
from keywords import get_keywords

the_question_to_answer = ""


def answer_question(teacher_chat_id, parent_chat_id, answer):
    with connection.cursor() as cursor:
        query = "SELECT * FROM parentsQuestions"
        cursor.execute(query)
        result = cursor.fetchone()
        if result is not None:
            ques = "'" + result['question'] + "'"
            lques = [result['question']]
            keywords = get_keywords(lques)
            query2 = f"INSERT INTO QA VALUES({result['chat_id']}, '{answer}', {ques}, '{keywords}')"
            cursor.execute(query2)
            query3 = f"DELETE FROM parentsQuestions WHERE question = {ques}"
            cursor.execute(query3)
            connection.commit()
            requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, parent_chat_id, "The teacher says:\n" + answer))
            requests.get(
                TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, teacher_chat_id, "Is this a general or a private question?"
                                                                         "(general/ private)"))
        else:
            requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, teacher_chat_id, "There are no questions to answer! "
                                                                                  "Thank you and have a nice day! :) "))
    return ques


def answer_the_last_question(answer, teacher_chat_id):
    with connection.cursor() as cursor:
        query = "SELECT * FROM parentsQuestionsQueue LIMIT 1"
        cursor.execute(query)
        result = cursor.fetchone()
        if result is not None:
            requests.get(
                TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, result['chat_id'], "The answer for your last question is :\n"
                                                 + answer))
            answer = "'" + answer + "'"
            ques = "'" + result['question'] + "'"
            lques = [result['question']]
            keywords = get_keywords(lques)
            query2 = f"INSERT INTO QA VALUES({teacher_chat_id}, {answer}, {ques}, '{keywords}')"
            cursor.execute(query2)
            query3 = f"DELETE FROM parentsQuestionsQueue WHERE question = {ques}"
            cursor.execute(query3)
            connection.commit()
        else:
            requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, teacher_chat_id, "THERE IS NO QUESTION TO ANSWER!!"))


def add_question(question, teacher_chat_id):
    global the_question_to_answer
    with connection.cursor() as cursor:
        query = f"SELECT * FROM QA WHERE question='{question}' and chat_id={teacher_chat_id}"
        cursor.execute(query)
        result = cursor.fetchone()
        if result is None:
            the_question_to_answer = question
            requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, teacher_chat_id,
                                                          "write @answer to answer the question you added!"))
        else:
            requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, teacher_chat_id, "question already exists!"))


def answer_add_question(answer, chat_id):
    global the_question_to_answer
    with connection.cursor() as cursor:
        query = f"SELECT * FROM QA WHERE question='{the_question_to_answer}' and chat_id={chat_id}"
        cursor.execute(query)
        result = cursor.fetchone()
        if result is None:
            lquest = [the_question_to_answer]
            keywords = get_keywords(lquest)
            query = f"INSERT INTO QA VALUES({chat_id}, '{answer}', '{the_question_to_answer}' , '{keywords}')"
            cursor.execute(query)
            connection.commit()
            requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "question added successfully!"))
    the_question_to_answer = ''


def add_announcement(announcement, class_):
    with connection.cursor() as cursor:
        query = f"SELECT chat_id FROM users WHERE role = 'parent' and class = {class_}"
        cursor.execute(query)
        result = cursor.fetchall()
        if result:
            for parent_chat_id in result:
                requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, parent_chat_id['chat_id'], announcement))


def return_answer_to_parent(parent_chat_id, answer):
    requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, parent_chat_id, "The teacher says:\n" + answer))


def remove_question(teacher_chat_id, ques):
    with connection.cursor() as cursor:
        query = f"SELECT * FROM QA where question = {ques}"
        cursor.execute(query)
        result = cursor.fetchone()
        if result is not None:
            query3 = f"DELETE FROM QA WHERE question = {ques}"
            cursor.execute(query3)
            connection.commit()
            requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, teacher_chat_id, "okay 🤗"))
