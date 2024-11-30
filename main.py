import telebot
from telebot import types

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


StartMessage = "👋 Привет! Я твой бот-помошник!"
HelpMessage = "Моя задача - поиск того самого кода, который тебе нужен сию минуту!"
SearchMessage = "Введите ваш запрос после команды /search!"
startMessages =['start', '/start']
helpMessages =['start', '/start']
searchMessages =['start', '/start']

bot = telebot.TeleBot('7719455155:AAE8o8em0OoOD35QBXUfonVSBIkUzXGnjMY')

user_last_request_time = {}

@bot.message_handler(commands=['start'])#start
def start(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn2 = types.KeyboardButton("/help")
    btn3 = types.KeyboardButton("/search")
    markup.add(btn2)
    markup.add(btn3)
    bot.send_message(message.from_user.id, StartMessage, reply_markup=markup)

@bot.message_handler(commands=['help'])#start
def help(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    ##btn1 = types.KeyboardButton("/start")
    btn3 = types.KeyboardButton("/search")
   # markup.add(btn1)
    markup.add(btn3)
    bot.send_message(message.from_user.id, HelpMessage, reply_markup=markup)

@bot.message_handler(commands=['search'])#start
def search(message):
    if(message.text == '/search'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        #btn1 = types.KeyboardButton("/start")
        btn3 = types.KeyboardButton("/help")
       # markup.add(btn1)
        markup.add(btn3)
        bot.send_message(message.from_user.id, SearchMessage, reply_markup=markup)
        print(message.text)
    else:
        markup = None
        Text2Search = message.text.replace("/search", "")
        MainSearch(message, Text2Search)
        #bot.send_message(message.from_user.id, Text2Search, reply_markup=markup) #Отлов запроса


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if(message):
        Text2Search = message.text.replace("/search", "")
        MainSearch(message, Text2Search, )
        #bot.send_message(message.from_user.id, "Я понимаю только язык команд, пиши командами", reply_markup=markup)


def MainSearch(message,T2S):
    options = Options()
    ua = UserAgent()
    user_agent = ua.random
    print(user_agent)
    options.add_argument(f'--user-agent={user_agent}')
    options.add_argument('--ignore-certificate-errors-spki-list')
    chromeService = webdriver.ChromeService(chrome_options=options, executable_path=r"C:\chromedriver-win64\chromedriver.exe")
    browser = webdriver.Chrome(service = chromeService)
    '''try:'''
    browser.get('https://habr.com/ru/search/')
    time.sleep(3)
    # регистрируем кнопку "Поиск" и имитируем нажатие
    open_search = browser.find_element("class name", "tm-search__input.tm-input-text-decorated__input")
    #open_search = browser.find_element('navbar_search', by=id )
    open_search.click()
    # регистрируем текстовое поле и имитируем ввод строки "Git"
    #search = browser.find_element("input-491" ,by=id)
    open_search.send_keys(T2S + Keys.RETURN)

    time.sleep(1)
    # загружаем страницу и извлекаем ссылки через атрибут rel
    soup = BeautifulSoup(browser.page_source, 'lxml')
    all_publications = \
    soup.find_all('a', {'class': 'tm-title__link'})[1:10]
    # форматируем результат
    TXTOUT = []
    for article in all_publications:
        print(article['href'])
        title = article.get_text()
        link = article['href']
        TXTOUT.append(f'{title}\nСсылка: {"https://habr.com"+link}\n\n')
        print("".join(TXTOUT))
        #message.reply_text(f'{title}\nСсылка: {link}')
    bot.send_message(message.from_user.id, "".join(TXTOUT))
    browser.close()
    '''except:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton(T2S)
        markup.add(btn)
        bot.send_message(message.from_user.id, f'Что-то пошло не так', reply_markup=markup)
        browser.close()
        return'''
bot.polling(none_stop=True, interval=0) #обязательная для работы бота часть