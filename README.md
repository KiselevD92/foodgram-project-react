# сайт Foodgram, «Продуктовый помощник». 

## Описание проекта
На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Инструкции по запуску

**Как запустить проект:**
Клонировать репозиторий и перейти в него в командной строке:

```bash
@git clone https://github.com/KiselevD92/foodgram-project-react.git
@cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```bash
@python3 -m venv env
@source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```bash
@python3 -m pip install --upgrade pip
@pip install -r requirements.txt
```

Выполнить миграции:

```bash
@python3 manage.py migrate
```

Запустить проект:

```bash
@python3 manage.py runserver
```

## Вход в админку
username: admin
password: adminadmin


## Использованные технологии
Python 3.7
Django 3
Django REST Framework

## Автор
Киселев Дмитрий
