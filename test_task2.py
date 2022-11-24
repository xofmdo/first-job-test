import unittest

from task1 import (
    binary_search, find_result, search_nearest_minute, get_score
)

LIST_WITH_DICT = [
    {'offset': x, 'score': {'home': 0, 'away': 0}
     } for x in range(10)
]

WRONG_KEY_IN_LIST_WITH_DICT = [
    {'ofset': x, 'score': {'home': 0, 'away': 0}
     } for x in range(10)
]


class TestBinarySearch(unittest.TestCase):

    def test_not_found_element(self):

        call = binary_search(LIST_WITH_DICT, 24)
        self.assertEqual(
            call, False, 'Функция binary_search() работает неправильно'
        )

    def test_found_element(self):
        number = 8
        call = binary_search(LIST_WITH_DICT, number)
        self.assertEqual(
            call, number, 'Функция binary_search() работает неправильно'
        )


class TestSearchNearestMinute(unittest.TestCase):

    def test_small_element(self):
        call = search_nearest_minute(1)
        self.assertEqual(
            call, False, 'Функция search_nearest_minute() работает неправильно'
        )

    def test_right_element(self):
        call = search_nearest_minute(3)
        self.assertIsInstance(
            call, int, 'Функция search_nearest_minute() работает неправильно'
        )


class TestGetScore(unittest.TestCase):

    def test_wrong_key_in_dict(self):
        with self.assertRaises(
                ValueError,
                msg='Функция должна вызывать исключение ValueError'):
            get_score(WRONG_KEY_IN_LIST_WITH_DICT, 1)

    def test_wrong_searching_element(self):
        with self.assertRaises(
                ValueError,
                msg='Функция должна вызывать исключение ValueError'):
            get_score(LIST_WITH_DICT, -1)

    def test_str_searching_element(self):
        with self.assertRaises(
                ValueError,
                msg='Функция должна вызывать исключение ValueError'):
            get_score(LIST_WITH_DICT, 'str')

    def test_float_searching_element(self):
        with self.assertRaises(
                ValueError,
                msg='Функция должна вызывать исключение ValueError'):
            get_score(LIST_WITH_DICT, 1.54)

    def test_empty_list(self):
        with self.assertRaises(
                ValueError,
                msg='Функция должна вызывать исключение ValueError'):
            get_score([], 1)

    def test_right_return(self):
        call = get_score(LIST_WITH_DICT, 1)
        self.assertEqual(
            call, (0, 0), 'Функция get_score() работает неправильно'
        )


class TestFindResult(unittest.TestCase):

    def test_right_return(self):
        call = find_result(LIST_WITH_DICT, 1)
        self.assertEqual(
            call, (0, 0), 'Функция find_result() работает неправильно'
        )


if __name__ == '__main__':
    unittest.main()