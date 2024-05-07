from telebot.types import Message
from config_data.config import DEFAULT_COMMANDS
from postgre.db_config import host, user, password, db_name
from loader import bot
import psycopg2 

@bot.message_handler(commands=["add"])
def get_task(message: Message):
    msg = bot.send_message(message.chat.id, 'Введите задание: ')
    bot.register_next_step_handler(msg, insert_in_db)

def insert_in_db(message: Message):
    customer = str(message.from_user.id)
    task = message.text
    if task != '/start' and task != '/tsk' and task != '/add':
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
                    """SELECT * FROM users_tasks WHERE user_id = %s;""",
                    (customer,)
                )
                existing_user = cursor.fetchone()
                if existing_user:
                    cursor.execute(
                        """UPDATE users_tasks 
                        SET task = CONCAT_WS(',', COALESCE(task, ''), %s) 
                        WHERE user_id = %s;""",
                        (task, customer)
                    )
                    bot.send_message(message.chat.id, f'Задание добавлено!')
                else:
                    cursor.execute(
                        """INSERT INTO users_tasks (user_id, task) VALUES (%s, %s);""",
                        (customer, task)
                    )
                    bot.send_message(message.chat.id, f'Задание добавлено!')

        except Exception as error:
            print('Не удалось подключиться к БД.', error)
        finally:
            if connection:
                connection.close()
                print('Соединение с БД закрыто.')
    else:
        get_task(message)
