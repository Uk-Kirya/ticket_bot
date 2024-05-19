##  Телеграм бот для поиска дешевых авиабилетов

Благодаря этому боту, можно найти самые дешевые авиабилеты на сервисе Aviasales

**Технологии, используемые при написании бота**

 - Python (основной язык программирования)
 - api (для работы с API)
 - certifi (для работы с SSL сертификатами)
 - charset-normalizer (для нормализации кодировки)
 - env (для работы с окружением)
 - idna (для работы с интернационализированными доменными именами)
 - nose (для тестирования)
 - peewee (для работы с базами данных)
 - pyTelegramBotAPI (для работы с API Telegram)
 - python-dotenv (для работы с переменными окружения)
 - requests (для отправки HTTP запросов)
 - stateful-object (для работы с объектами состояния)
 - telebot (для работы с API Telegram)
 - Unidecode (для транслитерации Unicode строк)
 - urllib3 (для работы с URL)


**Функции бота**
 - /start - начало поиска билета
 - /help - справочная информация
 - /about - информация о боте


**Принцип работы бота**

1. При первом запуске бота, выводится приветствие и идет запись пользователя в базу для дальнейшей с ним работы, например, каждый раз по-разному его приветствовать
2. Далее предлагается сразу, не «отходя от кассы», ввести город вылета
3. После, вводится город прибытия
4. Далее, вводится дата перелета в формате дд.мм.гггг
5. Ну и финалочка: вывод авиабилета с ценой, городами вылета и прибытия и датой. Ниже будет ссылка, перейдя по которой, можно оформить билет

## Первый запуск

 1. Установите все необходимые библиотеки - `pip install -r requirements.txt`
 2. Создайте файл `.env` по шаблону `.env.example` и впишите все данные (API/TOKEN)
 3. Запустите бота - `python3 main.py` 

**Количество запросов на сайте не ограничено!**

## Версия Python
Бот написан с использованием Python версии `3.12`