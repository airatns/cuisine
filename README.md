http://51.250.25.11/ | admin@admin.ru | admin


# Foodgram

![example workflow](https://github.com/airatns/foodgram-project-react/actions/workflows/main.yml/badge.svg)

Это проект, где пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список "Избранное", а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## **Стек технологий**

Python, Django, PostgreSQL, Docker, Docker Hub, Gunicorn, Nginx, Ubuntu, YandexCloud

## **Пользовательские роли:**

* **Гость**: может просматривать рецепты, страницы пользователей, фильтровать рецепты по тегам.

* **Авторизованный пользователь**: может менять свой пароль, добавлять рецепты в Избранное и в Список покупок, подписываться на Авторов рецептов.

* **Администратор**: может менять пароль любого пользователя, создавать аккаунты пользователей, создавать/редактировать/удалять рецепты, ингредиенты и теги, назначать роли пользователям.

## **Подготовка проекта локально:**

Клонировать репозиторий и перейти в него в командной строке:

>*git clone git@github.com:airatns/foodgram-project-react.git*

Cоздать и активировать виртуальное окружение:

>*python -m venv venv*
>*source venv/scripts/activate*

Создать .env файл и прописать в нем следующие данные

>*SECRET_KEY=<django project's secret key>* \
>*DEBUG=True | False*

>*DB_ENGINE=django.db.backends.postgresql* \
>*DB_NAME=postgres* \
>*POSTGRES_USER=postgres* \
>*POSTGRES_PASSWORD=postgres* \
>*DB_HOST=db* \
>*DB_PORT=5432*

В GitHub добавить секреты в Secrets

>*DB_ENGINE=django.db.backends.postgresql* \
>*DB_NAME=postgres* \
>*POSTGRES_USER=postgres* \
>*POSTGRES_PASSWORD=postgres* \
>*DB_HOST=db* \
>*DB_PORT=5432*

>*DOCKER_USERNAME=<dоckerHub username>* \
>*DOCKER_PASSWORD=<dоckerHub password>*

>*USER=<server's username>* \
>*HOST=<server's IP-address>*

>*SSH_KEY=<ssh key: cat ~/.ssh/id_rsa>* \
>*PASSPHRASE=<ssh's password>*

>*TELEGRAM_TO=<telegram account ID: through @userinfobot>* \
>*TELEGRAM_TOKEN=<telegram bot token: through @BotFather>*

## **Подготовка проекта на сервере:**

Прописать в *nginx.conf* адрес сервера.

Скопировать файлы *docker-compose.yaml* и *nginx.conf* на сервер в 

>*home/<your_username>/docker-compose.yaml* \
>*home/<your_username>/nginx.conf*

## **Запуск проекта на сервере:**

Выполнить в терминале на локале команды

>*git add .* \
>*git commit -m 'test'* \
>*git push*

В случае успешного деплоя в *telegram* придет сообщение: **foodgram-app workflow успешно выполнен!**

Зайти на сервер и выполнить команды

>*sudo docker compose exec web python manage.py createsuperuser* \
>*sudo docker compose exec web python manage.py load_data*

Если требуется загрузить подготовленные тестовые данные, выполнить команду

>*sudo docker compose exec web python manage.py loaddata fixtures.json*

**Приятного просмотра**
