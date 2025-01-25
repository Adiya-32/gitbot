import json
from telebot import TeleBot, types
import requests
from io import BytesIO
from time import sleep
bot = TeleBot('7620076493:AAFGWwpCgS9rUqGp2hkbAI-euATWA3OYjgw')

gme = False
index = 0
points = 0

with open('victorina.json', 'r', encoding='utf-8') as file:
    data = json.load(file)


def get_next_question(data, index):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton(f"1) {data[index]['вариант'][0]}"), types.KeyboardButton(f"2) {data[index]['вариант'][1]}"))
    markup.row(types.KeyboardButton(f"3) {data[index]['вариант'][2]}"), types.KeyboardButton(f"4) {data[index]['вариант'][3]}"))
    markup.row(types.KeyboardButton('Посмотреть счет'), types.KeyboardButton('Завершить игру'))
    return markup
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start = types.KeyboardButton('Начать игру')
    markup.add(start)
    return markup

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = main_menu()
    bot.send_message(message.chat.id, 'Добро пожаловать в игру "Викторина"!', reply_markup=markup)

@bot.message_handler(commands=['quezz'])
def quizz(message):
    global game, index
    game = True
    markup = get_next_question(data, index)
    if 'image' in data[index]:
        img_url = data[index]['image']
        responce = requests.get(img_url)
        img = BytesIO(responce.content)
        bot.send_photo(message.chat.id, img)

    question_text = f'{index + 1}) {data[index]["вопрос"]}'
    bot.send_message(message.chat.id, text=question_text, reply_markup=markup)

@bot.message_handler()
def victorinas(message):
    global game, index, points
    if message.text == 'Начать игру':
        index = 0
        points = 0
        quizz(message)
    elif message.text == 'Посмотреть счет':
        bot.send_message(message.chat.id, text = f'Набрано очков: {points}')
    elif message.text == 'Завершить игру':
        bot.send_message(message.chat.id, text='Игра завершена! Все данные обнулены!')
        points = 0
        game = False
        markup = main_menu()
        sleep(3)
        bot.send_message(message.chat.id, 'Возвращаемся в главное меню', reply_markup=markup)
    elif game:
        user_answer = message.text.split(') ')[-1]
        if user_answer == data[index]['ответ']:
            bot.send_message(message.chat.id, 'Правильно!')
            points += 1
        else:
            bot.send_message(message.chat.id, f'Неправильно! Правильный ответ: {data[index]["ответ"]}')
        index += 1
        if index < len(data):
            markup = get_next_question(data, index)
            if 'image' in data[index]:
                img_url = data[index]['image']
                responce = requests.get(img_url)
                img = BytesIO(responce.content)
                bot.send_photo(message.chat.id, img)

            question_text = f'{index + 1}) {data[index]["вопрос"]}'
            bot.send_message(message.chat.id, text=question_text, reply_markup=markup) 

        else:
            bot.send_message(message.chat.id, 'Викторина завершена! ВЫ ответили на все вопросы!')
            bot.send_message(message.chat.id, text =f'Набрано очков: {points}')
            game = False
            markup = main_menu()
            sleep(3)
            bot.send_message(message.chat.id, 'Возвращаемся в главное меню', reply_markup=markup)
            
bot.polling(non_stop=True)