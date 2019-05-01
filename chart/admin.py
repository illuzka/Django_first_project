from django.contrib import admin
from .models import ChartTicker, ChartItem


# Register your models here.
admin.site.register(ChartTicker)
admin.site.register(ChartItem)