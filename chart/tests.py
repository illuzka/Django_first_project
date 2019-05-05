from django.test import TestCase
from chart.backend.data.processing import DataProcessing
from .models import ChartTicker, ChartItem, ChartItemData
from chart.backend.models.creation import ModelsCreation
import numpy as np
from datetime import datetime
import requests

class TestDataProcessing(TestCase):

    def test(self):

        key = '1de25ecebeecbd8918f258fb09d4333c50f6d855c3107a5e98650d65868c99dd'
        url_request = 'https://min-api.cryptocompare.com/data/v2/news/?lang=EN&api_key=' + key
        data = requests.get(url_request).json()

        result = []

        for x in data['Data']:
            result.append(datetime.utcfromtimestamp(x['published_on']).strftime('%Y-%m-%d %H:%M:%S'))
            result.append(x['title'])
            result.append(x['url'])
            result.append(x['body'])





