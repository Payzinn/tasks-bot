from telebot.types import Message
from config_data.config import DEFAULT_COMMANDS
from loader import bot
from postgre.db_config import host, user, password, db_name
import psycopg2
import re

@bot.message_handler(commands=['tsk'])
def task_print(message: Message):
    customer = str(message.from_user.id)
    print('Вхождение в функцию task_print')
    bot.send_message(message.chat.id, 'Вывод заданий:')
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT task FROM users_tasks WHERE user_id = %s;""",(customer,)
            )
            tasks = cursor.fetchall()
            if tasks:
                tasks_list = ", ".join([task[0] for task in tasks])
                pattern = r',\s*([^,]+)'
                result = re.findall(pattern, tasks_list)
                print(result)
                full_result = "\n".join([f"{index + 1}. {task}" for index, task in enumerate(result)])
                bot.send_message(message.chat.id, f'Вот список ваших заданий:\n{full_result}')
            else:
                bot.send_message(message.chat.id, 'У вас пока нет заданий.')
        
    except Exception as error:
        print('Не удалось подключиться к БД.', error)
    finally:
        if connection:
            connection.close()
            print('Соединение с БД закрыто.')