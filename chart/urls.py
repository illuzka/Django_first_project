from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='HomeView'),
    path('Chart/<int:pk>/', views.ChartView.as_view(), name='ChartView'),
]