import telebot
import re
from telebot.types import BotCommand, Message
from telebot import custom_filters
from telebot.storage import StateMemoryStorage
from peewee import IntegrityError
from models import User, create_models
from config import BOT_TOKEN, greeting, DEFAULT_COMMANDS
from states import States
from api import cities, ticket

state_storage = StateMemoryStorage()
bot = telebot.TeleBot(BOT_TOKEN, state_storage=state_storage)


@bot.message_handler(commands=['start'])
def start(message: Message) -> None:
    """
    Сюда пользователь попадает, как только открывает бота и начинает с ним взаимодействовать (после выполнения команды /start)
    Сразу создается модель пользователя и он попадает в список, в базу данных, куда сохраняются его данные
    Пользователь вводит сообщение «Город вылета» и переносится на следующий шаг
    :return: Message : str
    """
    user_id: int = message.from_user.id
    username: str = message.from_user.username
    first_name: str = message.from_user.first_name
    last_name: str = message.from_user.last_name

    try:
        User.create(
            user_id=user_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        bot.send_message(
            message.chat.id,
            '{hello}, {name} 👋🏻\n\nЯ найду самые дешевые авиабилеты 🎫️\n\nНапишите город вылета 🛫'.format(
                hello=greeting,
                name=first_name
            )
        )
        bot.set_state(message.from_user.id, States.departure_city, message.chat.id)
    except IntegrityError:
        bot.reply_to(message,
                     f"{greeting}, {first_name}! Я снова к Вашим услугам 🫡\n\nДавайте поищем билет\n\nНапишите город вылета 🛫")
        bot.set_state(message.from_user.id, States.departure_city, message.chat.id)


@bot.message_handler(state=States.departure_city)
def departure_city(message: Message) -> None:
    """
    Проверяем, есть ли сообщение (город), переданное предыдущим шагом, в списке городов, полученных от api.py -> cities()
    Если города нет, уведомляем об этом пользователя и просим ввести город заново.
    Далее, пользователь вводит сообщение «Город прибытия» и переносится на следующий шаг
    :return: Message : str
    """
    message.text = message.text.title()

    if message.text == "/start":
        start(message)
        return

    if message.text == "/about":
        about_bot(message)
        bot.send_message(message.chat.id, 'Для продолжения поиска, введите город вылета 🛫')
        return

    if message.text == "/help":
        help_information(message)
        bot.send_message(message.chat.id, 'Для продолжения поиска, введите город вылета 🛫')
        return

    if message.text not in cities()[0]:
        bot.send_message(message.chat.id, 'Я не нашел город «{city}» 😱 Попробуйте еще раз!'.format(city=message.text))
        return

    bot.send_message(message.chat.id, 'Теперь город прибытия 🛬')
    bot.set_state(message.from_user.id, States.arrival_city)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        index_of_city_code = cities()[0].index(message.text)
        data['departure_city'] = message.text
        data['departure_city_code'] = cities()[1][index_of_city_code]


@bot.message_handler(state=States.arrival_city)
def arrival_city(message: Message) -> None:
    """
    Проверяем, есть ли сообщение (город), переданное предыдущим шагом, в списке городов, полученных от api.py -> cities()
    Если города нет, уведомляем об этом пользователя и просим ввести город заново.
    Далее, пользователь вводит сообщение «Дату перелета» и переносится на следующий шаг
    :return: Message : str
    """
    message.text = message.text.title()

    if message.text == "/start":
        start(message)
        return

    if message.text == "/about":
        about_bot(message)
        bot.send_message(message.chat.id, 'Для продолжения поиска, введите город прибытия 🛬')
        return

    if message.text == "/help":
        help_information(message)
        bot.send_message(message.chat.id, 'Для продолжения поиска, введите город прибытия 🛬')
        return

    if message.text not in cities()[0]:
        bot.send_message(message.chat.id, 'Я не нашел город «{city}» 😱 Попробуйте еще раз!'.format(city=message.text))
        return

    bot.send_message(message.chat.id, 'А теперь введите дату вылета 🗓 (дд.мм.гггг)')
    bot.set_state(message.from_user.id, States.flight_date)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        index_of_city_code = cities()[0].index(message.text)
        data['arrival_city'] = message.text
        data['arrival_city_code'] = cities()[1][index_of_city_code]


@bot.message_handler(state=States.flight_date)
def flight_date(message: Message) -> None:
    """
    Финальный шаг, на котором мы показываем пользователю билет с выбранными им данными
    Если пользователь пожелает, он может начать поиск заново, просто введя город отправления
    :return: Message : str
    """
    if message.text == "/start":
        start(message)
        return

    if message.text == "/about":
        about_bot(message)
        bot.send_message(message.chat.id, 'Для продолжения поиска, введите дату вылета 🗓️ (дд.мм.гггг)')
        return

    if message.text == "/help":
        help_information(message)
        bot.send_message(message.chat.id, 'Для продолжения поиска, введите дату вылета 🗓️ (дд.мм.гггг)')
        return

    date_mask = re.findall(r'(\d{2}).(\d{2}).(\d{4})', message.text)

    if not date_mask:
        bot.send_message(message.chat.id, 'Вы ввели некорректную дату. Пожалуйста, введите цифры (дд.мм.гггг)')
        return

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:

        departure_city_code_str = str(data['departure_city_code'])
        arrival_city_code_str = str(data['arrival_city_code'])

        msg = ticket(departure_city_code_str, arrival_city_code_str, message.text)
        bot.send_message(message.chat.id, f'🛫 {data['departure_city']} — 🛬 {data['arrival_city']}\n\n🗓 {message.text}\n\n{msg}')

    bot.delete_state(message.from_user.id, message.chat.id)
    bot.send_message(message.chat.id, 'Для нового поиска авиабилета, напишите /start 😀')


@bot.message_handler(commands=['about'])
def about_bot(message: Message) -> None:
    bot.send_message(
        message.chat.id,
        'Познакомимся поближе 🤗\n\nЯ бот, который помогает найти самый дешевый авиабилет в два клика\n\nДостаточно '
        'просто указать откуда, куда и когда Вы хотите прилететь и я подберу Вам самый дешевый билет'
    )


@bot.message_handler(commands=['help'])
def help_information(message: Message) -> None:
    bot.send_message(
        message.chat.id,
        'Данный бот работает довольно просто:\n\n1️⃣ — Вводите город вылета\n2️⃣ — Вводите город прибытия\n3️⃣ — '
        'Указываете дату перелета\n4️⃣ — Бот показывает самый дешевый авиабилет\n5️⃣ — В информации о билете будет '
        'ссылка для покупки авиабилета'
    )


if __name__ == "__main__":
    create_models()
    bot.add_custom_filter(custom_filters.StateFilter(bot))
    bot.set_my_commands([BotCommand(*cmd) for cmd in DEFAULT_COMMANDS])
    bot.infinity_polling()
