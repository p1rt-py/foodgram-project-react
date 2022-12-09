# Foodgram - Продуктовый помощник
![Logo](https://is2-ssl.mzstatic.com/image/thumb/Purple124/v4/c7/24/f0/c724f011-5059-acfa-704d-0b12c467add8/source/512x512bb.jpg)\
![workflow](https://github.com/p1rt-py/foodgram-project-react/actions/workflows/main.yml/badge.svg?branch=master&event=push)

## Стек технологий

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)

## Сервер доступен по адресу:
```bash
 http://158.160.23.29/
```
```bash
 http://foodgram-practicum.ddnsking.com/
```
* Пользователи для тестирования 
```bash
user@test.ru - pass "Yandex2022"
admin@test.ru - pass "admin"
```

## Описание проекта
Foodgram - cервис позволяет публиковать собственные рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список "Избранное", а перед походом в магазин - скачивать список продуктов, необходимых для приготовления одного или нескольких выбранных блюд. 

## Подготовка к запуску и запуск проекта foodgram
* Склонировать репозиторий на локальную машину:
```bash
git clone https://git@github.com:p1rt-py/foodgram-project-react.git
cd foodgram-project-react
```
* Cоздать и активировать виртуальное окружение:
```
python -m venv venv
```
```
source venv/scripts/activate
```
```
python -m pip install --upgrade pip
```
* Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
* Перейти в папку и выполнить миграции:
```
cd backend
```
```
python manage.py migrate
```
* Заполненить базу данных CSV-файлами:
```
python manage.py up_db ingredients.csv
```
* Запустить проект:
```
python manage.py runserver
```
* Локальный сервер будет доступен по адресу:
```bash
API - http://localhost/
Redoc - http://localhost/api/docs/
Админка - http://localhost/admin/
```
## Запуск проекта в Docker контейнере

* Создать файл .env в папке проекта:
```bash
SECRET_KEY='секретный ключ'\
DEBUG=False\
DB_ENGINE=django.db.backends.postgresql\
DB_NAME=postgres\
POSTGRES_USER=postgres\
POSTGRES_PASSWORD=postgres\
DB_HOST=db\
DB_PORT=5432\
ALLOWED_HOSTS='*'
```
* Установите Docker. При необходимости добавьте/измените адреса проекта в файле nginx.conf
* Перейдите в папку infra и создайте контейнеры
```bash
cd infra/
docker-compose up -d
 ```
*  Сделать миграции: 
```bash
docker-compose exec backend python manage.py migrate
```
*  Создать суперюзера: 
```bash
docker-compose exec backend python manage.py createsuperuser
```
*  Собрать статику: 
```bash
docker-compose exec backend python manage.py collectstatic --no-input
```
*  Загрузить ингредиенты: 
```bash
docker-compose exec backend python manage.py up_db ingredients.csv
```
* Локальный сервер будет доступен по адресу:
```bash
API - http://localhost/
Redoc - http://localhost/api/docs/
Админка - http://localhost/admin/
```
### Автор  🔗
- [p1rt-py](https://github.com/p1rt-py)
