from telebot import TeleBot, types
bot = TeleBot('7620076493:AAFGWwpCgS9rUqGp2hkbAI-euATWA3OYjgw')

user_modes = {}

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Калькулятор')
    markup.add(btn1)
    bot.send_message(message.chat.id, 'Привет, чем могу помочь?', reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def main(message):
    chat_id = message.chat.id
    if message.text.lower() == 'калькулятор':
        user_modes[chat_id] = 'калькулятор'
        bot.send_message(message.chat.id, 'режим калькулятор включен')
    else:
        mode = user_modes.get(chat_id, None)
        if mode == 'калькулятор':
            calculator(message)
def calculator(message):
    try:
        result = eval(message.text)
        bot.send_message(message.chat.id, f'Результат: {result}')
    except:
        bot.send_message(message.chat.id, 'Ошибкаб повторите попытку!')

bot.polling(non_stop=True)