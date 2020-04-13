#### configuração ambiente de desenvolvimento
```
pipenv --python 3.7.2 install
cp .env-sample .env
make runserver
```
....

Weather API - DJANGO
===================

Solução para monitoramento da variação de temperatura de cidades. 


Sequencia para a Monitor de variação de temperatura:
-------------
> - ```$ python manage.py weather_job```

Instalação:
-------------
> - ```$ pip install -r requirements.txt```
> - ```$ python manage.py makemigrations```
> - ```$ python manage.py migrate```
> - ```$ python manage.py runserver```
> - Agora é só acessar via browser ```http://127.0.0.1:8000/```.
://googleweblight.com/?lite_url=http://fernandofreitasalves.com/tarefas-assincronas-com-django-e-celery/&ei=7zwerLD9&lc=pt-BR&s=1&m=370&host=www.google.com.br&ts=1504897919&re=1&sig=ANTY_L1er7bQsH3V7v8lITAtitJrKqJHbg)