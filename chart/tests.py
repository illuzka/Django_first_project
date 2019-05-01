from django.test import TestCase
from chart.backend.data.processing import DataProcessing
from .models import ChartTicker, ChartItem, ChartItemData
from chart.backend.models.creation import ModelsCreation
import numpy as np

class TestDataProcessing(TestCase):

    def test(self):
        ModelsCreation().ticker_creation()
        ModelsCreation().chart_item_data_creation()

        tickers = ChartTicker.objects.all()
        pks = [i.pk for i in tickers]



