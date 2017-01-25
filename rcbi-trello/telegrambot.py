import telegram

from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters


class TelegramBot(object):

    def echo(self, text):
        self.sendingBot.sendMessage(chat_id=self.chat_id, text=text)

    def __init__(self):
        self.bot = telegram.ext.Updater(token='254583592:AAG0eINt7l8DKWFNHdF3_4Yr5iaWURVvn7s')
        self.sendingBot = telegram.Bot(token='254583592:AAG0eINt7l8DKWFNHdF3_4Yr5iaWURVvn7s')
        self.dispatcher = self.bot.dispatcher
        self.chat_id = '@rcbinotify'


        #status_handler = CommandHandler('status', status)
        #dispatcher.add_handler(status_handler)

        #echo_handler = MessageHandler([Filters.text], echo)
        #dispatcher.add_handler(echo_handler)
        #self.echo('asdasd')
        #self.bot.start_polling()


t = TelegramBot()
