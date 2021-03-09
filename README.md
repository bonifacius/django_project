Приложение из официльного туториала на сайте:
https://djbook.ru/rel3.0/index.html

И приложение weather

Запускаем:

1. Клонируем репозиторий: git clone 
2. Переходим в папку с проектом который хотим запустить
3. Создаем виртуальное окружение: python -m venv test-django
4. Активируем окружение: source test-django/bin/activate
5. Устанавливаем необходимые пакеты: pip install -r requirements.txt
6. Делаем миграцию БД: python manage.py migrate
7. Запускаем: python manage.py runserver
# django_projects
