from config import connection, TOKEN, TELEGRAM_SEND_MESSAGE_URL
import requests
from keywords import get_keywords


def ask_question(question, chat_id, class_):
    first_question = question
    similar_questions = []
    with connection.cursor() as cursor:
        question = "'" + question + "'"
        lquestion = [question]
        keywords = get_keywords(lquestion)
        query = f"SELECT * FROM QA"
        cursor.execute(query)
        res = cursor.fetchall()
        split_keywords = keywords.split()
        for result in res:
            db_keywords = result['keywords'].split()
            for key in split_keywords:
                if key in db_keywords:
                    similar_questions.append(result['question'])
                    break
        if len(similar_questions) != 0:
            requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "It seems we have similar questions:\n"
                                                                          "Write  %<number>"
                                                                          "  to choose the question you want\n"))
            for i, question in enumerate(similar_questions):
                requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, str(i) + ")" + " " + question + "\n"))
            requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "If you can't find your question, write 'none'"))
        else:
            requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "No similar questions were asked,"
                                                                          " we will send your question to the teacher. Please wait for the answer.\n"))
            query = f"INSERT INTO parentsQuestions VALUES({chat_id},'{first_question}')"
            cursor.execute(query)
            ask_question2(first_question, class_)
        connection.commit()
    return chat_id, first_question, similar_questions



def ask_question2(question, class_):
    with connection.cursor() as cursor:
        query = f"SELECT * FROM users WHERE job = 'main teacher' and class = {class_}"
        cursor.execute(query)
        res = cursor.fetchone()
        if res is not None:
            requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, res['chat_id'], "You have a new question:\n" +
                                                          question + "\nStart your answer with @ans"))
        else:
            query = f"SELECT * FROM users WHERE job = 'teacher' and class = {class_}"
            cursor.execute(query)
            res = cursor.fetchone()
            if res is not None:
                requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, res['chat_id'], "You have a new question:\n" +
                                                              question + "\nStart your answer with @ans"))
