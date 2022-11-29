# praktikum_new_diplom
![workflow](https://github.com/p1rt-py/foodgram-project-react/actions/workflows/main.yml/badge.svg?branch=master&event=push)
**Сервер будет доступен по адресу:**
```bash
 http://158.160.5.8/     
```
```bash
 http://foodgram-practicum.ddnsking.com/
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
