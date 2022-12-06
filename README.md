# Foodgram
![Logo](https://is2-ssl.mzstatic.com/image/thumb/Purple124/v4/c7/24/f0/c724f011-5059-acfa-704d-0b12c467add8/source/512x512bb.jpg)
![workflow](https://github.com/p1rt-py/foodgram-project-react/actions/workflows/main.yml/badge.svg?branch=master&event=push)

**Сервер будет доступен по адресу:**
```bash
 http://158.160.5.8/     
```
```bash
 http://foodgram-practicum.ddnsking.com/
```
```bash
user@test.ru - pass "Yandex2022"
admin@test.ru - pass "admin"
```
**Локальный сервер будет доступен по адресу:**
```bash
 http://localhost/
```


```bash
 cd infra/
 docker-compose up -d
 docker-compose exec backend python manage.py makemigrations
 docker-compose exec backend python manage.py migrate
 docker-compose exec backend python manage.py createsuperuser
 docker-compose exec backend python manage.py collectstatic --no-input
 docker-compose exec backend python manage.py up_db ingredients.csv
```
