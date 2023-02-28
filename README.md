# Foodgram

<img src="https://github.com/devicons/devicon/blob/master/icons/python/python-original-wordmark.svg" title="HTML5" alt="HTML" width="40" height="40"/>&nbsp;
<img src="https://github.com/devicons/devicon/blob/master/icons/django/django-plain-wordmark.svg" title="HTML5" alt="HTML" width="40" height="40"/>&nbsp;
<img src="https://github.com/devicons/devicon/blob/master/icons/mysql/mysql-original-wordmark.svg" title="HTML5" alt="HTML" width="40" height="40"/>&nbsp;
<img src="https://github.com/devicons/devicon/blob/master/icons/sqlite/sqlite-original-wordmark.svg" title="HTML5" alt="HTML" width="40" height="40"/>&nbsp;
<img src="https://github.com/devicons/devicon/blob/master/icons/postgresql/postgresql-original-wordmark.svg" title="HTML5" alt="HTML" width="40" height="40"/>&nbsp;
<img src="https://github.com/devicons/devicon/blob/master/icons/docker/docker-original-wordmark.svg" title="HTML5" alt="HTML" width="40" height="40"/>&nbsp;
<img src="https://github.com/devicons/devicon/blob/master/icons/nginx/nginx-original.svg" title="HTML5" alt="HTML" width="40" height="40"/>&nbsp;
<img src="https://github.com/devicons/devicon/blob/master/icons/ubuntu/ubuntu-plain-wordmark.svg" title="HTML5" alt="HTML" width="40" height="40"/>&nbsp;
<img src="https://github.com/devicons/devicon/blob/master/icons/vscode/vscode-original-wordmark.svg" title="HTML5" alt="HTML" width="40" height="40"/>&nbsp;

![example workflow](https://github.com/airatns/foodgram-project-react/actions/workflows/main.yml/badge.svg)

**Foodgram** is the project for publishing recipes, which allows users to subscribe to individual authors, add recipes to the favorites, download a list of ingredients of recipes they like. Authentication was realized via an Authtoken. Also realized filtering by tags and custom pagination, downloading a list of ingredients in pdf. The backend was developed in Python using Django Rest Framework. The API was used for server and application interaction. The project has been deployed **[to the server](http://46.18.107.21/recipes)** in three containers: Nginx, PostgreSQL, Django. CI and CD configured via GitHub Actions.

## **User roles:**

* **Guest**: has rights to view recipes, user pages, filter recipes by tags.

* **Authenticated user**: has rights to change his password, add recipes to the Favorites and to the Shopping List, subscribe to individual authors.

* **Administrator**: has rights to change the user's password, create a user account, create/edit/delete recipes, ingredients and tags, assign roles to users.

## **Getting Started:**

Clone the repository:

>*git clone git@github.com:airatns/foodgram-project-react.git*

Set up the virtual environment:

>*python -m venv venv*
>*source venv/scripts/activate*

Create an .env file and fill it with the next data

>*SECRET_KEY=<django project's secret key>* \
>*DEBUG=True | False*

>*DB_ENGINE=django.db.backends.postgresql* \
>*DB_NAME=postgres* \
>*POSTGRES_USER=postgres* \
>*POSTGRES_PASSWORD=postgres* \
>*DB_HOST=db* \
>*DB_PORT=5432*

Create GitHub Secrets and fill it with the next data

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

## **Before deploying on a server:**

Add the server address to the *nginx.conf* file.

Copy *docker-compose.yaml* and *nginx.conf* files to the server

>*home/<your_username>/docker-compose.yaml* \
>*home/<your_username>/nginx.conf*

## **Deploying on a server:**

Run the next commands in the IDE

>*git add .* \
>*git commit -m 'test'* \
>*git push*

In case of successful deployment, a message will be sent to the *Telegram*: **foodgram-app workflow has been successfully completed!**

Run the next commands on the server

>*sudo docker compose exec web python manage.py createsuperuser* \
>*sudo docker compose exec web python manage.py load_data*

If you need to upload the test data, run the next command

>*sudo docker compose exec web python manage.py loaddata fixtures.json*

## **Well, enjoy**

![main](https://user-images.githubusercontent.com/96816183/194041831-e1ee55d9-7f47-4d74-ab02-d8bf0ef1c0dc.png)
