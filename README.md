## Сеть по продаже электроники.

### Сеть представляет собой модель иерархии партнёров, где одному партнёру соответствует только один поставщик. Завод всегда на высшем уровне и не имеет поставщиков.

### Инструменты

    - Python
    - Django DRF
    - PostgreSQL
    - Spectacular
    - JWT
    - Docker Compose

### Запуск сервера

    1) Установить docker следуя инструкции на сайте для своей ОС: https://www.docker.com/
    2) example.env переименовать в .env
    3) Заполнить .env
    4) Запустить командой: "docker-compose up -d --build"
    5) Если .env заполнен верно - запустятся 2 контейнера.
    6) Сервер доступен по адресу: http://0.0.0.0:8000/

### Команды

    Запуск через docker-compose: "docker-compose up -d --build"
    ____________________________________________________________________
    Запуск без docker-compose: "python manage.py runserver 0.0.0.0:8000"
    ____________________________________________________________________
    Создание администратора: "python manage.py csu"
    (username = admin , password = 12345)

### Поля моделей

    Partner:
        name(CharField) - Название
        type_organization(choices) - Тип организации
        Contact:
            email(EmailField) - Почта
            country(CharField) - Страна
            city(CharField) - Город
            street(CharField) - Улица
            house_number(CharField) - Номер дома
        Products:
            name(CharField) - Наименование
            model(CharField) - Модель
            release_date(DateField) - Дата выпуска
        supplier(ForeignKey) - Поставщик
        debt(DecimalField) - Задолженность
        create_at(DateTimeField) - Время создания
