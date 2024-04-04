import requests
import json
from fake_useragent import UserAgent


class FormingRequest:
    data_packaging = {
        "name": {
            "data": {
                "url": "https://api.himera-search.info/2.0/name_standart"
            },
            "description": "Запрос по ФИО, минимум первые три поля"
        },
        "phone": {
            "data": {
                "url": "https://api.himera-search.info/2.0/phone"
            },
            "description": "номер телефона (по формату: 79123456789)"
        },
        "passport": {
            "data": {
                "url": "https://api.himera-search.info/2.0/passport"
            },
            "description": "серия и номер паспорта без пробелов"
        },

    }

    def __init__(self, type_request: str, data: dict):
        self.type_request = type_request
        self.data = data

    def _get_data(self):
        result = self.data_packaging.get(self.type_request).get("data")
        result["data"] = self.data
        return result

    def __call__(self):
        return self._get_data()


class GetJson:
    KEY = "0a092521cfbd7a103f477a21c2231d72"
    '''
    возвращаем json при вызове экземпляра класса
    '''

    def __init__(self, data):
        self.data = data
        self.data["data"]["key"] = self.KEY

    def _fake_user_agent(self):  # crate fake user agent
        ua = UserAgent()
        fake_ua = {'user-agent': ua.random}
        return fake_ua

    def _get_json(self) -> json:
        headers = self._fake_user_agent()
        response = requests.post(url=self.data.get('url'),
                                 headers=headers, data=self.data.get("data"))
        response.encoding = 'utf-8'
        if response:
            return response.text
        else:
            print('ERROR {}'.format(response.status_code))
            raise ValueError('ERROR STATUS CODE {}'.format(response.status_code))

    def __call__(self, *args, **kwargs):
        result = json.loads(self._get_json())
        return result


class Answer:
    """
    в методе _run(self) работает с классами FormingRequest, GetJson
    и возвращает json при вызове экземпляра класса
    """

    def __init__(self, type_request, data):
        """

        :param type_request: тип запроса: по установочным данным, телефону и т.д.
        :param data: словарь из поискового запроса
        """
        self.type_request = type_request
        self.data = data

    def _run(self) -> json:
        dt = FormingRequest(type_request=self.type_request,
                            data=self.data)()
        answer = GetJson(data=dt)()
        return answer

    def __call__(self):
        return self._run()


def mane():
    type_request = "passport"
    data = {"passport": "1991123456",
            }
    result = Answer(type_request=type_request, data=data)()
    print(result)


if __name__ == "__main__":
    mane()
