from chart.backend.data.request import DataRequest
from chart.backend.data.tickers import ALL_TICKER_FULL_NAMES, ALL_TICKERS
import re

class DataClearance(DataRequest):
    """
    Data clearance. !* To write comments. *!
    """

    def __init__(self):
        self.chart_data = super().chart_data_request()
        # self.coins_data = super().list_of_coins_request()

    def ticker_addition(self):
        counter = 0
        ticker_chart_data = []
        for item in self.chart_data:
            # Coins from Superclass (not all coins!).
            ticker_chart_data.append([super().coins[counter] + '/' + super().to_currency, item])
            counter += 1

        return ticker_chart_data

    def response_success(self):
        """
        Return: list of tickers and lists of data with success response.
        List of data pattern: ['time': 1555113600, 'close': 5080.66, 'high': 5128.96, 'low': 5056.19, 'open': 5081.5, 'volumefrom': 23342.24, 'volumeto': 118956124.9]
        """
        tickers_list = []
        tmp_data_list = []

        for item in self.ticker_addition():
            if item[1]['Response'] == 'Success':
                tmp_data_list.append(list(item[1]['Data']))
                tickers_list.append(item[0])

        return tickers_list, tmp_data_list

    def ticker_full_names(self):
        ticker_list = [re.sub(r'/USD', '', i) for i in self.response_success()[0]]

        result = []
        for x in ticker_list:
            try:
                result.append(ALL_TICKER_FULL_NAMES[ALL_TICKERS.index(x)])
            except ValueError:
                result.append(x)

        return result

    def item_data(self):
        """
        Return: list of tickers and lists of data with success response.
        List of data pattern:  ['time' 'close' 'high' 'low' 'open' 'volumefrom' 'volumeto']
        """
        data_list = []
        add_item = 1 # Request is for x items, but we receive x+1 items.

        for item in self.response_success()[1]:
            for keyvalues in item:
                try:
                    data_list.append(keyvalues['time'])
                    data_list.append(keyvalues['close'])
                    data_list.append(keyvalues['high'])
                    data_list.append(keyvalues['low'])
                    data_list.append(keyvalues['open'])
                    data_list.append(keyvalues['volumefrom'])
                    data_list.append(keyvalues['volumeto'])
                except KeyError as e:
                    print('DataClearance.item_data. Cannot find %s in received data.' %e)

        assert (len(data_list) % 7 == 0), 'DataClearance.item_data.len(data_list) % 7 != 0'

        # Split data_list by 7 elements.
        splitted_data_list = []

        while len(data_list) > 7:
            piece = data_list[:7]
            splitted_data_list.append(piece)
            data_list = data_list[7:]
        splitted_data_list.append(data_list)

        correct_nr_of_items = (len(self.response_success()[0])) * (super().limit + 1)
        assert correct_nr_of_items == len(splitted_data_list), 'DataClearance.item_data.correct_nr_of_items != len(splitted_data_list)'

        return splitted_data_list