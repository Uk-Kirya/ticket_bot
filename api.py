import requests
import json
from typing import Any
from config import AVIASALES_TOKEN


def cities() -> tuple[list[Any], list[Any]]:
    """
    Функция, которая запрашивает список городов по API get запросу и формирует их в список
    :return: city_list : str
    """
    result = requests.get('https://api.travelpayouts.com/data/ru/cities.json')
    city_list_name = [i["name"] for i in json.loads(result.text)]
    city_list_code = [i["code"] for i in json.loads(result.text)]
    return city_list_name, city_list_code


def ticket(departure_city, arrival_city, date):
    day = date[:2]
    month = date[3:5]
    year = date[6:]

    date = year + '-' + month + '-' + day

    querystring = {
        "origin": departure_city,
        "destination": arrival_city,
        "departure_at": date,
        "unique": "false",
        "limit": "1",
    }

    url = "https://api.travelpayouts.com/aviasales/v3/prices_for_dates"
    headers = {'x-access-token': AVIASALES_TOKEN}
    response = requests.request("GET", url, headers=headers, params=querystring)
    result = json.loads(response.text)['data']
    return f'💰Стоимость билета: {result[0]['price']:,} руб.\n\n🎫 Ссылка для покупки билета: https://aviasales.ru{result[0]['link']}'.replace(',', ' ')
