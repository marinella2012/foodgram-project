# foodgram-project

![foodgram workflow](https://github.com/marinella2012/foodgram-project/actions/workflows/main.yml/badge.svg)


# Описание
Cайт [Foodgram](http://marsmrn.tk) - это сайт для любителей еды. 
 

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
