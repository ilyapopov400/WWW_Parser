import requests
from fake_useragent import UserAgent

KEY = "0a092521cfbd7a103f477a21c2231d72"
URL = "https://api.himera-search.info/2.0/phone"
params = {"key": KEY,
          "phone": "79123456789"}


class GetHtml:
    '''
    получаем html в виде строки с использованием UserAgent
    '''

    def __init__(self, url, params=None):
        self.url = url
        self.params = params

    def _fake_user_agent(self):  # crate fake user agent
        ua = UserAgent()
        fake_ua = {'user-agent': ua.random}
        return fake_ua

    def _response_html(self) -> str:
        header = self._fake_user_agent()
        response = requests.get(url=self.url, params=self.params, headers=header)
        response.encoding = 'utf-8'
        if response:
            print(response.status_code)
            return response.text
        else:
            print('ERROR {}'.format(response.status_code))
            return False  # если страницы нет

    def __call__(self, *args, **kwargs):
        html = self._response_html()
        return html


def mane():
    result = GetHtml(url=URL, params=params)()
    print(result)


if __name__ == "__main__":
    mane()
