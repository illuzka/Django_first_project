from chart.backend.data.clearance import DataClearance
from numpy import linspace, diff as df
from datetime import datetime
from statistics import median

class DataProcessing(DataClearance):

    """
    notes:
    """

    ADDITIONAL_ITEM = 1
    CHART_WIDTH = 750
    CLOSE = 1
    HIGH = 2
    LOW = 3
    OPEN = 4

    def __init__(self):
        super().__init__()
        self.success_response = super().response_success()[1]
        self.item_data = super().item_data()

    def max_high_min_low(self):

        maxh_minl = []
        for ticker_item in range(len(self.success_response)):
            maxh_minl.append([max([value['high'] for value in self.success_response[ticker_item]]),
                                     min([value['low'] for value in self.success_response[ticker_item]])])

        return maxh_minl

    def price_labels(self):
        # item[0] = high, item[1] = low. 8 = amount of price labels for the chart.
        price_labels = list([linspace(item[1], item[0], 8) for item in self.max_high_min_low()])

        return price_labels

    def item_direction(self):
        """
        Check if item is down, up or doji.
        :return:  List of string values.
        """
        items_direction = []

        for item in super().item_data():
            if item[1] > item[4]:
                items_direction.append('Up')
            elif item[1] < item[4]:
                items_direction.append('Down')
            else:
                items_direction.append('Doji')

        return items_direction

    def item_margins(self):
        """
        # ['time' 'close' 'high' 'low' 'open' 'volumefrom' 'volumeto']
        :notes:
        1.

        :return:
        """

        prlab_diff = [median(x) for x in df(self.price_labels())]
        item_martop = []
        item_height = []
        item_up_shadow_height = []
        item_down_shadow_height = []
        item_direction = self.item_direction()

        amt_of_items = int(len(self.item_data) / len(prlab_diff))
        i = 0
        j = amt_of_items
        item_dir_counter = 0


        for ml, d in zip(self.max_high_min_low(), prlab_diff):
            for x in range(i, j):
                try:
                    if item_direction[item_dir_counter] == 'Down':
                        item_martop.append((((ml[0] - self.item_data[x][self.OPEN]) / d) * 40) + 10 + 7.5)
                        item_height.append(((((ml[0] - self.item_data[x][self.CLOSE]) / d) * 40) + 10 + 7.5)
                                           - ((((ml[0] - self.item_data[x][self.OPEN]) / d) * 40) + 10 + 7.5))
                        item_up_shadow_height.append(abs(((((ml[0] - self.item_data[x][self.HIGH]) / d) * 40) + 10 + 7.5)
                                                     - ((((ml[0] - self.item_data[x][self.OPEN]) / d) * 40) + 10 + 7.5)))
                        item_down_shadow_height.append(abs((((((ml[0] - self.item_data[x][self.LOW]) / d) * 40) + 10 + 7.5) -
                                                 (((((ml[0] - self.item_data[x][self.OPEN]) / d) * 40) + 10 + 7.5)
                                              + (((((ml[0] - self.item_data[x][self.CLOSE]) / d) * 40) + 10 + 7.5)
                                               - ((((ml[0] - self.item_data[x][self.OPEN]) / d) * 40) + 10 + 7.5))))))
                        item_dir_counter += 1

                    elif item_direction[item_dir_counter] == 'Up':
                        item_martop.append((((ml[0] - self.item_data[x][self.CLOSE]) / d) * 40) + 10 + 7.5)
                        item_height.append(((((ml[0] - self.item_data[x][self.OPEN]) / d) * 40) + 10 + 7.5)
                                           - ((((ml[0] - self.item_data[x][self.CLOSE]) / d) * 40) + 10 + 7.5))
                        item_up_shadow_height.append(((((ml[0] - self.item_data[x][self.CLOSE]) / d) * 40) + 10 + 7.5)
                                                    - ((((ml[0] - self.item_data[x][self.HIGH]) / d) * 40) + 10 + 7.5))
                        item_down_shadow_height.append(abs( (((((ml[0] - self.item_data[x][self.LOW]) / d) * 40) + 10 + 7.5)-
                                                            (((((ml[0] - self.item_data[x][self.CLOSE]) / d) * 40) + 10 + 7.5)
                                                    + (((((ml[0] - self.item_data[x][self.OPEN]) / d) * 40) + 10 + 7.5)
                                                    - ((((ml[0] - self.item_data[x][self.CLOSE]) / d) * 40) + 10 + 7.5))))))
                        item_dir_counter += 1

                    else:
                        # If item doesnt go anywhere. Price diff = 0.
                        if d == 0:
                            item_martop.append(160)
                            item_height.append(0)
                            item_up_shadow_height.append(0)
                            item_down_shadow_height.append(0)
                        else:
                            item_martop.append((((ml[0] - self.item_data[x][self.CLOSE]) / d) * 40) + 10 + 7.5)
                            item_height.append(0)
                            item_up_shadow_height.append(((((ml[0] - self.item_data[x][self.CLOSE]) / d) * 40) + 10 + 7.5)
                                                         - ((((ml[0] - self.item_data[x][self.HIGH]) / d) * 40) + 10 + 7.5))
                            item_down_shadow_height.append(
                                        abs((((((ml[0] - self.item_data[x][self.LOW]) / d) * 40) + 10 + 7.5) -
                                             (((((ml[0] - self.item_data[x][self.CLOSE]) / d) * 40) + 10 + 7.5)
                                              + (((((ml[0] - self.item_data[x][self.OPEN]) / d) * 40) + 10 + 7.5)
                                                 - ((((ml[0] - self.item_data[x][self.CLOSE]) / d) * 40) + 10 + 7.5))))))
                        item_dir_counter += 1

                except ZeroDivisionError:
                    item_martop.append(0 + 10 + 7.5)
            i += amt_of_items
            j += amt_of_items

        return item_martop, item_height, item_up_shadow_height, item_down_shadow_height

    def item_vol_time_mrleft(self):

        """

        :return:
        """
        volume = [i[5] for i in super().item_data()]
        time = [i[0] for i in super().item_data()]
        margin_left = linspace(5, self.CHART_WIDTH-10, (super().limit + self.ADDITIONAL_ITEM))

        return volume, time, margin_left
