from chart.backend.data.processing import DataProcessing
from chart.backend.data.clearance import DataClearance
from chart.models import ChartTicker, ChartItem, ChartItemData


class ModelsCreation(DataProcessing, DataClearance):

    def __init__(self):
        super().__init__()
        self.margins = super().item_margins()
        self.response = super().response_success()
        self.vol_time_mrleft = super().item_vol_time_mrleft()
        self.item_dir = super().item_direction()
        self.price_labs = super().price_labels()
        self.items_data = super().item_data()
        self.ticker_full_name = super().ticker_full_names()

    def ticker_creation(self):
        counter = 0
        for ticker in self.response[0]:
            ChartTicker.objects.bulk_create([
                ChartTicker(name=ticker, labels=self.price_labs[counter], full_name=self.ticker_full_name[counter])
            ])
            counter += 1

    def tickers(self):
        # super().response_success()[0] correct formatting. (tickers)
        tickers_list = []
        for i in self.response[0]:
            for j in range(super().limit + super().ADDITIONAL_ITEM):
                tickers_list.append(i)
        return tickers_list

    def items_creation(self):
        tickers = self.tickers()
        nr_of_items = len(self.response[0]) * (super().limit + super().ADDITIONAL_ITEM)

        # item_vol_time_mrleft()[2] correct formatting. (margin-left)
        margin_left = []
        for i in range(len(self.response[0])):
            margin_left += [float(i) for i in self.vol_time_mrleft[2]]

        # ChartItem models creation.
        counter = 0
        for item in range(nr_of_items):
            ChartItem.objects.bulk_create([
                ChartItem(item_margin_top=self.margins[0][counter],
                          item_height=self.margins[1][counter],
                          shadow_uheight=self.margins[2][counter],
                          shadow_dheight=self.margins[3][counter],
                          margin_left_value=margin_left[counter],
                          volume=self.vol_time_mrleft[0][counter],
                          date=self.vol_time_mrleft[1][counter],
                          number_of_items=nr_of_items,
                          updown_item=self.item_dir[counter],
                          ticker = ChartTicker.objects.get(name=tickers[counter])
            )])
            counter += 1

    def chart_item_data_creation(self):
        tickers = self.tickers()

        # Chart_item_raw_data_creation models creation.
        counter = 0
        for item in self.items_data:
            ChartItemData.objects.bulk_create([
                ChartItemData(time=item[0],
                                 close=item[1],
                                 high=item[2],
                                 low=item[3],
                                 open=item[4],
                                 volume=item[6],
                                 ticker=ChartTicker.objects.get(name=tickers[counter])
                                 )])

            counter += 1