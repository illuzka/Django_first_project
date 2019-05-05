import requests
from datetime import datetime

class MarketNews:
    """
    notes:
    """

    key = '1de25ecebeecbd8918f258fb09d4333c50f6d855c3107a5e98650d65868c99dd'
    url_request = 'https://min-api.cryptocompare.com/data/v2/news/?lang=EN&api_key=' + key
    data = requests.get(url_request).json()

    def published_on(self):
        result = []
        for x in self.data['Data']:
            result.append(datetime.utcfromtimestamp(x['published_on']).strftime('%Y-%m-%d %H:%M:%S'))

        return result[:10]

    def title(self):
        result = []
        for x in self.data['Data']:
            result.append(x['title'])

        return result[:10]

    def url(self):
        result = []
        for x in self.data['Data']:
            result.append(x['url'])

        return result[:10]

    def body(self):
        result = []
        for x in self.data['Data']:
            result.append(x['body'])

        return result[:10]

