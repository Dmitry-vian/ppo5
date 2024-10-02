"""
Модуль маршрутов URL для приложения.
Этот модуль определяет маршруты URL и связывает их с представлениями (views) приложения.
Функции:
urlpatterns (list): Список маршрутов URL для приложения.
"""

from django.urls import path
from .views import send_to_client

urlpatterns = [
    path('send/', send_to_client, name='send/'),
]
