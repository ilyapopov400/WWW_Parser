import unittest
from get_json import Answer


class MyTestCase(unittest.TestCase):
    def test_name_standart(self):
        type_request = "name_standart"
        data = {"firstname": "Иван",
                "lastname": "Иванов",
                "middlename": "Иванович",
                }
        result = Answer(type_request=type_request, data=data)()
        correct_answer = {'error': 'Not enough money'}
        self.assertEqual(result == correct_answer, True)

    def test_phone(self):
        type_request = "phone"
        data = {"phone": "79123456789",
                }
        result = Answer(type_request=type_request, data=data)()
        correct_answer = {'error': 'Not enough money'}
        self.assertEqual(result == correct_answer, True)

    def test_passport(self):
        type_request = "passport"
        data = {"passport": "1991123456",
                }
        result = Answer(type_request=type_request, data=data)()
        correct_answer = {'error': 'Not enough money'}
        self.assertEqual(result == correct_answer, True)


if __name__ == '__main__':
    unittest.main()
