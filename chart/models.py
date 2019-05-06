from django.db import models


class ChartTicker(models.Model):
    name = models.CharField(max_length=10)
    labels = models.TextField()
    full_name = models.CharField(max_length=30)


class ChartItem(models.Model):
    item_margin_top = models.FloatField()
    item_height = models.FloatField()
    shadow_uheight = models.FloatField()
    shadow_dheight = models.FloatField()
    margin_left_value = models.FloatField()
    volume = models.FloatField()
    date = models.IntegerField()
    number_of_items = models.IntegerField()
    updown_item  = models.CharField(max_length=10)
    ticker = models.ForeignKey(ChartTicker, on_delete=models.CASCADE)


class ChartItemData(models.Model):
    time = models.IntegerField()
    open = models.FloatField()
    close = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    volume = models.IntegerField()
    ticker = models.ForeignKey(ChartTicker, on_delete=models.CASCADE)


class News(models.Model):
    date = models.DateTimeField()
    url = models.CharField(max_length=300)
    title = models.CharField(max_length=300)
    body = models.CharField(max_length=1000)
