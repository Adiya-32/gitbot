from telebot import TeleBot, types
from random import choice, randint

bot = TeleBot('7220953758:AAH8jXqX5_YNIzuUbx_o-XIlTxyPJ9bk73I')

game_choice = ['камень', 'ножницы', 'бумага']
user_points = []
bot_points = []
draw_points = []
@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_game = types.KeyboardButton('Начать игру!')
    #searth_points = types.KeyboardButton('Посмотреть счет!')
    markup.add(start_game)

    bot.send_message(message.chat.id, 'Привет, давай поиграем в игру "Камень|Ножницы|Бумага"!', reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def main(message):
    global user_points, bot_points, draw_points
    if message.text == 'Начать игру!':
        user_points.append(0), bot_points.append(0), draw_points.append(0)
        game_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        rock_button = types.KeyboardButton('Камень')
        scissors_button = types.KeyboardButton('Ножницы')
        paper_button = types.KeyboardButton('Бумага')
        game_markup.add(rock_button, scissors_button, paper_button)
        game_markup.add(types.KeyboardButton('Посмотреть счет!'), types.KeyboardButton('Завершить игру!'))
        bot.send_message(message.chat.id, 'Выберите: "Камень|Ножницы|Бумага"', reply_markup=game_markup)
    elif message.text == 'Посмотреть счет!':
            show_score(message)
    elif message.text == 'Завершить игру!':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        start_game = types.KeyboardButton('Начать игру!')
        searth_points = types.KeyboardButton('Посмотреть счет!')
        markup.add(start_game, searth_points)
        bot.send_message(message.chat.id, 'Игра завершина, счет обнулен!', reply_markup=markup)
    elif message.text.lower() in game_choice:
        play_game(message)
    else:
        bot.send_message(message.chat.id, 'Введите корректный запрос!')

def show_score(message):
    global user_points, bot_points, draw_points
    for i in range(len(user_points)):
        bot.send_message(message.chat.id, f'Раунд {i + 1}\nПользователь: {user_points[i]}\nБот: {bot_points[i]}\nНичья: {draw_points[i]}')
        #bot.send_message(message.chat.id, f'Пользователь: {user_points[i]}')
        #bot.send_message(message.chat.id, f'Бот: {bot_points[i]}')Ничья: {draw_points[i]}
        #bot.send_message(message.chat.id, f'Ничья: {draw_points[i]}')

def play_game(message):
    global user_points, bot_points, draw_points
    user_choice = message.text.lower()
    bot_choice = choice(game_choice)
    bot.send_message(message.chat.id, f'Бот выбрал: {bot_choice}!')
    if user_choice == bot_choice:
        result = 'Ничья!'
        draw_points[-1] += 1
    elif (user_choice == 'камень' and bot_choice == 'ножницы' or user_choice == 'ножницы' and bot_choice == 'бумага' or user_choice == 'бумага' and bot_choice == 'камень'):
        result = 'Вы выиграли!'
        user_points[-1] += 1
    else:
        result = 'Вы проиграли!'
        bot_points[-1] += 1
    bot.send_message(message.chat.id, result)

bot.polling(non_stop=True)