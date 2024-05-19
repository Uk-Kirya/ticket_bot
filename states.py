from telebot.handler_backends import State, StatesGroup


class States(StatesGroup):
    """
    Состояния.
    1 — Ввод города вылета
    3 — Ввод города прилета
    4 — Ввод даты перелета
    """
    departure_city = State()
    arrival_city = State()
    flight_date = State()
