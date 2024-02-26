import os
import wikipedia

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv

#Язык по умолчанию для поиска в wikipedia
wikipedia.set_lang("ru")
#Настройка безопасности для токена
load_dotenv()
secret_token = os.getenv('TOKEN')

#Функция которая пишет приветствие про запуске бота командой /start
def start(update, context):
    user_name = update.message.from_user.first_name
    update.message.reply_text(f'Привет {user_name}, я бот который ищет информацию в wikipedia, задай мне вопрос и я тебе найду все, что тебе надо. \n\n Если Вы хотите узнать как я работаю, введите команду /help.')

#Функция которая объясняет, что может бот командой /help
def help_bot(update, context):
    message = 'Данный бот помогает найти информацию в wikipedia\n\n Вы можете написать любой текст и бот вам найдет информацию которая будет включать краткое содержание и ссылку на запрашиваемую информацию\n\n На данный момент есть несколько команд:\n\n /start - Начать диалог с ботом;\n\n /help - информацию по пользованию бота wiki4sber.'
    update.message.reply_text(message)

#Функция которая обрабатывает сообщения
def search_wikipedia(update, context):
    search_query = update.message.text
    try:
        page = wikipedia.page(search_query)
        summary = wikipedia.summary(search_query, sentences=3)
        reply_message = f"🟢 {page.title}\n\n{summary}\n\n[Ссылка на статью]({page.url})"
    except wikipedia.exceptions.PageError:
        reply_message = "🔴 По вашему запросу в wikipedia ничего не найдено."
    
    update.message.reply_markdown(reply_message)
#Запуск программы
def main():
    updater = Updater(token=secret_token)

    dispatcher = updater.dispatcher.add_handler

    dispatcher(CommandHandler("start", start))
    dispatcher(CommandHandler("help", help_bot))
    dispatcher(MessageHandler(Filters.text & ~Filters.command, search_wikipedia))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
