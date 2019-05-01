from chart.models import ChartTicker, ChartItem, ChartItemData
from chart.backend.data.request import DataRequest
from datetime import datetime
import numpy as np

class ModelsDataProcessing(DataRequest):

    def price_margin(self, labels):
        margins = [10, 50, 90, 130, 170, 210, 250, 290]
        stop_list = [']', '[', ',']
        tmp_price = ''.join([i for i in labels if i not in stop_list]).split()

        if float(tmp_price[0]) > 1:
            prices = ['{:.2f}'.format(i) for i in list(reversed(([round(float(i), 2) for i in tmp_price])))]
        else:
            prices = list(reversed([round(float(i), 4) for i in tmp_price]))

        margins_prices = list(zip(prices, margins))

        return margins_prices

    def volume_max_min_values(self, volume_list):
        values = [round(max(volume_list)), round(min(volume_list))]

        return values

    def volume_heights_margins(self, volume, mar_left):
        """
        max volume value = 47px
         :param volume_values:
        :return:
        """

        if max(volume) != 0:
            pixel = max(volume) / 47
            heights = [i / pixel for i in volume]
        else:
            heights = [1 for i in volume]

        margins = [59 - i for i in heights]
        mar_left_values = mar_left

        return list(zip(heights, margins, mar_left_values))

    def dates_margins_dict(self, dates_list):
        n = super().limit
        # margins = [5, 152, 299, 446, 593, 740]
        margins = [5, 142, 279, 416, 553, 690]
        counter_dates = int(n / 5)
        dates = []

        i = 0
        while i < n + 1:
            dates.append(datetime.utcfromtimestamp(dates_list[i]).strftime('%Y-%m-%d'))
            i += counter_dates

        return dict(zip(margins, dates))

    def last_item_values(self, pk):
        data = ChartTicker.objects.get(pk=pk).chartitemdata_set.all()

        open = [i for i in data.values('open')][-1]['open']
        close = [i for i in data.values('close')][-1]['close']
        high = [i for i in data.values('high')][-1]['high']
        low = [i for i in data.values('low')][-1]['low']

        if (close - open) > 1:
            change_absolute = round((close - open), 2)
            change_percent = round((abs(((close / open) - 1) * 100)), 2)
        else:
            change_absolute = round((close - open), 4)
            change_percent = round(((((close / open) - 1) * 100)), 2)

        item_up = True if ((close - open) > 0) else False

        return open, close, high, low, change_absolute, change_percent, item_up


class DataFilters:

    def __init__(self):
        pass

    def sort_by_volume(self, tickers):
        '''

        :return: [[[97286490, 1, 'BTC/USD'], [31193267, 2, 'ETH/USD'], [13158448, 3, 'LTC/USD']]
        last item volume, ticker pk, ticker name. list sorted by volume
        '''

        pks = [i.pk for i in tickers]
        volume = [list(ChartTicker.objects.get(pk=pk).chartitemdata_set.values('volume')) for pk in pks]

        result = []
        counter = 0
        while counter < len(volume):
            result.append([volume[counter][-1]['volume'], pks[counter], tickers[counter].name])
            counter += 1

        result.sort(key=lambda x: int(x[0]), reverse=True)

        return result

    def sort_by_gainers_losers(self, tickers):
        """
        :param tickers:
        :return:
        """

        pks = [i.pk for i in tickers]
        open = [list(ChartTicker.objects.get(pk=pk).chartitemdata_set.values('open')) for pk in pks]
        close = [list(ChartTicker.objects.get(pk=pk).chartitemdata_set.values('close')) for pk in pks]

        temp_list = []
        counter = 0
        while counter < len(open):
            temp_list.append((round(((((close[counter][-1]['close']) / (open[counter][-1]['open'])) - 1) * 100), 2),
                              pks[counter], tickers[counter].name))
            counter += 1

        gainers_percent = sorted(temp_list, key=lambda x: float(x[0]), reverse=True)
        losers_percent = sorted(temp_list, key=lambda x: float(x[0]))

        temp_list2 = []
        counter = 0
        while counter < len(open):
            temp_list2.append((round((close[counter][-1]['close']) - (open[counter][-1]['open']), 4), pks[counter],
                         tickers[counter].name))
            counter += 1

        gainers_abs = sorted(temp_list2, key=lambda x: float(x[0]), reverse=True)
        losers_abs = sorted(temp_list2, key=lambda x: float(x[0]))

        return gainers_percent, losers_percent, gainers_abs, losers_abs

    def sort_by_unusual_volume(self, tickers):
        pks = [i.pk for i in tickers]
        volume = [list(ChartTicker.objects.get(pk=pk).chartitemdata_set.values('volume')) for pk in pks]
        temp = []
        counter = 0

        while counter < len(volume):
            median = np.median([i['volume'] for i in volume[counter][:-1]])
            if median != 0.0:
                last_vol = volume[counter][-1]['volume']
                temp.append(((round(((last_vol / median) * 100), 1)), pks[counter], tickers[counter].name))
                counter += 1
            else:
                temp.append((0, pks[counter], tickers[counter].name))
                counter += 1

        unusual_vol = sorted(temp, key=lambda x: float(x[0]), reverse=True)

        return unusual_vol

