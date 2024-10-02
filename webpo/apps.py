from django.apps import AppConfig


class WebpoConfig(AppConfig):
    """Конфигурация приложения Webpo.
        Это класс конфигурации приложения, который содержит настройки
        для приложения Django.
        Атрибуты:
        default_auto_field (str): Строка, определяющая тип поля, используемого для автоматической генерации идентификаторов модели.

        Name (str): Имя приложения. Это должно совпадать с именем каталога приложения.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'webpo'
