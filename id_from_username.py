from baseclient import BaseClient
import requests   #библиотека запросы
import json


class IdFromUsername(BaseClient):
    BASE_URL = 'https://api.vk.com/method/users.get'
    http_method = 'GET'

    def __init__(self, name):
        self.name = name

    def get_params(self):
        return 'user_ids=' + self.name

    def response_handler(self, response):    #обработчик ответа
        try:
            uobj = json.loads(response.text)
            return uobj.get('response')[0].get('uid')
        except:
            raise Exception("Couldn't handle response for username {}".format(self.name))

    def _get_data(self, method, http_method):
        response = None

        response = requests.get(self.BASE_URL + '?' + self.get_params())
        return self.response_handler(response)