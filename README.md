# сайт Foodgram, «Продуктовый помощник». 

## Описание проекта
На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Инструкции по запуску

**Как запустить проект:**
Описание команд для запуска приложения в контейнерах:

```bash
sudo docker-compose up #для запуска контейнера
sudo docker-compose exec backend python manage.py migrate # выполнить миграции
sudo docker-compose exec backend python manage.py createsuperuser # создать суперпользователя
sudo docker-compose exec backend python manage.py collectstatic --no-input # собрать статику
sudo docker-compose exec backend python manage.py loaddata ./static/data/data.json #загрузка бд
```

Остановка и удаление контейнеров вместе с зависимостями
```bash
docker-compose down -v
```

Образ на сайте DockerHub
```bash
kiselevdv/foodgram-backend:latest
```

## Данные для входа в админку:
```bash
Username: admin
Password: admin
```

## Использованные технологии
Python 3.7
Django 3
Django REST Framework

## Автор
Киселев Дмитрий
