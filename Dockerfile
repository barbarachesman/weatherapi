RUN apk add openssh bash curl-dev make


ARG DEPLOY_PATH='/code'

RUN mkdir -p $DEPLOY_PATH/static
RUN mkdir -p /var/run/celery
WORKDIR $DEPLOY_PATH

ADD cnab/ $DEPLOY_PATH/cnab
ADD cnab_reader/ $DEPLOY_PATH/cnab_reader
ADD core/ $DEPLOY_PATH/core
ADD user_auth/ $DEPLOY_PATH/user_auth
ADD celery_config.py $DEPLOY_PATH/celery_config.py
ADD gunicorn.py $DEPLOY_PATH/gunicorn.py
ADD manage.py $DEPLOY_PATH/manage.py
ADD Makefile $DEPLOY_PATH/Makefile

ADD Pipfile $DEPLOY_PATH/Pipfile
ADD Pipfile.lock $DEPLOY_PATH/Pipfile.lock

RUN export PIP_NO_CACHE_DIR=false && pipenv install --deploy

EXPOSE 8000

CMD ["pipenv", "run", "gunicorn", "-c", "gunicorn.py", "cnab_reader.wsgi"]
