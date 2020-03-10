CatBot
=====

CatBot – бот в Telegram, могущий присылать картинки с котиками и рассказывать о том, в каком созвездии находятся планеты нашей Солнечной системы.

Установка
---------

Создайте виртуальное окружение и активируйте его. После в нём выполнить:

.. code-block:: text

    pip install -r requirememts.txt 

Картинки с котиками положить в папку с названием images. Название файлов должно начинаться с cat, а заканчиваться .jpg (например: cat_fghdf.jpg)

Настрока
--------

В файле bot.py необходимо указать ваш API ключ и PROXY:

.. code-block:: python

    PROXY = {'proxy_url': 'socks5://ваш_прокси:1080',
        'urllib3_proxy_kwargs': {'username': 'ЛОГИН', 'password': 'ПАРОЛЬ'}}

    mybot = Updater('API_KEY, который вы получили у BotFather', request_kwargs=PROXY)

Запуск
------

В активно виртуальном окружении выполнить:

..code-block:: python   

    python bot.py