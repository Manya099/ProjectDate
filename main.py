import telebot, database
from telebot.apihelper import send_photo
bot = telebot.TeleBot('1650114540:AAEbzTKu60P0VE97xpMUGYOQqYzfyqP0mlg')
bot.delete_webhook()

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    bot.send_message(message.from_user.id, 'Ваше сообщение обработано, спасибо.')
    print('From ' + str(message.from_user.id) + ' message "' + message.text + '"')
    bot.send_photo(message.from_user.id, 'AgACAgIAAxkBAAIBDWCo46zFg0uONMmE_lgsT1hAmRMHAAKUszEbpCxJSZQavgl64jg5Q3gUpC4AAwEAAwIAA20AA2tqAQABHwQ')

bot.polling(none_stop = True, interval = 0)
