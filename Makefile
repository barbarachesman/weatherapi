STATIC_DIR = "static"
MAKEFLAGS += --silent

.DEFAULT: help

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "clean"
	@echo "		clean all compiled files"
	@echo "dependencies"
	@echo "		run docker compose for up all depencienes db, rabbitmq"
	@echo "migrate"
	@echo "		migrate database"
	@echo "makemigrations"
	@echo "		make migrations files"
	@echo "login_aws"
	@echo "		update aws token to use image resources"
	@echo "runserver"
	@echo "		run development server d'nt use in production"
	@echo "runworker"
	@echo "		run consumer queues"
	@echo "build"
	@echo "		build a docker image"


clean:
	@echo "cleaning compiled files"
	find . ! -path "./.eggs/*" -name "*.pyc" -exec rm {} \;
	find . ! -path "./.eggs/*" -name "*.pyo" -exec rm {} \;
	find . ! -path "./.eggs/*" -name ".coverage" -exec rm {} \;

login_aws:
	sh -c "`pipenv run aws ecr get-login --no-include-email`"

dependencies: clean
	@echo "start project dependencies"
	docker-compose up -d

migrate: dependencies
	pipenv run python manage.py migrate

makemigrations: dependencies
	@echo "creating migrations files"
	pipenv run python manage.py makemigrations

runserver: dependencies migrations migrate
	pipenv run python manage.py runserver

runworker: dependencies
	@echo "running celery worker"
	pipenv run celery worker -A celery_config -l INFO -Q cnab-import 

build: clean login_aws
	@echo "build image"
	docker build --no-cache -t cnab-reader .

deploy: clean
	@echo "migrate database"
	pipenv run python manage.py migrate
	@echo "upload static files to s3 bucket"
	pipenv run python manage.py collectstatic --noinput
	@echo "running application"
	pipenv run gunicorn -c gunicorn.py cnab_reader.wsgi

#############################
# Argument fix workaround
#############################
%:
	@:
