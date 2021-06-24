# foodgram-project

![foodgram workflow](https://github.com/marinella2012/foodgram-project/actions/workflows/foodgram_workflow.yml/badge.svg)


# Описание
Cайт «Foodgram».
 

# Порядок установки
## В режиме разработки
1. Установить виртуальный интерпретатор `python3 -m venv venv`

После выполнения этой команды в директории проекта появится папка venv, в которой хранятся служебные файлы виртуального окружения. Там же будут сохранены все зависимости проекта.

2. Ативировать виртуальное окружение в зависимости от операционной системы  
   Unix-системы: `source venv/bin/activate`  
   Windows: `source venv/Scripts/activate`

В терминале появится уведомление о том, что вы работаете в виртуальном окружении: строка  (venv) будет предварять все команды.

3. Установите необходимые пакеты `pip install -r requirements.txt`
4. Создайте необходимые миграции:   
   ```python manage.py makemigrations```
5. Накатите созданные миграции в БД  
   ```python manage.py migrate```
6. Создайте суперпользователя:  
   ```python manage.py createsuperuser```
7. Соберите статику  
   ```python manage.py collectstatic --no-input```
8. Запустите приложение в терминале `python manage.py runserver`
9. Приложение будет доступно по адресу  
   ```http://127.0.0.1/```

## В режиме запуска на сервере
1. Запустите докер  
   ```docker-compose up -d --build```
2. Создайте необходимые миграции:   
   ```docker-compose exec web python manage.py makemigrations api```
3. Накатите созданные миграции в БД  
   ```docker-compose exec web python manage.py migrate```
4. Создайте суперпользователя:  
   ```docker-compose exec web python manage.py createsuperuser```
5. Соберите статику  
   ```docker-compose exec web python manage.py collectstatic --no-input```
6. Приложение будет доступно по адресу  
   ```http://127.0.0.1/```
   
# База данных
Если же вам нужна чистая база, но уже чтобы были какие-то ингредиенты, то для загрузки тестовых ингредиентов существует команда `python manage.py load_data` , которая загрузит только тестовые ингредиенты.  
Тестировать пустой проект будет неудобно, а наполнять его руками — долго.
