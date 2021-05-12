import telebot, database
bot = telebot.TeleBot('1650114540:AAEbzTKu60P0VE97xpMUGYOQqYzfyqP0mlg')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    bot.send_message(message.from_user.id, 'Ваше сообщение обработано, спасибо.')
    print('From ' + str(message.from_user.id) + ' message "' + message.text + '"')

print(database.is_user_exists('3'))
print(database.is_user_exists('4'))

bot.polling(none_stop = True, interval = 0)
