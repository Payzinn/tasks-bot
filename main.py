from loader import bot
from utils.set_bot_commands import set_default_commands
from handlers.default_handlers import start
from handlers.default_handlers import tsk
from handlers.default_handlers import add

if __name__ == "__main__":
    set_default_commands(bot)
    bot.infinity_polling()