 # Задатки телеграм-бота
import telebot
from telebot import types
import telebot
from telebot import apihelper
import database

#token = '1650114540:AAEbzTKu60P0VE97xpMUGYOQqYzfyqP0mlg'
token='1454331124:AAGK-3FCOuKxD2USul1kaAKC_etS4cTOxiQ'

bot = telebot.TeleBot(token)
bot.delete_webhook()

@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('Зарегестрироваться')
    bot.send_message(message.chat.id, 'Привет!\n Это бот для знакомств. Здесь вы сможете найти свою вторую половинку!', reply_markup=keyboard)

@bot.message_handler(commands=['menu'])
def main_menu(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('Смотреть анкеты','Изменить данные','удалить аккаунт')
    bot.send_message(message.chat.id, 'Главное меню:\n 1.Продлжить смотреть анкеты\n 2.Изменить данные\n 3.Удалить аккаунт', reply_markup=keyboard)

def get_text_messages(message):
    bot.send_message(message.from_user.id, "Как тебя зовут?")
    bot.register_next_step_handler(message, get_name)

name = None
def get_name(message):
    global name
    name = message.text
    bot.send_message(message.from_user.id, "Сколько тебе лет?",reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, get_age)


age = None
def get_age(message):
    global age
    try:
        age = int(message.text)
        if (age<0) or (age>100):
            bot.send_message(message.chat.id, 'Некорректный ввод,повторите попытку')
        else:
            keyboard = telebot.types.ReplyKeyboardMarkup(True)
            keyboard.row('Мужчина', 'Женщина')
            bot.send_message(message.chat.id, 'Вы мужчина или женщина?', reply_markup=keyboard)
            bot.register_next_step_handler(message, get_sex)
    except:
        bot.send_message(message.chat.id, 'Некорректный ввод,повторите попытку')
        bot.send_message(message.chat.id, 'Сколько Вам лет?')
        bot.register_next_step_handler(message, get_age)


sex = None
def get_sex(message):
    global sex
    sex_1 = message.text
    if (sex_1=='Мужчина'):
        sex='m'
    else:
        sex='f'
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('Мужчину', 'Женщину', 'Не важно')
    bot.send_message(message.chat.id, 'Кого вы ищите?', reply_markup=keyboard)
    bot.register_next_step_handler(message, partner_sex)

k = 0
partner_sex = None
def partner_sex(message):
    global partner_sex
    partner_sex_1 = message.text
    if (partner_sex_1=='Мужчину'):
        partner_sex='m'
    elif (partner_sex_1=='Женщину'):
        partner_sex='f'
    else:
        partner_sex = 'any'
    if (k == 0):
        bot.send_message(message.chat.id, 'Регистрация прошла успешно', reply_markup=types.ReplyKeyboardRemove())
        try:
            database.create_user(message.from_user.id, name, age, sex, partner_sex)
        except:
            pass
        #bot.register_next_step_handler(message, main_menu)
        main_menu(message)
    else:
        bot.send_message(message.chat.id, 'Данные успешно обновлены!', reply_markup=types.ReplyKeyboardRemove())
        database.update_userdata(message.from_user.id, name, age, sex, partner_sex)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'зарегестрироваться':
        get_text_messages(message)
        k = 0
    elif message.text.lower() == 'удалить аккаунт':
        bot.send_message(message.chat.id, 'Надеюсь, мы помогли вам найти и познакомится с новыми людьми!\nВаш аккаунт удален!')
        database.delete_user(message.from_user.id)
    elif message.text.lower() == 'изменить данные':
        get_text_messages(message)
        k = 1
    elif message.text.lower() == 'смотреть анкеты':
        partner_anketa = database.get_partner(message.from_user.id)
        database.read_userdata(message.from_user.id,partner_anketa)


bot.polling(none_stop = True, interval = 0)