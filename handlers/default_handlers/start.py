from telebot.types import Message
from config_data.config import DEFAULT_COMMANDS
from postgre.db_config import host, user, password, db_name
from loader import bot
import psycopg2 


@bot.message_handler(commands=["start"])
def welcome(message: Message):
    print('Вхождение в /start')

    customer = str(message.from_user.id)
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
            if not existing_user:
                cursor.execute(
                    """INSERT INTO users_tasks (user_id) VALUES (%s);""",
                    (customer,)
                )
        
    except Exception as error:
        print('Не удалось подключиться к БД.', error)
    finally:
        if connection:
            connection.close()
            print('Соединение с БД закрыто.')

    text = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]
    bot.send_message(message.chat.id, f'Привет {message.from_user.username}, я бот .\nВот список команд.')
    bot.send_message(message.chat.id, "\n".join(text))
    print(f'id пользователя: {customer}')
