import telebot
import requests
import json

bot = telebot.TeleBot('7620076493:AAFGWwpCgS9rUqGp2hkbAI-euATWA3OYjgw')

api = '51ab1a6c2739a19c24ef957574176b30'

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, я бот который показывает погоду! Назови свой город:')

@bot.message_handler(content_types='text')
def get_weather(message):  
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api}&units=metric&lang=ru')
    if res.status_code == 200:
        data = json.loads(res.text)
        temp = data["main"]["temp"]
        weather_description = data["weather"][0]["description"]
        bot.send_message(message.chat.id, f' Сейчас в городе {city}: {temp}°С. Погода: {weather_description}')

        if weather_description.find('снег') != -1:
            image_url = 'https://avatars.mds.yandex.net/i?id=94709bb247860427d6917c58a96c34fbd38517a1d3c2e47f-8556780-images-thumbs&n=13'
        elif weather_description.find('дожд') != -1:
            image_url = 'https://avatars.mds.yandex.net/i?id=52ba649c6c771f3d90f4d2d1a69926c767d0f40d-6307799-images-thumbs&n=13'
        elif weather_description.find('туман') != -1:
            image_url = 'https://avatars.mds.yandex.net/i?id=aec012d1a94a77a77fd29d0a5e4d5eba164ea84c-8549420-images-thumbs&n=13'
        elif weather_description.find('облач') != -1:
            image_url = 'https://avatars.mds.yandex.net/i?id=076943b2e9da305f30205f4021b1e482c5d8875d-4034258-images-thumbs&n=13'
        elif weather_description.find('пасмурн') != -1:
            image_url = 'https://avatars.mds.yandex.net/i?id=692509838e39cc72215d231838d439d91a4a23cb-5859751-images-thumbs&n=13'
        elif weather_description.find('ясн') != -1:
            image_url = 'https://avatars.mds.yandex.net/i?id=68d8f3f934eb0eb188118ed3b3568a6d4d2ba30d-9598634-images-thumbs&n=13'
        else:
            image_url = 'https://avatars.mds.yandex.net/i?id=2a0000017a160c125fbb26f3f0f6e8f918b8-4567411-images-thumbs&n=13'

        bot.send_photo(message.chat.id, image_url)

    else:
        bot.send_message(message.chat.id, 'Город не найден повторите попытку!')

bot.polling(non_stop=True)