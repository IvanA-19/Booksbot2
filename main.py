from bot import bot
from background import keep_alive


def main():
    bot.polling(non_stop=True)


if __name__ == '__main__':
    keep_alive()
    main()
