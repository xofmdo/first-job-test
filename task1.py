import random
from typing import List, Dict

import math

TIMESTAMPS_COUNT = 50000

PROBABILITY_SCORE_CHANGED = 0.0001

PROBABILITY_HOME_SCORE = 0.45

OFFSET_MAX_STEP = 3

INITIAL_STAMP = {
    "offset": 0,
    "score": {
        "home": 0,
        "away": 0
    }
}


def generate_stamp(previous_value):
    score_changed = random.random() > 1 - PROBABILITY_SCORE_CHANGED
    home_score_change = 1 if score_changed and random.random() > 1 - \
                             PROBABILITY_HOME_SCORE else 0
    away_score_change = 1 if score_changed and not home_score_change else 0
    offset_change = math.floor(random.random() * OFFSET_MAX_STEP) + 1

    return {
        "offset": previous_value["offset"] + offset_change,
        "score": {
            "home": previous_value["score"]["home"] + home_score_change,
            "away": previous_value["score"]["away"] + away_score_change
        }
    }


def generate_game():
    stamps = [INITIAL_STAMP, ]
    current_stamp = INITIAL_STAMP
    for _ in range(TIMESTAMPS_COUNT):
        current_stamp = generate_stamp(current_stamp)
        stamps.append(current_stamp)

    return stamps


game_stamps = generate_game()

# pprint(game_stamps)


def binary_search(lst: List[Dict], search_item: int) -> False or int:
    """
    Функция бинарного поиска нужного нам элемента.

    :param lst: список со словарями.
    :param search_item: искомая минута
    :return:
    1) False, если для такой минуты нет результата
    2) Int - искомый элемент в списке
    """

    # Для ускорения бинарного поиска при запросе ближайших минут можно
    # посчитать логарифм от количества элементов
    # degree = math.ceil(math.log2(TIMESTAMPS_COUNT))
    # и на последнем проходе запоминать значение middle, чтобы потом начинать
    # поиск с данного элемента
    low = 0
    high = len(lst) - 1

    while low <= high:
        middle: int = (low + high) // 2
        guess: int = lst[middle]['offset']
        if guess == search_item:
            return middle
        if guess > search_item:
            high = middle - 1
        else:
            low = middle + 1
    return False


def search_nearest_minute(search_element: int) -> int or False:
    """
    Дополнительный поиск ответа, если искомой минуты нет в наших данных.

    :param search_element: искомый элемент.
    :return: ближайшую минуту для ответа.
    """
    # по текущим условиям у нас не может быть соседней минуты не из
    # этого списка
    if search_element == 1:
        return False
    add_list = [
        search_element-1, search_element+1,
        search_element-2, search_element+2
    ]
    for time in add_list:
        result_elem = binary_search(game_stamps, time)
        if result_elem:
            return result_elem
    return False


def find_result(
        lst: List[Dict],
        search_number: int,
        text='Наша минута найдена') -> (int, int):
    """
    Функция выдачи ответа.

    :param text: Переменная может показывать нашли мы искомый элемент или
    ближайший, но так как в задании нужно вернуть только home и away,
    то переменная текст не выводится.
    :param lst: список со словарями.
    :param search_number: искомый или ближайший к нему элемент.
    :return: значение для ключей home и away
    """
    home: int = lst[search_number]['score']['home']
    away: int = lst[search_number]['score']['away']
    return home, away


def get_score(game_stamps: List[Dict], offset: int) -> tuple or str:
    """
        Takes list of game's stamps and time offset for which returns the scores for the home and away teams.
        Please pay attention to that for some offsets the game_stamps list may not contain scores.
    """
    if isinstance(offset, float | str) or offset < 0:
        raise ValueError
    if len(game_stamps) < 1:
        raise ValueError
    if game_stamps[0].get('offset') is None:
        raise ValueError
    if game_stamps[0]['score'].get('home') is None:
        raise ValueError
    if game_stamps[0]['score'].get('away') is None:
        raise ValueError

    result = binary_search(game_stamps, offset)
    if result:
        return find_result(game_stamps, result)

    if not result:
        # если offset не найдено в нашем списке, то поищем ближайшие минуты
        additional_search = search_nearest_minute(offset)
        if additional_search:
            return find_result(
                game_stamps,
                additional_search,
                text='нашли ближайшую минуту'
            )
        else:
            return f'Такой минуты нет в нашем списке'
