from telebot import TeleBot, types
from time import time
from random import randint

# Initialize bot with your token
bot = TeleBot("7220953758:AAH8jXqX5_YNIzuUbx_o-XIlTxyPJ9bk73I")

# Global constant for ban duration
BAN_DURATION = 1200  # 20 minutes in seconds


# Load bad words from file
def load_bad_words(filename="bad_words.txt"):
    """Loads bad words from a file and returns a set of lowercase words."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return {word.strip().lower() for word in f.readlines()}
    except FileNotFoundError:
        print(f"Error: {filename} not found. Please ensure the file exists.")
        return set()


BAD_WORDS = load_bad_words()


def is_group(message):
    """Checks if the message is from a group or supergroup."""
    return message.chat.type in ('group', 'supergroup')


@bot.message_handler(commands=["check"])
def start_check(message):
    """Starts the math check with an inline keyboard."""
    # Generate random numbers
    n1 = randint(1, 5)
    n2 = randint(1, 5)
    correct_sum = n1 + n2  # Generate the sum before assigning it to a variable

    # Create inline keyboard
    numbers = ["один", "два", "три", "четыре", "пять",
               "шесть", "семь", "восемь", "девять", "десять"]
    keyboard = types.InlineKeyboardMarkup()
    keys = [
        types.InlineKeyboardButton(text=number, callback_data=str(idx + 1))
        for idx, number in enumerate(numbers)
    ]
    keyboard.row(*keys)

    # Store the correct sum in a dictionary for this specific user and message.
    bot.current_check_sums = getattr(bot, "current_check_sums", {})  # Initialize if not existing
    bot.current_check_sums[message.message_id] = correct_sum
    bot.send_message(
        message.chat.id, f"Решите пример: {n1} + {n2} = ?", reply_markup=keyboard)



@bot.callback_query_handler(func=lambda call: call.data.isdigit())
def handle_math_check(call):
    """Handles the callback from the math check."""

    try:
        user_answer = int(call.data)
        correct_sum = bot.current_check_sums.get(call.message.message_id)

        if correct_sum is None:
           bot.edit_message_text(chat_id=call.message.chat.id,  # ID чата
                              message_id=call.message.message_id,  # ID сообщения для удаления
                              text="Проверка устарела") # Message was sent from the past


        elif user_answer == correct_sum:
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text="Проверка пройдена")

            # Remove the check from the dictionary
            del bot.current_check_sums[call.message.message_id]

        else:
            # Ban the user
            bot.ban_chat_member(call.message.chat.id, call.from_user.id)
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text="Неверный ответ, игрок заблокирован!")
           # Remove the check from the dictionary
            del bot.current_check_sums[call.message.message_id]

    except Exception as e:
         print(f"Error processing callback: {e}")
         bot.send_message(call.message.chat.id, f"An error occurred")




@bot.message_handler(func=lambda message: message.entities is not None and is_group(message))
def delete_links(message):
    """Deletes messages with URLs or text links in groups."""
    for entity in message.entities:
        if entity.type in ["url", "text_link"]:
            bot.delete_message(message.chat.id, message.message_id)


def has_bad_words(text):
    """Checks if the text contains any bad words."""
    if not text:  # Check if text is None or empty
        return False
    message_words = text.lower().split()
    for word in message_words:
        if word in BAD_WORDS:
            return True
    return False


@bot.message_handler(func=lambda message:  is_group(message) and message.text is not None and has_bad_words(message.text))
def handle_bad_words(message):
    """Handles messages with bad words in groups."""
    try:
       bot.restrict_chat_member(
           message.chat.id,
           message.from_user.id,
           until_date=time() + BAN_DURATION
       )
       bot.send_message(message.chat.id, text='Тебе бан на 20 минут',
                        reply_to_message_id=message.message_id)
       bot.delete_message(message.chat.id, message.message_id)

    except Exception as e:
        print(f"Error in handling bad words: {e}")
        bot.send_message(message.chat.id, "An error occurred while processing bad words.")



if __name__ == "__main__":
    bot.polling(non_stop=True)