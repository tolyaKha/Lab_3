from baseclient import BaseClient
import requests
import json
from datetime import datetime


class Friends(BaseClient):
    BASE_URL = 'https://api.vk.com/method/friends.get'
    http_method = 'GET'

    def __init__(self, uid):
        self.uid = uid

    def get_params(self):
        return 'user_id=' + str(self.uid) + '&fields=bdate'

    def response_handler(self, response):          #обработчик ответа
        try:
            uobj = json.loads(response.text)
            friends = uobj.get('response')

            ages = []

            for friend in friends:
                bdate = friend.get('bdate')

                if bdate is None or bdate.count('.') < 2:
                    continue

                bdate = datetime.strptime(bdate, "%d.%m.%Y")
                ndate = datetime.now()

                ages.append(int((ndate - bdate).days) // 365.2425)

            uniqages = list(set(ages))      #устранение дубликатов в массиве возрастов
            return sorted([(x, ages.count(x)) for x in uniqages], key=lambda x: x[0])
        except:
            raise Exception("Couldn't handle response for friends of uid {}".format(self.uid))

    def _get_data(self, method, http_method):
        response = requests.get(self.BASE_URL + '?' + self.get_params())
        return self.response_handler(response)