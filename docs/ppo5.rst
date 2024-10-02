Основной проект
===============

Подмодули
---------

Модуль ppo5.asgi
----------------
.. code-block:: python

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ppo5.settings')

    application = get_asgi_application()

.. automodule:: ppo5.asgi
   :members:
   :undoc-members:
   :show-inheritance:

Модуль ppo5.settings
--------------------
.. code-block:: python

    INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    'webpo.apps.WebpoConfig',
    ]

.. automodule:: ppo5.settings
   :members:
   :undoc-members:
   :show-inheritance:

Модуль ppo5.urls
----------------
.. code-block:: python

    from django.urls import path, include

    urlpatterns = [
        path('', include('webpo.urls'))
    ]

.. automodule:: ppo5.urls
   :members:
   :undoc-members:
   :show-inheritance:

Модуль ppo5.wsgi
----------------
.. code-block:: python

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ppo5.settings')

    application = get_wsgi_application()

.. automodule:: ppo5.wsgi
   :members:
   :undoc-members:
   :show-inheritance:
